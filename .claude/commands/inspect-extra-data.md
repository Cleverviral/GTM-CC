# Inspect Extra Data

Show all unique keys stored in leads.extra_data for a client/segment. Helps operators understand what enrichment data exists before setting up Clay tables or HTTP push-back queries.

Available to all roles (read-only).

## Step 1: Identify Client + Segment

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query

clients = read_query("SELECT client_id, client_name FROM clients WHERE client_status = 'active' LIMIT 50")
```

Show numbered list. After client selection:

```python
segments = read_query("SELECT segment_id, segment_name, segment_tag FROM segments WHERE client_id = $1 LIMIT 50", [str(client_id)])
```

Ask:
> **Which segment?** (or type "all" to see extra_data across all segments for this client)

## Step 2: Pull Extra Data Summary

### For a specific segment:
```sql
SELECT
    key,
    COUNT(*) as lead_count,
    COUNT(CASE WHEN value IS NOT NULL AND value::text != 'null' AND value::text != '' THEN 1 END) as non_empty_count
FROM leads,
    jsonb_each_text(COALESCE(extra_data, '{}'::jsonb)) AS kv(key, value)
WHERE $1 = ANY(segment_ids)
GROUP BY key
ORDER BY lead_count DESC
LIMIT 50
```

### For all segments:
```sql
SELECT
    key,
    COUNT(*) as lead_count,
    COUNT(CASE WHEN value IS NOT NULL AND value::text != 'null' AND value::text != '' THEN 1 END) as non_empty_count
FROM leads l
JOIN segments s ON s.segment_id = ANY(l.segment_ids)
WHERE s.client_id = $1
GROUP BY key
ORDER BY lead_count DESC
LIMIT 50
```

## Step 3: Display Results

Show as a clean table:

> **Extra Data Keys for {client_name} / {segment_name}:**
>
> | Key | Leads with Data | Fill Rate |
> |-----|----------------|-----------|
> | cdn_detected | 142 / 500 | 28% |
> | crux_lcp_p75 | 389 / 500 | 78% |
> | product_category | 500 / 500 | 100% |
> | poor_experience_pct | 389 / 500 | 78% |
>
> **Total leads in segment: {total}**
> **Total unique extra_data keys: {key_count}**

## Step 4: Drill Down (Optional)

Ask:
> **What would you like to do?**
> 1. **Sample values** — show 5 example values for a specific key
> 2. **Value distribution** — show unique values and counts for a key
> 3. **Find leads missing a key** — show leads where a specific key is empty
> 4. **Done**

### For sample values:
```sql
SELECT lead_id, email, company_name, extra_data->>$2 as value
FROM leads
WHERE $1 = ANY(segment_ids) AND extra_data ? $2
ORDER BY lead_id
LIMIT 5
```

### For value distribution:
```sql
SELECT extra_data->>$2 as value, COUNT(*) as count
FROM leads
WHERE $1 = ANY(segment_ids) AND extra_data ? $2
GROUP BY extra_data->>$2
ORDER BY count DESC
LIMIT 20
```

### For missing key:
```sql
SELECT COUNT(*) as missing_count
FROM leads
WHERE $1 = ANY(segment_ids) AND (extra_data IS NULL OR NOT extra_data ? $2)
```

## Step 5: Related Lineage Columns (optional)

`clay_table_names` and `info_tags` are array columns on `leads` (NOT keys inside `extra_data`). If the operator wants the same fill-rate view for those, run:

```sql
SELECT unnest(clay_table_names) AS clay_table, COUNT(*) AS leads
FROM leads
WHERE $1 = ANY(segment_ids)
GROUP BY clay_table
ORDER BY leads DESC
LIMIT 25;

SELECT unnest(info_tags) AS info_tag, COUNT(*) AS leads
FROM leads
WHERE $1 = ANY(segment_ids)
GROUP BY info_tag
ORDER BY leads DESC
LIMIT 25;
```

`clay_table_names` records which Clay tables a lead has been pushed from (operational lineage). `info_tags` is everything else — legacy migration tags, qualification labels, etc. Both are merged via union, never overwritten.

## Important
- This is READ-ONLY — nothing is modified
- Useful before running `/generate-http-query` — shows what keys already exist
- Useful before `/push-to-clay` — shows what enrichment data is already populated
- If no extra_data exists for a segment, say: "No extra_data found. This segment's leads haven't been enriched yet via the upsert_lead push-back."
- `lcp`, `tti`, `aov` are NOT dedicated columns — they live as `extra_data` keys (e.g. `crux_lcp_p75`, `aov`).
- `clay_table_names` is a dedicated array column on `leads`, not an `extra_data` key.
