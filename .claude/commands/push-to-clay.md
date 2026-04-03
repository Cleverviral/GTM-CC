# Push Leads to Clay Table

You are guiding the operator through pushing leads to a Clay table via webhook. Follow these steps IN ORDER.

## Prerequisites

If the operator hasn't run `/pull-leads` yet in this session, tell them:
> **You need to pull leads first.** Run `/pull-leads` to select your client, segment, and leads.

## Step 1: Get Webhook URL

Ask:
> **Paste the Clay webhook URL.**
> (It should look like: `https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-...`)

Validate:
- Must start with `https://api.clay.com/`
- Must contain `webhook`

If invalid, ask again.

## Step 2: Confirm Table Setup

Ask:
> **Is this a blank Clay table (not a template)?**
> Clay auto-creates columns from our JSON keys on blank tables.
> If you're using a template, column mapping may fail.

## Step 3: Build Payload

Use `scripts/db.py` to build the complete push payload. The push MUST include all standard fields.

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query, get_active_recipe, get_leads_with_outputs
from datetime import datetime

# Get client info
client = read_query("SELECT client_id, client_name FROM clients WHERE client_id = $1", [client_id])[0]

# Get active recipe for this segment
recipe = get_active_recipe(segment_id)

# Get leads with any existing outputs
leads = get_leads_with_outputs(segment_id, limit=batch_size)

# Generate batch_id
batch_id = f"{client_tag}_{segment_tag}_{datetime.now().strftime('%Y%m%d')}_001"
```

For each lead, build this **exact** JSON payload (41 fields):

```python
payload = {
    # Identity (7 fields)
    "lead_id": lead["lead_id"],
    "email": lead["email"],
    "first_name": lead["first_name"],
    "last_name": lead["last_name"],
    "full_name": lead["full_name"],
    "job_title": lead["job_title"],
    "linkedin_profile_url": lead["linkedin_profile_url"],

    # Company (5 fields)
    "company_name": lead["company_name"],
    "company_domain": lead["company_domain"],
    "company_website": lead["company_website"],
    "industry": lead["industry"],
    "employee_count": lead["employee_count"],

    # Client + Segment (5 fields)
    "client_id": str(client["client_id"]),
    "client_name": client["client_name"],
    "segment_id": segment_id,
    "segment_name": segment["segment_name"],
    "segment_tag": segment["segment_tag"],

    # Verification (5 fields)
    "email_verified": lead["email_verified"],
    "email_verified_at": str(lead["email_verified_at"] or ""),
    "is_catchall": lead["is_catchall"],
    "mx_provider": lead["mx_provider"],
    "has_email_security_gateway": lead.get("has_email_security_gateway", ""),

    # Enrichment (4 fields)
    "monthly_visits": lead["monthly_visits"],
    "lcp": lead["lcp"],
    "tti": lead["tti"],
    "aov": lead["aov"],

    # Recipe (3 fields)
    "recipe_id": recipe["recipe_id"] if recipe else None,
    "current_recipe_version": recipe["version"] if recipe else None,
    "batch_id": batch_id,

    # Existing outputs (12 fields — from latest email_outputs row if exists)
    "last_recipe_version": lead.get("recipe_version"),
    "existing_subject_line_1": lead.get("subject_line_1"),
    "existing_subject_line_2": lead.get("subject_line_2"),
    "existing_email_1_variant_a": lead.get("email_1_variant_a"),
    "existing_email_1_variant_b": lead.get("email_1_variant_b"),
    "existing_email_1_variant_c": lead.get("email_1_variant_c"),
    "existing_email_2_variant_a": lead.get("email_2_variant_a"),
    "existing_email_2_variant_b": lead.get("email_2_variant_b"),
    "existing_email_2_variant_c": lead.get("email_2_variant_c"),
    "existing_email_3_variant_a": lead.get("email_3_variant_a"),
    "existing_email_3_variant_b": lead.get("email_3_variant_b"),
    "existing_email_3_variant_c": lead.get("email_3_variant_c"),
}
```

## Step 4: Preview

Show the operator what will be pushed:
> **Push preview:**
> - Client: {client_name}
> - Segment: {segment_name} ({segment_tag})
> - Recipe: v{version} (recipe_id: {recipe_id})
> - Batch ID: {batch_id}
> - Total leads: {count}
> - Leads with existing emails: {count_with_outputs} (Clay will skip regeneration for these if recipe version unchanged)
> - Leads needing generation: {count_without_outputs}
>
> **Fields per lead: 41** (identity, company, segment, verification, enrichment, recipe, existing outputs)

Show the first lead's full payload as example.

## Step 5: Test Push (1 Lead)

Ask:
> **Push 1 test lead first to verify it works?** (recommended)

If yes:
- POST the first lead as a single JSON object to the webhook URL
- Use `urllib.request` with `ssl.create_default_context()`
- Show the response status code
- Ask operator to check Clay table: "Go to your Clay table and verify all 41 columns appear correctly."
- **Specifically verify:** `client_id`, `client_name`, `segment_id`, `recipe_id`, `batch_id` columns exist (these were previously missing)

Wait for confirmation before proceeding.

## Step 6: Push All Leads

> **Pushing {count} leads to Clay (one at a time)...**

For each lead:
1. Build the 41-field JSON payload (Step 3 pattern)
2. POST to webhook URL
3. Show progress every 25 leads: "Pushed 25/{total}..."
4. Use 0.1s delay between requests

Handle errors gracefully:
- If a POST fails, log the lead email and error, continue with next lead
- At the end, show: "{success} pushed, {failed} failed"

## Step 7: Summary

> **Push complete!**
> - Leads pushed: {success}
> - Failed: {failed}
> - Batch ID: {batch_id}
> - Clay table: [check your Clay table]
>
> **Next steps for Kuldeep (Clay Operator):**
> 1. Verify all 41 columns appear in Clay table
> 2. Set up verification waterfall (Section B in clay-template-spec)
> 3. Add HTTP Column 1 — verification push-back to Neon
> 4. Add decision logic columns (needs_enrichment, needs_generation)
> 5. Add enrichment columns per recipe instructions
> 6. Add HTTP Column 2 — enrichment push-back to Neon
> 7. Add email generation columns per recipe instructions
> 8. Add HTTP Column 3 — email output push-back to Neon
> 9. Test with 3 leads → verify all HTTP columns fire correctly
> 10. Run the full table
>
> See `docs/clay-template-spec.md` for HTTP column SQL and full template reference.

## Important Notes

- ALWAYS push one lead at a time (single JSON object per POST, NOT arrays)
- Clay webhook does NOT accept arrays — it must be one object per request
- All 41 fields must be present in every payload — use `None`/`null` for missing values
- `client_id`, `segment_id`, `recipe_id`, `batch_id` are CRITICAL — HTTP Column 3 needs them
- Use a 0.1s delay between requests to avoid rate limiting
- If the push fails on ALL leads, the webhook URL might be wrong — ask to verify
