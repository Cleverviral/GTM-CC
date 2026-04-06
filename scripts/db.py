"""
GTM-CC Database Access Utility
Safe wrapper around Neon SQL-over-HTTP API.
All operator commands use this — never raw HTTP calls.
"""

import urllib.request
import json
import ssl
import os
import csv
import io
from datetime import datetime

# ── Connection ──────────────────────────────────────────────

def _get_connection():
    """Read connection string from .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    conn_str = None

    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.split('#')[0].strip()  # Remove inline comments
                if key in ('NEON_CONNECTION_STRING', 'NEON_TEST_CONNECTION_STRING'):
                    conn_str = val
                    break

    if not conn_str:
        raise RuntimeError("No NEON_CONNECTION_STRING or NEON_TEST_CONNECTION_STRING found in .env")

    # Extract host from connection string
    # Format: postgresql://user:pass@host/db?sslmode=require
    host = conn_str.split('@')[1].split('/')[0]
    return conn_str, host


# ── Safety Checks ───────────────────────────────────────────

BLOCKED_KEYWORDS = ['DELETE', 'DROP', 'TRUNCATE', 'ALTER']

def _safety_check(sql):
    """Block dangerous SQL operations."""
    upper = sql.strip().upper()
    for kw in BLOCKED_KEYWORDS:
        if upper.startswith(kw) or f' {kw} ' in upper:
            raise ValueError(f"BLOCKED: {kw} statements are not allowed. Contact Mayank if you need this.")

    # Check for UPDATE without WHERE
    if upper.startswith('UPDATE') and 'WHERE' not in upper:
        raise ValueError("BLOCKED: UPDATE without WHERE clause. Every UPDATE must have a WHERE condition.")


# ── Core Query Function ────────────────────────────────────

def query(sql, params=None):
    """
    Execute a SQL query against Neon via HTTP.
    Returns: dict with 'rows', 'fields', 'rowCount' keys.
    """
    _safety_check(sql)

    conn_str, host = _get_connection()
    url = f'https://{host}/sql'

    body = {'query': sql}
    if params:
        body['params'] = params

    payload = json.dumps(body).encode()
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Neon-Connection-String', conn_str)

    ctx = ssl.create_default_context()
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        result = json.loads(resp.read().decode())
        return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            raise RuntimeError(f"Database error: {error_json.get('message', error_body)}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Database error ({e.code}): {error_body}")


# ── Read Query (SELECT only) ──────────────────────────────

def read_query(sql, params=None):
    """
    Execute a SELECT query. Returns list of row dicts.
    Automatically adds LIMIT 500 if no LIMIT clause present.
    """
    upper = sql.strip().upper()
    if not upper.startswith('SELECT') and not upper.startswith('WITH'):
        raise ValueError("read_query() only accepts SELECT queries. Use write_query() for INSERT/UPDATE.")

    # Auto-add LIMIT if missing
    if 'LIMIT' not in upper:
        sql = sql.rstrip(';') + ' LIMIT 500'

    result = query(sql, params)
    return result.get('rows', [])


# ── Write Query (INSERT/UPDATE) ───────────────────────────

def write_query(sql, params=None, confirmed=False):
    """
    Execute an INSERT or UPDATE query.
    Shows preview and requires confirmation unless confirmed=True.
    Returns: result dict with rowCount.
    """
    upper = sql.strip().upper()
    if upper.startswith('SELECT'):
        raise ValueError("write_query() is for INSERT/UPDATE. Use read_query() for SELECT.")

    if not confirmed:
        print("\n" + "=" * 60)
        print("WRITE OPERATION PREVIEW")
        print("=" * 60)
        print(f"SQL: {sql}")
        if params:
            print(f"Params: {params}")
        print("=" * 60)
        print("Call write_query(..., confirmed=True) to execute.")
        print("=" * 60 + "\n")
        return None

    result = query(sql, params)
    row_count = result.get('rowCount', 0)
    print(f"Done. {row_count} row(s) affected.")
    return result


# ── Convenience Functions ──────────────────────────────────

def get_clients(active_only=True):
    """Get list of clients."""
    sql = "SELECT client_id, client_name, client_website, client_status FROM clients"
    if active_only:
        sql += " WHERE client_status = 'active'"
    sql += " ORDER BY client_name"
    return read_query(sql)


def get_segments(client_id):
    """Get segments for a specific client."""
    return read_query(
        "SELECT s.segment_id, s.segment_name, s.segment_tag, s.status "
        "FROM segments s WHERE s.client_id = $1 ORDER BY s.segment_id",
        [str(client_id)]
    )


def get_lead_count(segment_id):
    """Count leads in a segment."""
    rows = read_query(
        "SELECT COUNT(*) as cnt FROM leads WHERE $1 = ANY(segment_ids)",
        [segment_id]
    )
    return rows[0]['cnt'] if rows else 0


def get_leads_for_segment(segment_id, limit=500, filters=None):
    """
    Pull leads for a segment with optional filters.
    filters: dict with optional keys:
        - email_verified: 'true'/'false'
        - country: str
        - min_visits: int
        - max_visits: int
        - has_email_outputs: bool (join check)
    """
    sql = """
        SELECT l.*, s.segment_name, s.segment_tag
        FROM leads l
        JOIN segments s ON s.segment_id = $1
        WHERE $1 = ANY(l.segment_ids)
    """
    params = [segment_id]
    param_idx = 2

    if filters:
        if 'email_verified' in filters:
            sql += f" AND l.email_verified = ${param_idx}"
            params.append(filters['email_verified'])
            param_idx += 1
        if 'country' in filters:
            sql += f" AND l.country ILIKE ${param_idx}"
            params.append(filters['country'])
            param_idx += 1
        if 'min_visits' in filters:
            sql += f" AND l.monthly_visits >= ${param_idx}"
            params.append(filters['min_visits'])
            param_idx += 1
        if 'max_visits' in filters:
            sql += f" AND l.monthly_visits <= ${param_idx}"
            params.append(filters['max_visits'])
            param_idx += 1

    sql += f" ORDER BY l.lead_id LIMIT ${param_idx}"
    params.append(limit)

    return read_query(sql, params)


def get_leads_with_outputs(segment_id, recipe_id=None, limit=500):
    """Pull leads with their latest email outputs for a segment."""
    sql = """
        SELECT l.lead_id, l.email, l.first_name, l.last_name, l.full_name,
               l.company_name, l.company_domain, l.company_website, l.job_title,
               l.linkedin_profile_url, l.industry, l.monthly_visits, l.employee_count,
               l.email_verified, l.email_verified_at, l.is_catchall, l.mx_provider,
               l.has_email_security_gateway, l.lcp, l.tti, l.aov, l.extra_data,
               eo.output_id, eo.recipe_id, eo.recipe_version, eo.selected_approach,
               eo.email_1_variant_a, eo.email_1_variant_b,
               eo.email_2_variant_a, eo.email_2_variant_b,
               eo.email_3_variant_a, eo.email_3_variant_b,
               eo.company_summary
        FROM leads l
        LEFT JOIN LATERAL (
            SELECT * FROM email_outputs eo2
            WHERE eo2.lead_id = l.lead_id AND eo2.segment_id = $1
            ORDER BY eo2.created_at DESC LIMIT 1
        ) eo ON true
        WHERE $1 = ANY(l.segment_ids)
    """
    params = [segment_id]

    if recipe_id:
        sql += " AND eo.recipe_id = $2"
        params.append(recipe_id)

    sql += f" ORDER BY l.lead_id LIMIT {limit}"
    return read_query(sql, params)


def get_active_recipe(segment_id):
    """Get the active recipe for a segment."""
    rows = read_query(
        "SELECT * FROM recipes WHERE segment_id = $1 AND status = 'active' LIMIT 1",
        [segment_id]
    )
    return rows[0] if rows else None


def get_batches(segment_id=None, limit=10):
    """Get recent batch summaries."""
    sql = """
        SELECT eo.batch_id,
               COUNT(*) as lead_count,
               MIN(eo.created_at) as started_at,
               MAX(eo.created_at) as completed_at,
               eo.recipe_version,
               eo.segment_id,
               s.segment_name
        FROM email_outputs eo
        JOIN segments s ON s.segment_id = eo.segment_id
    """
    params = []
    if segment_id:
        sql += " WHERE eo.segment_id = $1"
        params.append(segment_id)

    sql += """
        GROUP BY eo.batch_id, eo.recipe_version, eo.segment_id, s.segment_name
        ORDER BY MIN(eo.created_at) DESC
        LIMIT $%d
    """ % (len(params) + 1)
    params.append(limit)

    return read_query(sql, params)


def export_to_csv(rows, filepath, columns=None):
    """Export rows to a CSV file."""
    if not rows:
        print("No rows to export.")
        return None

    if not columns:
        columns = list(rows[0].keys())

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Exported {len(rows)} rows to {filepath}")
    return filepath


# ── Clay Push Payload Builder ─────────────────────────────

def build_clay_payload(lead, client, segment, recipe, batch_id):
    """
    Build the standardized 38-field JSON payload for a single lead push to Clay.

    Args:
        lead: dict from get_leads_with_outputs() — includes lead fields + existing outputs
        client: dict with client_id, client_name
        segment: dict with segment_id, segment_name, segment_tag, leadlist_context, value_prop
        recipe: dict from get_active_recipe() — or None if no recipe
        batch_id: str — format: {client_tag}_{segment_tag}_{YYYYMMDD}_{seq}

    Returns: dict ready to POST as JSON to Clay webhook
    """
    return {
        # Identity (7)
        "lead_id": lead.get("lead_id"),
        "email": lead.get("email"),
        "first_name": lead.get("first_name"),
        "last_name": lead.get("last_name"),
        "full_name": lead.get("full_name"),
        "job_title": lead.get("job_title"),
        "linkedin_profile_url": lead.get("linkedin_profile_url"),

        # Company (5)
        "company_name": lead.get("company_name"),
        "company_domain": lead.get("company_domain"),
        "company_website": lead.get("company_website"),
        "industry": lead.get("industry"),
        "employee_count": lead.get("employee_count"),

        # Enrichment (4)
        "monthly_visits": lead.get("monthly_visits"),
        "lcp": lead.get("lcp"),
        "tti": lead.get("tti"),
        "aov": lead.get("aov"),

        # Verification (5)
        "email_verified": lead.get("email_verified"),
        "email_verified_at": str(lead.get("email_verified_at") or ""),
        "is_catchall": lead.get("is_catchall"),
        "mx_provider": lead.get("mx_provider"),
        "has_email_security_gateway": lead.get("has_email_security_gateway", ""),

        # Client (2)
        "client_id": str(client.get("client_id", "")),
        "client_name": client.get("client_name"),

        # Segment (5) — value_prop lives on segment level
        "segment_id": segment.get("segment_id"),
        "segment_name": segment.get("segment_name"),
        "segment_tag": segment.get("segment_tag"),
        "lead_list_context": segment.get("leadlist_context"),
        "value_prop": segment.get("value_prop"),

        # Batch + Recipe (3)
        "recipe_id": recipe["recipe_id"] if recipe else None,
        "current_recipe_version": recipe["version"] if recipe else None,
        "batch_id": batch_id,

        # Existing outputs (7) — from LEFT JOIN in get_leads_with_outputs
        "last_recipe_version": lead.get("recipe_version"),
        "existing_email_1_variant_a": lead.get("email_1_variant_a"),
        "existing_email_1_variant_b": lead.get("email_1_variant_b"),
        "existing_email_2_variant_a": lead.get("email_2_variant_a"),
        "existing_email_2_variant_b": lead.get("email_2_variant_b"),
        "existing_email_3_variant_a": lead.get("email_3_variant_a"),
        "existing_email_3_variant_b": lead.get("email_3_variant_b"),
    }


def generate_batch_id(client_name, segment_tag):
    """Generate a batch ID: {client_tag}_{segment_tag}_{YYYYMMDD}_{seq}."""
    import re
    client_tag = re.sub(r'[^a-z0-9]', '-', client_name.lower()).strip('-')
    seg_tag = re.sub(r'[^a-z0-9]', '-', segment_tag.lower()).strip('-')
    date_str = datetime.now().strftime('%Y%m%d')
    base = f"{client_tag}_{seg_tag}_{date_str}"

    # Check for existing batches today
    existing = read_query(
        "SELECT DISTINCT batch_id FROM email_outputs WHERE batch_id LIKE $1",
        [f"{base}%"]
    )
    seq = len(existing) + 1
    return f"{base}_{seq:03d}"


def push_to_clay_webhook(webhook_url, payload):
    """POST a single lead payload to a Clay webhook URL. Returns (success, status_code, error)."""
    import time
    data = json.dumps(payload).encode()
    req = urllib.request.Request(webhook_url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    ctx = ssl.create_default_context()
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        return True, resp.status, None
    except urllib.error.HTTPError as e:
        return False, e.code, e.read().decode()
    except Exception as e:
        return False, 0, str(e)


# ── Quick Test ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Testing connection...")
    clients = get_clients(active_only=False)
    print(f"Found {len(clients)} clients:")
    for c in clients:
        print(f"  - {c['client_name']} ({c['client_status']})")
