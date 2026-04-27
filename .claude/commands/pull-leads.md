# Pull Leads for a Client Segment

You are guiding the operator through pulling leads from the database. Follow these steps IN ORDER. Do not skip steps. Ask one question at a time and wait for the answer.

## Step 1: Identify Client

Run this query using `scripts/db.py`:
```python
import sys; sys.path.insert(0, 'scripts')
from db import get_clients
clients = get_clients()
```

Show the list as a numbered menu:
> **Which client are you pulling leads for?**
> 1. SpeedSize
> 2. Solara
> (etc.)

Wait for their answer.

## Step 2: Identify Segment

Run `get_segments(client_id)` for the chosen client.

Show segments as a numbered menu with lead counts:
> **Which segment?**
> 1. SpeedSize 1M+ Qualified (segment_id: 28) — 1,240 leads
> 2. SpeedSize 100K-1M (segment_id: 37) — 4,820 leads
> (etc. — pull live from the segments table; segment_ids in this DB live in the 28–54 range)

For each segment, also run `get_lead_count(segment_id)` to show how many leads are available.

Wait for their answer.

## Step 3: Filters (Optional)

Ask:
> **Any filters? (type 'none' to skip)**
> - Email verified only? (yes/no)
> - Minimum monthly visits? (e.g., 100000)
> - Specific country? (e.g., US)
> - Filter by Clay table lineage? (e.g., only leads where `clay_table_names` includes a specific table — useful for re-running just one Clay batch)
> - Filter by info_tags? (e.g., `ss-qualified-feb26`, `builtwith-data`)

Build the filters dict from their answers.

## Step 4: Preview

Run `get_leads_for_segment(segment_id, limit=5, filters=filters)` to get a sample.

Show:
- Total count matching filters
- Sample of 5 leads: email, company_name, job_title, monthly_visits, email_verified

> **Found {count} leads matching your criteria.**
> Here's a preview of 5:
> | Email | Company | Title | Visits | Verified |
> |-------|---------|-------|--------|----------|
> ...

## Step 5: Check for Existing Outputs

Run `get_active_recipe(segment_id)` to check if there's an active recipe.

If recipe exists, show:
> **Active recipe found:** v{version} (recipe_id: {id})
> {count} leads already have email outputs for this recipe.

This tells the operator how many will be PASS_THRU vs REGENERATE in Clay.

## Step 6: Confirm

> **Ready to pull {count} leads for {client_name} / {segment_name}?**
> - With existing outputs: {X} leads (will be PASS_THRU in Clay)
> - Without outputs: {Y} leads (will be REGENERATE in Clay)
>
> Type 'yes' to pull, or adjust filters.

## Step 7: Execute

Run `get_leads_with_outputs(segment_id)` to pull the full dataset.

Save the result for use with `/push-to-clay`. Show summary:
> **Pulled {count} leads.**
> Ready for `/push-to-clay` when you have the Clay webhook URL.

IMPORTANT: Store the pulled leads in a variable so `/push-to-clay` can reference them.
