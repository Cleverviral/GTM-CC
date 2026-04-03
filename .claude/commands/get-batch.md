# Get a Ready Batch (Campaign Operator)

Guide the campaign operator through downloading a batch ready for sequencer upload.

## Step 1: Identify Client + Segment

Use `get_clients()` and `get_segments(client_id)` to let the operator choose.

> **Which client?** (numbered list)
> **Which segment?** (numbered list)

## Step 2: Show Available Batches

Query for batches that have email outputs:
```python
from db import get_batches
batches = get_batches(segment_id)
```

Show:
> **Available batches for {client_name} / {segment_name}:**
> | # | Batch ID | Leads | Recipe v | Date |
> |---|----------|-------|----------|------|
> ...

If no batches exist, say:
> No batches ready yet. Check with the Clay operator (Kuldeep).

## Step 3: Preview Batch

For the chosen batch, show:
- Lead count
- Email verified count (only verified leads go to sequencer)
- 3 sample rows: email, company, subject_line_1

## Step 4: Generate CSV

Export with these exact columns (sequencer format):
```
email, first_name, last_name, company_name, job_title,
subject_line_1, subject_line_2,
email_1_variant_a, email_1_variant_b, email_1_variant_c,
email_2_variant_a, email_2_variant_b, email_2_variant_c,
email_3_variant_a, email_3_variant_b, email_3_variant_c,
segment_id, recipe_id, recipe_version, selected_approach
```

Save to: `exports/{client_name}-{segment_name}-batch-{date}.csv`

> **Batch exported!**
> - File: `{filepath}`
> - Leads: {count} (verified only)
> - Recipe: v{version}
> - Custom fields included: segment_id, recipe_id, recipe_version, selected_approach
>
> Upload this to your sequencer (Smartlead / Instantly).
> The custom fields enable performance tracking by segment x recipe x approach.

## Important
- ONLY include email_verified = 'true' or 'valid' leads
- ALWAYS include the 4 custom fields for tracking
- This is a READ-ONLY operation — nothing is modified in the database
