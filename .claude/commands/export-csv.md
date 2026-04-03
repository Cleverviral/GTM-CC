# Export Leads + Emails as CSV

You are guiding the operator through exporting data as a CSV file for the campaign operator or for review.

## Step 1: Identify Client + Segment

Use `get_clients()` and `get_segments(client_id)` to let the operator choose.

> **Which client?** (numbered list)
> **Which segment?** (numbered list)

## Step 2: What to Export

Ask:
> **What do you want to export?**
> 1. **Full batch for campaign operator** — leads + email outputs + custom fields (for sequencer upload)
> 2. **Leads only** — just lead data, no email outputs
> 3. **Email outputs only** — for review or comparison

## Step 3: Filters

For option 1 (full batch):
- Ask: "Which batch_id?" (show recent batches using `get_batches(segment_id)`)
- Ask: "Verified leads only?" (default: yes)

For option 2 (leads only):
- Ask: "Any filters?" (verified status, visit range, etc.)

For option 3 (email outputs):
- Ask: "Which recipe version?" (show available versions)
- Ask: "Which batch?" (show recent batches)

## Step 4: Preview

Show 3 sample rows of what will be exported.

For a campaign operator batch, the CSV columns should be:
```
email, first_name, last_name, company_name, job_title,
subject_line_1, subject_line_2,
email_1_variant_a, email_1_variant_b, email_1_variant_c,
email_2_variant_a, email_2_variant_b, email_2_variant_c,
email_3_variant_a, email_3_variant_b, email_3_variant_c,
segment_id, recipe_id, recipe_version, selected_approach
```

The last 4 are custom fields for sequencer tracking.

## Step 5: Generate CSV

Use `export_to_csv(rows, filepath, columns)` from db.py.

Save to: `exports/{client_name}-{segment_name}-{date}.csv`
Create the exports/ directory if it doesn't exist.

> **Exported {count} rows to `{filepath}`**
> This file is ready to hand to the campaign operator.

## Important
- The 4 custom fields (segment_id, recipe_id, recipe_version, selected_approach) MUST be included for performance tracking
- Verify email_verified = 'true' or 'valid' before including in a campaign batch
- Never include HOLD or unverified leads in a campaign export
