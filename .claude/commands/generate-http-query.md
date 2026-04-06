# Generate HTTP Push-Back Query

Generate the exact HTTP body (query + params) for Clay to push data back to Neon. Available to Copy Strategist and Clay Operator.

## Step 1: What type of push-back?

Ask:
> **What are you pushing back from Clay?**
> 1. **Enrichment data** — new data points into leads.extra_data (HTTP Col 2)
> 2. **Email outputs** — generated emails into email_outputs table (HTTP Col 3)

## Option 1: Enrichment Data (HTTP Col 2)

Ask:
> **List the Clay column names you want to push back to the DB.**
> Example: "CDN Detected, LCP P75, Poor Experience Percent, Product Category"

For each data point provided, build the query. The pattern is:
- `lcp` gets its own SET clause (it's a dedicated DB column): `lcp = CASE WHEN $N != '' THEN $N::float ELSE lcp END`
- Everything else goes into `extra_data` as a JSONB key using: `'key_name', NULLIF($N, '')`
- `lead_id` is ALWAYS the last param

### Building the query:

1. For each data point, create a snake_case key name (e.g., "CDN Detected" → "cdn_detected")
2. Check if it maps to a dedicated leads column (lcp, tti, aov, monthly_visits, email_verified, is_catchall, mx_provider, city, country)
3. If dedicated column: add a SET clause
4. If not: add to jsonb_build_object

### Output format:

Show the complete JSON body ready to copy-paste into Clay:

```json
{
    "query": "UPDATE leads SET [dedicated columns if any], extra_data = COALESCE(extra_data, '{}'::jsonb) || jsonb_strip_nulls(jsonb_build_object([key-value pairs])) WHERE lead_id = $N",
    "params": [
        "SLOT 1 → type / and pick your [Column Name] column",
        "SLOT 2 → type / and pick your [Column Name] column",
        "SLOT N → type / and pick your Lead Id column"
    ]
}
```

Then show the mapping table:

| Slot | $param | What it stores | Clay column to pick |
|------|--------|---------------|-------------------|
| 1 | $1 | ... | /Column Name |
| 2 | $2 | ... | /Column Name |
| N | $N | Identifies which lead | /Lead Id |

Remind the operator:
> **Important:**
> - The `"query"` part stays exactly as-is — do NOT edit it
> - In the `"params"` array, type `/` in each slot and pick the Clay column from the dropdown
> - `Lead Id` must ALWAYS be the last param
> - Empty Clay values are automatically skipped (won't overwrite existing data)
> - To add a new data point later, tell me and I'll regenerate the query

## Option 2: Email Outputs (HTTP Col 3)

This is mostly standard. Show the query:

```json
{
    "query": "INSERT INTO email_outputs (lead_id, client_id, segment_id, recipe_id, recipe_version, selected_approach, email_1_variant_a, email_2_variant_a, email_3_variant_a) VALUES ($1, $2::uuid, $3, $4, $5, $6, $7, $8, $9)",
    "params": [
        "SLOT 1 → type / and pick Lead Id",
        "SLOT 2 → type / and pick Client Id",
        "SLOT 3 → type / and pick Segment Id",
        "SLOT 4 → type / and pick Recipe Id",
        "SLOT 5 → type / and pick Current Recipe Version",
        "SLOT 6 → type / and pick Selected Approach Name",
        "SLOT 7 → type / and pick Cleaned Email - 1",
        "SLOT 8 → type / and pick Cleaned Email - 2",
        "SLOT 9 → type / and pick Cleaned Email - 3"
    ]
}
```

Then show the mapping table:

| Slot | $param | DB column | Clay column to pick |
|------|--------|-----------|-------------------|
| 1 | $1 | lead_id | /Lead Id |
| 2 | $2 | client_id | /Client Id |
| 3 | $3 | segment_id | /Segment Id |
| 4 | $4 | recipe_id | /Recipe Id |
| 5 | $5 | recipe_version | /Current Recipe Version |
| 6 | $6 | selected_approach | /Selected Approach Name |
| 7 | $7 | email_1_variant_a | /Cleaned Email - 1 |
| 8 | $8 | email_2_variant_a | /Cleaned Email - 2 |
| 9 | $9 | email_3_variant_a | /Cleaned Email - 3 |

Ask:
> **Do your Clay column names match the ones above?**
> If not, tell me the actual column names and I'll update the mapping.

## Important
- NEVER include connection string or credentials in the output — operator pastes those separately in Clay's header config
- Lead Id is ALWAYS the identifier — if it's missing from the Clay table, the push-back will fail
- For enrichment: empty Clay values are safely ignored (NULLIF + jsonb_strip_nulls pattern)
- For email outputs: each run creates a NEW row (INSERT, not UPDATE) — history is preserved
