# Push Leads to Clay Table

You are guiding the operator through pushing leads to a Clay table via webhook. Follow these steps IN ORDER.

## Prerequisites

If the operator hasn't run `/pull-leads` yet in this session, tell them:
> **You need to pull leads first.** Run `/pull-leads` to select your client, segment, and leads.

## Step 1: Show Recipe Info

Before anything else, pull the active recipe for this segment and display:

```python
recipe = read_query("""
    SELECT recipe_id, version, clay_template_name, clay_instructions
    FROM recipes
    WHERE client_id = $1 AND segment_id = $2 AND status = 'active'
    LIMIT 1
""", [str(client_id), segment_id])[0]
```

Show the operator:
> **Recipe Info:**
> - Recipe ID: {recipe_id}, Version: {version}
> - Clay Template: {clay_template_name}
> - Instructions: {clay_instructions}
>
> **Set up your Clay table using the template above before proceeding.**

If `clay_template_name` is NULL, tell the operator:
> No saved Clay template found for this recipe. Ask the Strategist to set one up, or create a blank table.

Wait for confirmation that the table is ready.

## Step 2: Get Webhook URL

Ask:
> **Paste the Clay webhook URL from your table.**
> (It should look like: `https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-...`)

Validate:
- Must start with `https://api.clay.com/`
- Must contain `webhook`

If invalid, ask again.

## Step 3: Build Payload

Use `scripts/db.py` to build the complete push payload. The push MUST include ALL 38 fields listed below. DO NOT skip any field.

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query
from datetime import datetime

# Get client info
client = read_query("SELECT client_id, client_name FROM clients WHERE client_id = $1", [client_id])[0]

# Get segment info (includes leadlist_context + value_prop)
segment = read_query("SELECT segment_id, segment_name, segment_tag, leadlist_context, value_prop FROM segments WHERE segment_id = $1", [segment_id])[0]

# Get active recipe
recipe = read_query("SELECT recipe_id, version FROM recipes WHERE client_id = $1 AND segment_id = $2 AND status = 'active' LIMIT 1", [str(client['client_id']), segment_id])[0]

# Generate batch_id
batch_id = f"{segment['segment_tag']}_{datetime.now().strftime('%Y%m%d')}_001"

# Get leads
leads = read_query("""
    SELECT l.lead_id, l.email, l.first_name, l.last_name, l.full_name,
           l.job_title, l.linkedin_profile_url,
           l.company_name, l.company_domain, l.company_website, l.industry,
           l.employee_count, l.monthly_visits, l.lcp, l.tti, l.aov,
           l.email_verified, l.email_verified_at, l.is_catchall, l.mx_provider,
           l.has_email_security_gateway
    FROM leads l
    WHERE l.segment_ids @> ARRAY[$1]::int[]
    ORDER BY l.lead_id
    LIMIT 500
""", [segment_id])
```

For each lead, check for existing outputs and build this EXACT 38-field payload:

```python
# Check for existing email outputs (for rerun detection)
outputs = read_query("""
    SELECT recipe_version, email_1_variant_a, email_1_variant_b,
           email_2_variant_a, email_2_variant_b,
           email_3_variant_a, email_3_variant_b
    FROM email_outputs
    WHERE lead_id = $1
    ORDER BY created_at DESC LIMIT 1
""", [lead["lead_id"]])

latest = outputs[0] if outputs else {}

