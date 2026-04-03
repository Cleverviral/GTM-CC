# Check Email Outputs (Campaign Operator)

Show the campaign operator email output stats for any client/segment combination.

## Step 1: Identify Client + Segment

Use `get_clients()` and `get_segments(client_id)` to let the operator choose.

## Step 2: Show Output Summary

Query:
```sql
SELECT COUNT(*) as total,
       COUNT(DISTINCT lead_id) as unique_leads,
       COUNT(DISTINCT batch_id) as batches,
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
> - Batches: {batches}
> - Recipe versions used: {versions}
> - Date range: {first} — {latest}

## Step 3: Breakdown Options

Ask:
> **What would you like to see?**
> 1. Breakdown by recipe version
> 2. Breakdown by selected approach
> 3. Breakdown by batch
> 4. Sample emails (3 random outputs)
> 5. Search by lead email
> 6. Done

Handle each option with the appropriate query.

For sample emails, show: email address, company, subject_line_1, first 100 chars of email_1_variant_a.

For search by email, query: WHERE lead_id = (SELECT lead_id FROM leads WHERE email ILIKE $1)

## Important
- This is READ-ONLY — nothing is modified
- If the operator asks to change anything, redirect them to the Clay operator or Strategist
