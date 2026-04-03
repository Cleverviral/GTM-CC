#!/usr/bin/env python3
"""
GTM-CC Test Project Setup
=========================
Creates v3.1 schema on the new GTM-CC-Test Neon project
and migrates 1,000 Speedsize leads from Supabase.

Safety:
- WRITES ONLY to: GTM-CC-Test Neon project (delicate-wave-68549342)
- READ ONLY from: Supabase (lfpsdwrrseqqhabzojug)
- READ ONLY from: Neon Cleverviral (rough-queen-94797098)
- NEVER touches existing Neon Cleverviral data
"""

import urllib.request
import urllib.parse
import json
import ssl
import sys
import time

# === CONFIG ===
# Load from .env — never hardcode credentials
import os
_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
_env = {}
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                _env[k.strip()] = v.split('#')[0].strip()

SUPABASE_URL = _env.get('SUPABASE_URL', '')
SUPABASE_KEY = _env.get('SUPABASE_SERVICE_ROLE_KEY', '')
NEON_CLEVERVIRAL_CONNSTR = _env.get('NEON_CONNECTION_STRING', '')
NEON_TEST_CONNSTR = _env.get('NEON_TEST_CONNECTION_STRING', '')
NEON_TEST_HOST = NEON_TEST_CONNSTR.split('@')[1].split('/')[0] if '@' in NEON_TEST_CONNSTR else ''

SPEEDSIZE_SUPABASE_ID = "07645f11-f326-4624-ac3b-76c1e6a597ec"
SPEEDSIZE_NEON_ID = "a1b2c3d4-0000-0000-0000-000000000001"

# === HELPERS ===
ctx = ssl.create_default_context()

def neon_sql(query, connstr=NEON_TEST_CONNSTR):
    """Execute SQL on Neon via HTTP API."""
    host = urllib.parse.urlparse(connstr).hostname
    url = f"https://{host}/sql"
    payload = json.dumps({"query": query, "params": []}).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Neon-Connection-String", connstr)
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read())

def supabase_get(path, params=None):
    """GET from Supabase REST API."""
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read())

def supabase_get_raw(path):
    """GET from Supabase with full URL params (for complex queries)."""
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read())

def log(msg):
    print(f"  {'>'} {msg}")

# ============================================================
# STEP 1: CREATE SCHEMA ON GTM-CC-TEST
# ============================================================
print("\n" + "="*60)
print("STEP 1: Creating v3.1 schema on GTM-CC-Test")
print("="*60)

