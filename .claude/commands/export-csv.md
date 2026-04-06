# Export Leads + Emails as CSV

Guide the operator through exporting data as a CSV file.

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

## Step 2: What to Export

Ask:
> **What do you want to export?**
> 1. **Full batch for sequencer** — leads + email outputs + tracking fields
> 2. **Leads only** — just lead data, no email outputs
> 3. **Email outputs only** — for review or comparison

## Step 3: Filters

For option 1 (full batch):
- Ask: "Verified leads only?" (default: yes)
- Ask: "Which recipe version?" (show available versions)

For option 2 (leads only):
- Ask: "Any filters?" (verified status, visit range, etc.)

For option 3 (email outputs):
- Ask: "Which recipe version?" (show available versions)

## Step 4: Preview

Show 3 sample rows of what will be exported.

For a campaign batch, the CSV columns should be:
```
email, first_name, last_name, company_name, job_title,
email_1_variant_a, email_1_variant_b,
email_2_variant_a, email_2_variant_b,
email_3_variant_a, email_3_variant_b,
segment_id, recipe_id, recipe_version, selected_approach
```

The last 4 are custom fields for sequencer tracking.

## Step 5: Generate CSV

Save to: `exports/{client_name}-{segment_tag}-{date}.csv`
Create the exports/ directory if it doesn't exist.

> **Exported {count} rows to `{filepath}`**

## Important
- The 4 custom fields (segment_id, recipe_id, recipe_version, selected_approach) MUST be included
- Verify email_verified = 'true' or 'valid' before including in a campaign batch
- Never include unverified leads in a campaign export
