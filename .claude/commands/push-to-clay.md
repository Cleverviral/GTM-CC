# Push Leads to Clay Table

You are guiding the operator through pushing leads to a Clay table via webhook. Follow these steps IN ORDER.

## Prerequisites

If the operator hasn't run `/pull-leads` yet in this session, tell them:
> **You need to pull leads first.** Run `/pull-leads` to select your client, segment, and leads.

## Step 1: Show Recipe Info

Before anything else, pull the active recipe for this segment and display:

```python
recipe = read_query("""
    SELECT recipe_id, version, clay_template_name, clay_template_link, recipe_notes
    FROM recipes
    WHERE client_id = $1 AND segment_id = $2 AND status = 'active'
    LIMIT 1
""", [str(client_id), segment_id])[0]
```

Show the operator:
> **Recipe Info:**
> - Recipe ID: {recipe_id}, Version: {version}
> - Clay Template: {clay_template_name}
> - Clay Template Link: {clay_template_link}
> - Notes: {recipe_notes}
>
> **Set up your Clay table using the template above before proceeding.**

If `clay_template_name` is NULL, tell the operator:
> No saved Clay template found for this recipe. Ask the Strategist to set one up, or create a blank table.

If `clay_template_name` is `"Refer to sample email repo"`, tell the operator:
> This recipe uses a Notion-based static approach (not a Clay template). See the sample email repo for the approach and set up the Clay table manually.

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

Use `scripts/db.py > build_clay_payload()` to build the complete push payload. Every core field listed below must be included, and every `leads.extra_data` key gets flattened to the top level.

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

# Get leads — pull everything; build_clay_payload flattens extra_data into the payload
leads = read_query("""
    SELECT l.lead_id, l.email, l.first_name, l.last_name, l.full_name,
           l.job_title, l.linkedin_profile_url, l.linkedin_username,
           l.company_name, l.company_domain, l.company_website, l.company_linkedin_url,
           l.industry, l.employee_count, l.monthly_visits,
           l.email_verified, l.email_verified_at, l.is_catchall, l.mx_provider,
           l.has_email_security_gateway, l.is_personal_email, l.city, l.country,
           l.extra_data, l.info_tags, l.segment_ids
    FROM leads l
    WHERE l.segment_ids @> ARRAY[$1]::int[]
    ORDER BY l.lead_id
    LIMIT 500
""", [segment_id])
```

**Note:** `lcp`, `tti`, `aov` are NOT dedicated columns — they live in `extra_data` and get flattened into the Clay payload automatically (see Step 3).

For each lead, check for existing outputs and build the payload:

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

# Use the built-in helper — it handles extra_data flattening automatically
from db import build_clay_payload
payload = build_clay_payload(lead, client, segment, recipe, batch_id)

# Attach existing outputs (NULL for fresh leads) — these are NOT in build_clay_payload
payload.update({
    "last_recipe_version": latest.get("recipe_version"),
    "existing_email_1_variant_a": latest.get("email_1_variant_a"),
    "existing_email_1_variant_b": latest.get("email_1_variant_b"),
    "existing_email_2_variant_a": latest.get("email_2_variant_a"),
    "existing_email_2_variant_b": latest.get("email_2_variant_b"),
    "existing_email_3_variant_a": latest.get("email_3_variant_a"),
    "existing_email_3_variant_b": latest.get("email_3_variant_b"),
})
```

`build_clay_payload()` produces:
- 28 core fields (identity, company, 1 enrichment, verification, client, segment, batch+recipe)
- All `leads.extra_data` keys flattened to top-level (each becomes its own Clay column)
- Plus the 7 existing-output fields we add above

Total: **35 core fields + N extra_data keys + 7 existing-output fields** — the final field count depends on how many keys the lead has in `extra_data`.

## MANDATORY: All Fields Must Be Pushed