# Define each statement separately — Neon HTTP API is single-statement only
schema_statements = [
    "DROP TABLE IF EXISTS email_outputs CASCADE",
    "DROP TABLE IF EXISTS recipes CASCADE",
    "DROP TABLE IF EXISTS leads CASCADE",
    "DROP TABLE IF EXISTS segments CASCADE",
    "DROP TABLE IF EXISTS clients CASCADE",

    """CREATE TABLE clients (
        client_id UUID PRIMARY KEY,
        client_name TEXT NOT NULL,
        client_website TEXT,
        client_status TEXT DEFAULT 'active',
        primary_poc_name TEXT,
        primary_poc_email TEXT,
        target_icp_details TEXT,
        target_persona TEXT,
        pain_points TEXT,
        client_usp_differentiators TEXT,
        all_client_sales_resources TEXT,
        all_social_proof_brand_names TEXT,
        client_call_to_action TEXT,
        complimentary_sales_value TEXT,
        casestudy_or_leadmagnet_links TEXT,
        dnc_list_url TEXT,
        client_crm TEXT,
        notification_channels TEXT,
        slack_main_channel_id TEXT,
        ar_mode TEXT,
        ar_context_doc TEXT,
        approved BOOLEAN DEFAULT false,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    )""",

    """CREATE TABLE segments (
        segment_id SERIAL PRIMARY KEY,
        client_id UUID NOT NULL REFERENCES clients(client_id),
        segment_name TEXT NOT NULL,
        segment_tag TEXT NOT NULL UNIQUE,
        description TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        UNIQUE(client_id, segment_name)
    )""",

    """CREATE TABLE leads (
        lead_id SERIAL PRIMARY KEY,
        email TEXT UNIQUE,
        first_name TEXT, last_name TEXT, full_name TEXT,
        job_title TEXT,
        linkedin_profile_url TEXT, linkedin_username TEXT,
        company_name TEXT, company_domain TEXT, company_website TEXT,
        company_linkedin_url TEXT, industry TEXT,
        monthly_visits INTEGER, employee_count TEXT,
        email_verified TEXT, email_verified_at TIMESTAMPTZ,
        mx_provider TEXT, has_email_security_gateway TEXT,
        is_catchall TEXT, is_personal_email BOOLEAN,
        city TEXT, country TEXT,
        lcp FLOAT, tti FLOAT, aov FLOAT,
        tags TEXT[] DEFAULT '{}',
        info_tags TEXT[] DEFAULT '{}',
        extra_data JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW()
    )""",

    "CREATE INDEX idx_leads_email ON leads(email)",
    "CREATE INDEX idx_leads_linkedin_username ON leads(linkedin_username)",
    "CREATE INDEX idx_leads_company_domain ON leads(company_domain)",
    "CREATE INDEX idx_leads_tags ON leads USING GIN(tags)",
    "CREATE INDEX idx_leads_info_tags ON leads USING GIN(info_tags)",

    """CREATE TABLE recipes (
        recipe_id SERIAL PRIMARY KEY,
        client_id UUID NOT NULL REFERENCES clients(client_id),
        segment_id INTEGER NOT NULL REFERENCES segments(segment_id),
        version INTEGER NOT NULL DEFAULT 1,
        status TEXT DEFAULT 'testing',
        parent_recipe_id INTEGER REFERENCES recipes(recipe_id),
        approach_content TEXT, value_prop TEXT, lead_list_context TEXT,
        data_variables_required TEXT[], enrichment_sources TEXT[],
        clay_template_name TEXT, clay_instructions TEXT,
        notes TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        UNIQUE(client_id, segment_id, version)
    )""",

    """CREATE TABLE email_outputs (
        output_id SERIAL PRIMARY KEY,
        lead_id INTEGER NOT NULL REFERENCES leads(lead_id),
        client_id UUID NOT NULL REFERENCES clients(client_id),
        segment_id INTEGER NOT NULL REFERENCES segments(segment_id),
        recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id),
        recipe_version INTEGER NOT NULL,
        selected_approach TEXT,
        subject_line TEXT, email_body TEXT, company_summary TEXT,
        batch_id TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW()
    )""",

    "CREATE INDEX idx_email_outputs_lead ON email_outputs(lead_id)",
    "CREATE INDEX idx_email_outputs_client_segment ON email_outputs(client_id, segment_id)",
    "CREATE INDEX idx_email_outputs_recipe ON email_outputs(recipe_id)",
    "CREATE INDEX idx_email_outputs_batch ON email_outputs(batch_id)",
]

log(f"Executing {len(schema_statements)} SQL statements...")
for i, stmt in enumerate(schema_statements):
    try:
        neon_sql(stmt)
        first_line = stmt.strip().split('\n')[0][:60]
        log(f"  [{i+1}/{len(schema_statements)}] {first_line}")
    except Exception as e:
        err_body = ""
        if hasattr(e, 'read'):
            err_body = e.read().decode()
        print(f"  ERROR on statement {i+1}: {e}")
        if err_body:
            print(f"  Detail: {err_body[:200]}")
        sys.exit(1)

log("Schema created successfully!")
log("Note: upsert_lead function will be added separately (requires $$ syntax handling)")

# Verify tables
result = neon_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
tables = [r["table_name"] for r in result["rows"]]
log(f"Tables created: {tables}")

# ============================================================
# STEP 2: INSERT SPEEDSIZE CLIENT (from Neon Cleverviral)
# ============================================================
print("\n" + "="*60)
print("STEP 2: Copying Speedsize client from Neon Cleverviral")
print("="*60)

