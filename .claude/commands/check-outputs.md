# Check Email Outputs

Show email output stats for any client/segment combination. Available to **Copy Strategist** and **Campaign Operator**.

This is read-only. The Campaign Operator should never be able to modify anything from this command.

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

## Step 2: Show Output Summary

```sql
SELECT COUNT(*) AS total,
       COUNT(DISTINCT lead_id) AS unique_leads,
       COUNT(DISTINCT recipe_version) AS versions,
       COUNT(DISTINCT batch_id) AS batches,
       MIN(created_at) AS first_output,
       MAX(created_at) AS latest_output
FROM email_outputs
WHERE client_id = $1 AND segment_id = $2
```

Display:
> **Email Outputs for {client_name} / {segment_name}:**
> - Total outputs: {total}
> - Unique leads: {unique_leads}
> - Recipe versions used: {versions}
> - Batches: {batches}
> - Date range: {first} — {latest}

## Step 3: Breakdown Options

Ask:
> **What would you like to see?**
> 1. Breakdown by recipe version
> 2. Breakdown by selected approach
> 3. Breakdown by Clay table lineage (clay_table_names on each lead)
> 4. Sample emails (3 random outputs, with personalizations)
> 5. Search by lead email
> 6. Done

### 1. Breakdown by recipe version
```sql
SELECT recipe_version, COUNT(*) AS rows, COUNT(DISTINCT lead_id) AS unique_leads
FROM email_outputs
WHERE client_id = $1 AND segment_id = $2
GROUP BY recipe_version
ORDER BY recipe_version DESC
```

### 2. Breakdown by selected approach
```sql
SELECT selected_approach, COUNT(*) AS rows
FROM email_outputs
WHERE client_id = $1 AND segment_id = $2 AND selected_approach IS NOT NULL
GROUP BY selected_approach
ORDER BY rows DESC
```

### 3. Breakdown by Clay table lineage
Joins to `leads.clay_table_names` to show which Clay tables produced this segment's outputs.
```sql
SELECT unnest(l.clay_table_names) AS clay_table, COUNT(DISTINCT eo.output_id) AS outputs
FROM email_outputs eo
JOIN leads l ON l.lead_id = eo.lead_id
WHERE eo.client_id = $1 AND eo.segment_id = $2
GROUP BY clay_table
ORDER BY outputs DESC
LIMIT 25
```

### 4. Sample emails (with personalizations)
Pull 3 random outputs and show the structured personalizations alongside the email body so the Campaign Operator can see how the copy was crafted.
```sql
SELECT eo.output_id, l.email, l.company_name,
       eo.selected_approach,
       LEFT(eo.email_1_variant_a, 200) AS email_1_preview,
       eo.personalizations
FROM email_outputs eo
JOIN leads l ON l.lead_id = eo.lead_id
WHERE eo.client_id = $1 AND eo.segment_id = $2
ORDER BY random()
LIMIT 3
```

Display each: email, company, selected_approach, first 200 chars of email_1_variant_a, then `personalizations` keys + values as a table (e.g. `first_line`, `research_report`, `relevant_proof_brand`).

### 5. Search by lead email
```sql
SELECT eo.output_id, eo.recipe_version, eo.selected_approach,
       eo.batch_id, eo.created_at,
       LEFT(eo.email_1_variant_a, 200) AS email_1_preview,
       LEFT(eo.email_2_variant_a, 200) AS email_2_preview,
       LEFT(eo.email_3_variant_a, 200) AS email_3_preview,
       eo.personalizations
FROM email_outputs eo
JOIN leads l ON l.lead_id = eo.lead_id
WHERE l.email ILIKE $1
ORDER BY eo.created_at DESC
LIMIT 10
```

## Important
- This is READ-ONLY — nothing is modified.
- If the operator asks to change anything, redirect to Copy Strategist.
- `personalizations` is a jsonb column on `email_outputs` — keys vary by recipe (commonly `first_line`, `research_report`, `relevant_proof_brand`, `company_summary_bullets`, etc.). Show as a key/value table, not raw JSON.
- `clay_table_names` lives on `leads`, not `email_outputs` — join through `lead_id` to surface lineage. Same lead can have multiple Clay tables in its lineage.
- Never run `UPDATE` or `DELETE` from this command. Campaign Operator role enforces this.
