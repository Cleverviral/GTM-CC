"""
Backfill leads.clay_table_names from the legacy Supabase client_contacts table.

ONE-TIME SCRIPT — already run once on 2026-04-27 against the TAM + Recipe DB.
Kept in repo for reference and in case a re-run is needed (idempotent — uses
union-merge so re-running does not duplicate).

Reads /tmp/clay_table_backfill.json which is produced by the upstream Supabase
fetch step (see HANDOVER.md or ask Mayank for that script if you need to
regenerate the input file).

For each email -> [clay_table_name, ...] mapping, performs:
    UPDATE leads SET clay_table_names = union(existing, incoming) WHERE email = ?
batched in groups of 200 emails per UPDATE statement.
"""

import os, json, urllib.request, ssl, time, sys
sys.stdout.reconfigure(line_buffering=True)

env = {}
with open('/Users/mayankmittal/Desktop/GTM-CC/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.split('#')[0].strip()
conn_str = env['NEON_TEST_CONNECTION_STRING']
host = conn_str.split('@')[1].split('/')[0]

def neon(sql, params=None):
    body = {'query': sql}
    if params: body['params'] = params
    req = urllib.request.Request(f'https://{host}/sql', data=json.dumps(body).encode(), method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Neon-Connection-String', conn_str)
    try:
        return json.loads(urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30).read().decode())
    except urllib.error.HTTPError as e:
        print(f'ERR {e.code}: {e.read().decode()[:300]}'); raise

with open('/tmp/clay_table_backfill.json') as f:
    email_to_clay = json.load(f)

emails = sorted(email_to_clay.keys())
print(f'Backfilling {len(emails)} leads...')
BATCH = 200
total_updated = 0
t0 = time.time()
for bstart in range(0, len(emails), BATCH):
    batch = emails[bstart:bstart+BATCH]
    # Build VALUES rows: ($1, $2::text[]), ($3, $4::text[]), ...
    placeholders = []
    params = []
    for i, e in enumerate(batch):
        idx = i*2 + 1
        placeholders.append(f'(${idx}, ${idx+1}::text[])')
        params.append(e)
        params.append(email_to_clay[e])
    sql = f"""
        UPDATE leads l
        SET clay_table_names = ARRAY(
            SELECT DISTINCT t FROM unnest(COALESCE(l.clay_table_names, ARRAY[]::text[]) || v.tables) t WHERE t IS NOT NULL AND t <> ''
        )
        FROM (VALUES {','.join(placeholders)}) AS v(email, tables)
        WHERE l.email = v.email
    """
    r = neon(sql, params)
    total_updated += r.get('rowCount', 0)
    if bstart % 5000 == 0 or bstart + BATCH >= len(emails):
        print(f'  {bstart+len(batch)}/{len(emails)} processed, total rows updated: {total_updated} ({time.time()-t0:.0f}s)')

print(f'\n✅ Backfill done. {total_updated} leads updated in {time.time()-t0:.0f}s')

# Verify
r = neon("SELECT COUNT(*) AS c FROM leads WHERE clay_table_names IS NOT NULL AND array_length(clay_table_names, 1) > 0")
print(f'Leads with clay_table_names populated: {r["rows"][0]["c"]}')

# Distribution check
r = neon("""
    SELECT t AS clay_table_name, COUNT(*) AS leads
    FROM leads, unnest(clay_table_names) AS t
    GROUP BY t ORDER BY leads DESC LIMIT 10
""")
print('\nTop 10 clay tables by lead count:')
for row in r['rows']:
    print(f'  {row["leads"]:>6}  {row["clay_table_name"]}')