# Read Speedsize from Neon Cleverviral (READ ONLY)
cv_result = neon_sql(
    f"SELECT client_id, client_name, client_website, client_status, "
    f"client_call_to_action, complimentary_sales_value, client_usp_differentiators, "
    f"dnc_list_url, slack_main_channel_id, ar_context_doc "
    f"FROM clients WHERE client_id = '{SPEEDSIZE_NEON_ID}'",
    connstr=NEON_CLEVERVIRAL_CONNSTR
)
ss_client = cv_result["rows"][0]
log(f"Read from Neon Cleverviral: {ss_client['client_name']} ({ss_client['client_id']})")

# Safely escape single quotes
def esc(val):
    if val is None:
        return "NULL"
    return "'" + str(val).replace("'", "''") + "'"

# Insert into test project
insert_client = f"""
INSERT INTO clients (client_id, client_name, client_website, client_status,
    client_call_to_action, complimentary_sales_value, client_usp_differentiators,
    dnc_list_url, slack_main_channel_id, ar_context_doc, approved)
VALUES (
    '{ss_client['client_id']}',
    {esc(ss_client['client_name'])},
    {esc(ss_client['client_website'])},
    {esc(ss_client.get('client_status', 'active'))},
    {esc(ss_client.get('client_call_to_action'))},
    {esc(ss_client.get('complimentary_sales_value'))},
    {esc(ss_client.get('client_usp_differentiators'))},
    {esc(ss_client.get('dnc_list_url'))},
    {esc(ss_client.get('slack_main_channel_id'))},
    {esc(ss_client.get('ar_context_doc'))},
    true
)
"""
neon_sql(insert_client)
log("Speedsize client inserted into GTM-CC-Test")

# ============================================================
# STEP 3: CREATE 4 SEGMENTS
# ============================================================
print("\n" + "="*60)
print("STEP 3: Creating Speedsize segments")
print("="*60)

segments = [
    ("1M+ Qualified", "speedsize-1m-plus-qualified", "Ecommerce sites with 1M+ monthly visits, qualified leads"),
    ("100K-1M Qualified", "speedsize-100k-1m-qualified", "Ecommerce sites with 100K-1M monthly visits, qualified leads"),
    ("150K-200K Qualified", "speedsize-150k-200k-qualified", "Ecommerce sites with 150K-200K monthly visits, qualified leads"),
    ("50K-100K Qualified", "speedsize-50k-100k-qualified", "Ecommerce sites with 50K-100K monthly visits, qualified leads"),
]

for name, tag, desc in segments:
    neon_sql(f"""
        INSERT INTO segments (client_id, segment_name, segment_tag, description)
        VALUES ('{SPEEDSIZE_NEON_ID}', '{name}', '{tag}', '{desc}')
    """)
    log(f"Created segment: {tag}")

# Verify segments
result = neon_sql("SELECT segment_id, segment_name, segment_tag FROM segments ORDER BY segment_id")
for r in result["rows"]:
    log(f"  #{r['segment_id']}: {r['segment_tag']}")

# ============================================================
# STEP 4: PULL 1,000 SPEEDSIZE CONTACTS FROM SUPABASE
# ============================================================
print("\n" + "="*60)
print("STEP 4: Pulling 1,000 Speedsize contacts from Supabase (READ ONLY)")
print("="*60)

# Get 1,000 contact IDs linked to Speedsize
junction_rows = supabase_get_raw(
    f"client_contacts?client_id=eq.{SPEEDSIZE_SUPABASE_ID}"
    f"&select=contact_id,clay_table_names&limit=1100"
)
log(f"Fetched {len(junction_rows)} junction rows")

# Get unique contact IDs + their clay_table_names mapping
contact_clay_map = {}
for row in junction_rows:
    cid = row["contact_id"]
    names = row.get("clay_table_names") or []
    if cid not in contact_clay_map:
        contact_clay_map[cid] = []
    contact_clay_map[cid].extend(names)

