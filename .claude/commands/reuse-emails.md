# Reuse Emails for Bad Infrastructure (Campaign Operator)

When a campaign has bad infrastructure (0% reply rate = domain/IP issues), the campaign operator needs the SAME emails on fresh sending infrastructure. No need to go through Clay again.

## Step 1: Explain What's Happening

> **Bad infrastructure scenario:**
> The campaign isn't performing because of sending infrastructure issues (bad domains, burned IPs).
> We'll pull the exact same emails from the database and you can upload them to a new sequencer campaign with fresh domains.
> **Zero Clay cost. Zero regeneration.**

## Step 2: Identify the Original Batch

> **Which client?** (numbered list from `get_clients()`)
> **Which segment?** (numbered list from `get_segments(client_id)`)
> **Which batch had the bad infra?** (show recent batches from `get_batches(segment_id)`)

## Step 3: Pull Original Emails

Query the exact same email outputs from the original batch:
```sql
SELECT l.email, l.first_name, l.last_name, l.company_name, l.job_title,
       eo.subject_line_1, eo.subject_line_2,
       eo.email_1_variant_a, eo.email_1_variant_b, eo.email_1_variant_c,
       eo.email_2_variant_a, eo.email_2_variant_b, eo.email_2_variant_c,
       eo.email_3_variant_a, eo.email_3_variant_b, eo.email_3_variant_c,
       eo.selected_approach, eo.recipe_version, eo.batch_id as original_batch_id,
       eo.segment_id, eo.recipe_id
FROM email_outputs eo
JOIN leads l ON l.lead_id = eo.lead_id
WHERE eo.batch_id = $1
```

## Step 4: Preview + Export

Show count and 3 sample rows.

> **Found {count} emails from original batch.**
> These are the exact same emails — just upload to a new sequencer campaign with fresh infrastructure.

Export CSV with same format as `/get-batch`.
Save to: `exports/{client_name}-{segment_name}-reuse-{date}.csv`

> **Exported! Upload to your new sequencer campaign.**
> Original batch: {original_batch_id}
> Leads: {count}
> No Clay processing needed.