payload = {
    # ── Lead Identity (7 fields) ──
    "lead_id": lead["lead_id"],
    "email": lead["email"],
    "first_name": lead["first_name"],
    "last_name": lead["last_name"],
    "full_name": lead["full_name"],
    "job_title": lead["job_title"],
    "linkedin_profile_url": lead["linkedin_profile_url"],

    # ── Company (5 fields) ──
    "company_name": lead["company_name"],
    "company_domain": lead["company_domain"],
    "company_website": lead["company_website"],
    "industry": lead["industry"],
    "employee_count": lead["employee_count"],

    # ── Enrichment (4 fields) ──
    "monthly_visits": lead["monthly_visits"],
    "lcp": lead["lcp"],
    "tti": lead["tti"],
    "aov": lead["aov"],

    # ── Verification (5 fields) ──
    "email_verified": lead["email_verified"],
    "email_verified_at": str(lead["email_verified_at"]) if lead["email_verified_at"] else None,
    "is_catchall": lead["is_catchall"],
    "mx_provider": lead["mx_provider"],
    "has_email_security_gateway": lead["has_email_security_gateway"],

    # ── Client (2 fields) ──
    "client_id": str(client["client_id"]),
    "client_name": client["client_name"],

    # ── Segment (5 fields) ──
    "segment_id": segment["segment_id"],
    "segment_name": segment["segment_name"],
    "segment_tag": segment["segment_tag"],
    "lead_list_context": segment["leadlist_context"],
    "value_prop": segment["value_prop"],

    # ── Batch + Recipe (3 fields) ──
    "batch_id": batch_id,
    "recipe_id": recipe["recipe_id"],
    "current_recipe_version": recipe["version"],

    # ── Existing Outputs (7 fields — NULL for fresh leads) ──
    "last_recipe_version": latest.get("recipe_version"),
    "existing_email_1_variant_a": latest.get("email_1_variant_a"),
    "existing_email_1_variant_b": latest.get("email_1_variant_b"),
    "existing_email_2_variant_a": latest.get("email_2_variant_a"),
    "existing_email_2_variant_b": latest.get("email_2_variant_b"),
    "existing_email_3_variant_a": latest.get("email_3_variant_a"),
    "existing_email_3_variant_b": latest.get("email_3_variant_b"),
}
```

## MANDATORY: All 38 Fields Must Be Pushed

NEVER skip any field. Here is the complete checklist:

| Group | # | Field | Source |
|-------|---|-------|--------|
| Lead Identity | 1 | lead_id | leads |
| | 2 | email | leads |
| | 3 | first_name | leads |
| | 4 | last_name | leads |
| | 5 | full_name | leads |
| | 6 | job_title | leads |
| | 7 | linkedin_profile_url | leads |
| Company | 8 | company_name | leads |
| | 9 | company_domain | leads |
| | 10 | company_website | leads |
| | 11 | industry | leads |
| | 12 | employee_count | leads |
| Enrichment | 13 | monthly_visits | leads |
| | 14 | lcp | leads |
| | 15 | tti | leads |
| | 16 | aov | leads |
| Verification | 17 | email_verified | leads |
| | 18 | email_verified_at | leads |
| | 19 | is_catchall | leads |
| | 20 | mx_provider | leads |
| | 21 | has_email_security_gateway | leads |
| Client | 22 | client_id | clients |
| | 23 | client_name | clients |
| Segment | 24 | segment_id | segments |
| | 25 | segment_name | segments |
| | 26 | segment_tag | segments |
| | 27 | lead_list_context | segments.leadlist_context |
| | 28 | value_prop | segments.value_prop |
| Batch + Recipe | 29 | batch_id | generated |
| | 30 | recipe_id | recipes |
| | 31 | current_recipe_version | recipes.version |
| Existing Outputs | 32 | last_recipe_version | email_outputs (latest) |
| | 33 | existing_email_1_variant_a | email_outputs (latest) |
| | 34 | existing_email_1_variant_b | email_outputs (latest) |
| | 35 | existing_email_2_variant_a | email_outputs (latest) |
| | 36 | existing_email_2_variant_b | email_outputs (latest) |
| | 37 | existing_email_3_variant_a | email_outputs (latest) |
| | 38 | existing_email_3_variant_b | email_outputs (latest) |

Fields 32-38 will be NULL for fresh leads. For reruns (leads with existing outputs), they will contain the previous email output data.

## Step 4: Preview

Show the operator what will be pushed:
> **Push preview:**
> - Client: {client_name}
> - Segment: {segment_name} ({segment_tag})
> - Recipe: v{version} (recipe_id: {recipe_id})
> - Batch ID: {batch_id}
> - Total leads: {count}
> - Leads with existing emails: {count_with_outputs}
> - Leads needing generation: {count_without_outputs}
>
> **Fields per lead: 38** (identity, company, enrichment, verification, client, segment, recipe, existing outputs)

Show the first lead's full payload as example.

## Step 5: Test Push (1 Lead)

Ask:
> **Push 1 test lead first to verify it works?** (recommended)

If yes:
- POST the first lead as a single JSON object to the webhook URL
- Use `urllib.request` with `ssl.create_default_context()`
- Show the response status code
- Ask operator to check Clay table: "Go to your Clay table and verify all 38 columns appear correctly."
- Specifically verify: `client_id`, `value_prop`, `lead_list_context`, `has_email_security_gateway`, all 6 `existing_email_*` columns

Wait for confirmation before proceeding.

## Step 6: Push All Leads

> **Pushing {count} leads to Clay (one at a time)...**

For each lead:
1. Build the 38-field JSON payload (Step 3 pattern)
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
> 1. Verify all 38 columns appear in Clay table
> 2. Set up verification waterfall
> 3. Add HTTP Column 1 — verification push-back to Neon
> 4. Add enrichment columns per recipe instructions
> 5. Add HTTP Column 2 — enrichment push-back to Neon
> 6. Add email generation columns per recipe (use saved Clay template)
> 7. Add HTTP Column 3 — email output push-back to Neon
> 8. Test with 5 leads — verify all HTTP columns fire correctly
> 9. Run the full table

## Important Notes

- ALWAYS push one lead at a time (single JSON object per POST, NOT arrays)
- Clay webhook does NOT accept arrays — it must be one object per request
- ALL 38 fields must be present in every payload — use None/null for missing values
- value_prop comes from clients table, lead_list_context from segments table
- Approaches are NOT pushed — they live in the saved Clay template
- `client_id`, `segment_id`, `recipe_id`, `batch_id` are CRITICAL — HTTP Column 3 needs them
- Use a 0.1s delay between requests to avoid rate limiting
- If the push fails on ALL leads, the webhook URL might be wrong — ask to verify
