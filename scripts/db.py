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
        SELECT l.lead_id, l.email, l.first_name, l.last_name, l.company_name,
               l.company_domain, l.job_title, l.industry, l.monthly_visits,
               l.email_verified, l.lcp, l.tti, l.aov, l.extra_data,
               eo.output_id, eo.recipe_id, eo.recipe_version, eo.selected_approach,
               eo.subject_line_1, eo.subject_line_2,
               eo.email_1_variant_a, eo.email_1_variant_b, eo.email_1_variant_c,
               eo.email_2_variant_a, eo.email_2_variant_b, eo.email_2_variant_c,
               eo.email_3_variant_a, eo.email_3_variant_b, eo.email_3_variant_c,
               eo.company_summary, eo.batch_id
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


# ── Quick Test ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Testing connection...")
    clients = get_clients(active_only=False)
    print(f"Found {len(clients)} clients:")
    for c in clients:
        print(f"  - {c['client_name']} ({c['client_status']})")