unique_ids = list(contact_clay_map.keys())[:1000]
log(f"Unique contact IDs: {len(unique_ids)}")

# Fetch contacts in batches of 50
all_contacts = []
for i in range(0, len(unique_ids), 50):
    batch = unique_ids[i:i+50]
    ids_str = ",".join(batch)
    contacts = supabase_get_raw(
        f"contacts?id=in.({ids_str})"
        f"&select=id,email,first_name,last_name,full_name,job_title,"
        f"linkedin_profile_url,company_name,company_domain,company_website,"
        f"company_linkedin_url,industry,monthly_visits,employee_count,"
        f"email_verified,mx_provider,has_email_security_gateway,is_catchall,"
        f"is_personal_email,tags,extra_data"
    )
    all_contacts.extend(contacts)
    if (i // 50) % 5 == 0:
        log(f"  Fetched {len(all_contacts)}/{len(unique_ids)} contacts...")

log(f"Total contacts fetched: {len(all_contacts)}")

# ============================================================
# STEP 5: ASSIGN SEGMENT TAGS + MIGRATE TO NEON
# ============================================================
print("\n" + "="*60)
print("STEP 5: Assigning segment tags and inserting leads")
print("="*60)

def assign_segment_tag(contact, clay_names):
    """Assign segment_tag based on monthly_visits (from Supabase data)."""
    visits = contact.get("monthly_visits")
    if visits is None:
        return "speedsize-100k-1m-qualified"  # Default for unknowns
    visits = int(visits) if visits else 0
    if visits >= 1_000_000:
        return "speedsize-1m-plus-qualified"
    elif 150_000 <= visits <= 200_000:
        return "speedsize-150k-200k-qualified"
    elif 100_000 <= visits < 1_000_000:
        return "speedsize-100k-1m-qualified"
    elif 50_000 <= visits < 100_000:
        return "speedsize-50k-100k-qualified"
    else:
        # Below 50K — assign to 50K-100K as catch-all for test
        return "speedsize-50k-100k-qualified"

def build_info_tags(contact, clay_names):
    """Build info_tags from old Supabase tags + clay_table_names."""
    info = []

    # Convert old tags to info_tags
    old_tags = contact.get("tags") or []
    for t in old_tags:
        if t.startswith("ss-"):
            info.append(t)  # Keep as-is for now
        elif t == "builtwith-data":
            info.append("src:builtwith")
        elif "apollo" in t.lower():
            info.append("src:apollo")
        elif t == "20k-plus-new":
            info.append(t)
        else:
            info.append(t)

    # Derive source from clay_table_names
    for name in clay_names:
        if "apollo" in name.lower() and "src:apollo" not in info:
            info.append("src:apollo")
        elif "hubspot" in name.lower() and "src:hubspot" not in info:
            info.append("src:hubspot")
        elif "salesnav" in name.lower() and "src:salesnav" not in info:
            info.append("src:salesnav")
        elif "builtwith" in name.lower() and "src:builtwith" not in info:
            info.append("src:builtwith")

    return list(set(info))

# Insert leads
inserted = 0
skipped = 0
errors = 0

for contact in all_contacts:
    email = contact.get("email")
    if not email:
        skipped += 1
        continue

    clay_names = contact_clay_map.get(contact["id"], [])
    segment_tag = assign_segment_tag(contact, clay_names)
    info_tags = build_info_tags(contact, clay_names)

    # Build tags array SQL
    tags_sql = "ARRAY['" + segment_tag + "']"
    info_tags_sql = "ARRAY[" + ",".join(f"'{t}'" for t in info_tags) + "]" if info_tags else "'{}'::text[]"

    # Escape values
    def e(v):
        if v is None:
            return "NULL"
        return "'" + str(v).replace("'", "''") + "'"

    extra = contact.get("extra_data")
    extra_sql = e(json.dumps(extra)) if extra and extra != {} else "'{}'::jsonb"

    insert_sql = f"""
    INSERT INTO leads (
        email, first_name, last_name, full_name, job_title,
        linkedin_profile_url, company_name, company_domain, company_website,
        company_linkedin_url, industry, monthly_visits, employee_count,
        email_verified, mx_provider, has_email_security_gateway, is_catchall,
        is_personal_email, tags, info_tags, extra_data
    ) VALUES (
        {e(email)}, {e(contact.get('first_name'))}, {e(contact.get('last_name'))},
        {e(contact.get('full_name'))}, {e(contact.get('job_title'))},
        {e(contact.get('linkedin_profile_url'))},
        {e(contact.get('company_name'))}, {e(contact.get('company_domain'))},
        {e(contact.get('company_website'))}, {e(contact.get('company_linkedin_url'))},
        {e(contact.get('industry'))},
        {contact.get('monthly_visits') or 'NULL'},
        {e(contact.get('employee_count'))},
        {e(contact.get('email_verified'))}, {e(contact.get('mx_provider'))},
        {e(contact.get('has_email_security_gateway'))}, {e(contact.get('is_catchall'))},
        {str(contact.get('is_personal_email', False)).lower() if contact.get('is_personal_email') is not None else 'NULL'},
        {tags_sql}, {info_tags_sql}, {extra_sql}
    ) ON CONFLICT (email) DO NOTHING
    """

    try:
        neon_sql(insert_sql)
        inserted += 1
        if inserted % 100 == 0:
            log(f"  Inserted {inserted} leads...")
    except Exception as ex:
        errors += 1
        if errors <= 3:
            log(f"  Error on {email}: {ex}")

log(f"Done! Inserted: {inserted}, Skipped (no email): {skipped}, Errors: {errors}")

# ============================================================
# STEP 6: VERIFY
# ============================================================
print("\n" + "="*60)
print("STEP 6: Verification")
print("="*60)

# Total leads
result = neon_sql("SELECT COUNT(*) as cnt FROM leads")
log(f"Total leads: {result['rows'][0]['cnt']}")

# Leads per segment tag
result = neon_sql("""
    SELECT unnest(tags) as tag, COUNT(*) as cnt
    FROM leads
    GROUP BY tag
    ORDER BY cnt DESC
""")
log("Leads per segment tag:")
for r in result["rows"]:
    log(f"  {r['cnt']:>6}  {r['tag']}")

# Info tags distribution
result = neon_sql("""
    SELECT unnest(info_tags) as tag, COUNT(*) as cnt
    FROM leads
    GROUP BY tag
    ORDER BY cnt DESC
    LIMIT 10
""")
log("Top info_tags:")
for r in result["rows"]:
    log(f"  {r['cnt']:>6}  {r['tag']}")

# Sample leads
result = neon_sql("""
    SELECT email, company_name, monthly_visits, tags, info_tags
    FROM leads
    ORDER BY monthly_visits DESC NULLS LAST
    LIMIT 5
""")
log("Top 5 leads by monthly visits:")
for r in result["rows"]:
    log(f"  {r['email']:>40} | {str(r.get('company_name','')):>25} | visits: {r.get('monthly_visits','?'):>10} | tags: {r['tags']}")

# Segments
result = neon_sql("SELECT segment_id, segment_tag, status FROM segments ORDER BY segment_id")
log("Segments:")
for r in result["rows"]:
    log(f"  #{r['segment_id']}: {r['segment_tag']} ({r['status']})")

# Client
result = neon_sql("SELECT client_id, client_name, approved FROM clients")
log(f"Client: {result['rows'][0]['client_name']} (id: {result['rows'][0]['client_id']}, approved: {result['rows'][0]['approved']})")

print("\n" + "="*60)
print("SETUP COMPLETE!")
print(f"Project: GTM-CC-Test (delicate-wave-68549342)")
print(f"Connection: postgresql://...@ep-wild-bonus-anpaxuk6.c-6.us-east-1.aws.neon.tech/neondb")
print("="*60 + "\n")
