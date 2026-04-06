# Check Email Outputs

Show email output stats for any client/segment combination. Available to Copy Strategist and Campaign Operator.

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
SELECT COUNT(*) as total,
       COUNT(DISTINCT lead_id) as unique_leads,
       COUNT(DISTINCT recipe_version) as versions,
       MIN(created_at) as first_output,
       MAX(created_at) as latest_output
FROM email_outputs
WHERE client_id = $1 AND segment_id = $2
```

Display:
> **Email Outputs for {client_name} / {segment_name}:**
> - Total outputs: {total}
> - Unique leads: {unique_leads}
> - Recipe versions used: {versions}
> - Date range: {first} — {latest}

## Step 3: Breakdown Options

Ask:
> **What would you like to see?**
> 1. Breakdown by recipe version
> 2. Breakdown by selected approach
> 3. Sample emails (3 random outputs)
> 4. Search by lead email
> 5. Done

For sample emails, show: email address, company, first 100 chars of email_1_variant_a.

For search by email: WHERE lead_id = (SELECT lead_id FROM leads WHERE email ILIKE $1)

## Important
- This is READ-ONLY — nothing is modified
- If the operator asks to change anything, redirect to Copy Strategist