Never skip any of the core fields below. Every `leads.extra_data` key flattens automatically via `build_clay_payload()`.

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
| Verification | 14 | email_verified | leads |
| | 15 | email_verified_at | leads |
| | 16 | is_catchall | leads |
| | 17 | mx_provider | leads |
| | 18 | has_email_security_gateway | leads |
| Client | 19 | client_id | clients |
| | 20 | client_name | clients |
| Segment | 21 | segment_id | segments |
| | 22 | segment_name | segments |
| | 23 | segment_tag | segments |
| | 24 | lead_list_context | segments.leadlist_context |
| | 25 | value_prop | segments.value_prop |
| Batch + Recipe | 26 | batch_id | generated |
| | 27 | recipe_id | recipes |
| | 28 | current_recipe_version | recipes.version |
| Existing Outputs | 29 | last_recipe_version | email_outputs (latest) |
| | 30 | existing_email_1_variant_a | email_outputs (latest) |
| | 31 | existing_email_1_variant_b | email_outputs (latest) |
| | 32 | existing_email_2_variant_a | email_outputs (latest) |
| | 33 | existing_email_2_variant_b | email_outputs (latest) |
| | 34 | existing_email_3_variant_a | email_outputs (latest) |
| | 35 | existing_email_3_variant_b | email_outputs (latest) |
| extra_data | N | Every `extra_data` key becomes its own Clay column | leads.extra_data |

Fields 29-35 are NULL for fresh leads. Fields 13 (monthly_visits) can be NULL — SpeedSize + some segments have mv gaps.

`lcp`, `tti`, `aov` are NOT dedicated payload fields — they flow through as extra_data keys (e.g. `crux_lcp_p75`, `aov`) if present on the lead.

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
> **Fields per lead:** 35 core fields + extra_data keys flattened (count varies by lead depending on enrichment history)

Show the first lead's full payload as example.

## Step 5: Test Push (1 Lead)

Ask:
> **Push 1 test lead first to verify it works?** (recommended)

If yes:
- POST the first lead as a single JSON object to the webhook URL
- Use `urllib.request` with `ssl.create_default_context()`
- Show the response status code
- Ask operator to check Clay table: "Go to your Clay table and verify all core columns + extra_data columns appear correctly."
- Specifically verify: `client_id`, `value_prop`, `lead_list_context`, `has_email_security_gateway`, all 6 `existing_email_*` columns, and any extra_data keys the recipe expects (e.g. `aov`, `crux_lcp_p75`, `product_category`)

Wait for confirmation before proceeding.

## Step 6: Push All Leads

> **Pushing {count} leads to Clay (one at a time)...**

For each lead:
1. Build the JSON payload via `build_clay_payload()` (Step 3 pattern)
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
> **Next steps for the Clay Operator:**
> 1. Verify all core + extra_data columns appear in Clay table
> 2. Set up verification waterfall
> 3. Add HTTP Column 1 — verification push-back to Neon
> 4. Add enrichment columns per recipe instructions
> 5. Add HTTP Column 2 — enrichment push-back to Neon (writes into `leads.extra_data` + verification fields)
> 6. Add email generation columns per recipe (use saved Clay template)
> 7. Add HTTP Column 3 — email output push-back to Neon (INSERTs into `email_outputs`)
> 8. Test with 5 leads — verify all HTTP columns fire correctly
> 9. Run the full table

## Important Notes

- ALWAYS push one lead at a time (single JSON object per POST, NOT arrays)
- Clay webhook does NOT accept arrays — it must be one object per request
- All 35 core fields must be present in every payload — use None/null for missing values
- value_prop and lead_list_context both come from the segments table (NOT clients)
- Approaches are NOT pushed — they live in the saved Clay template
- `client_id`, `segment_id`, `recipe_id`, `batch_id` are CRITICAL — HTTP Column 3 needs them
- Use a 0.1s delay between requests to avoid rate limiting
- If the push fails on ALL leads, the webhook URL might be wrong — ask to verify
