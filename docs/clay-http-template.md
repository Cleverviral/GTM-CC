# Clay → Neon HTTP Template (Universal)

This doc has everything a Clay operator needs to wire up a new Clay table
to push data into the TAM + Recipe DB. **One template, every Clay table.**

## How it works in 30 seconds

Clay's HTTP column POSTs to Neon's built-in SQL-over-HTTP endpoint. The body
calls one Postgres function — `upsert_lead()` — which lives inside Neon
(see [`db/functions/upsert_lead.sql`](../db/functions/upsert_lead.sql)).
The function:

1. Upserts the lead in `leads` (insert if new, update if email exists,
   merging arrays + jsonb without overwriting non-null with null).
2. If the row also has generated email content (`email_*_variant_*` slots
   are non-empty), inserts a new row in `email_outputs` linked to that
   lead, segment, and recipe.

The same body works for every Clay table. Per-table differences are
hardcoded into 6 specific slots — the operator changes only those.

---

## Endpoint config

### URL

```
https://ep-wild-bonus-anpaxuk6.c-6.us-east-1.aws.neon.tech/sql
```

### Method

`POST`

### Headers

```
Content-Type: application/json
Neon-Connection-String: <connection string from .env>
```

The Neon-Connection-String value is in `.env` as
`NEON_TEST_CONNECTION_STRING`. Don't paste the literal value into shared
docs.

---

## Body — paste this verbatim

```json
{
  "query": "SELECT upsert_lead(p_email := $1, p_segment_ids := $2, p_first_name := NULLIF($3, ''), p_last_name := NULLIF($4, ''), p_full_name := NULLIF($5, ''), p_job_title := NULLIF($6, ''), p_linkedin_profile_url := NULLIF($7, ''), p_linkedin_username := NULLIF($8, ''), p_company_name := NULLIF($9, ''), p_company_domain := NULLIF($10, ''), p_company_website := NULLIF($11, ''), p_company_linkedin_url := NULLIF($12, ''), p_industry := NULLIF($13, ''), p_monthly_visits := NULLIF($14, '')::int, p_employee_count := NULLIF($15, ''), p_email_verified := NULLIF($16, ''), p_email_verified_at := NULLIF($17, ''), p_mx_provider := NULLIF($18, ''), p_has_email_security_gateway := NULLIF($19, ''), p_is_catchall := NULLIF($20, ''), p_is_personal_email := NULLIF($21, '')::boolean, p_city := NULLIF($22, ''), p_country := NULLIF($23, ''), p_info_tags := NULLIF($24, ''), p_extra_data_pairs := NULLIF($25, ''), p_recipe_id := NULLIF($26, '')::int, p_recipe_version := NULLIF($27, '')::int, p_selected_approach := NULLIF($28, ''), p_batch_id := NULLIF($29, ''), p_email_1_variant_a := NULLIF($30, ''), p_email_1_variant_b := NULLIF($31, ''), p_email_2_variant_a := NULLIF($32, ''), p_email_2_variant_b := NULLIF($33, ''), p_email_3_variant_a := NULLIF($34, ''), p_email_3_variant_b := NULLIF($35, ''), p_company_summary := NULLIF($36, ''), p_personalizations_pairs := NULLIF($37, ''))",
  "params": [
    "{{Email}}",
    "<SEGMENT_ID>",
    "{{First Name}}",
    "{{Last Name}}",
    "{{Full Name}}",
    "{{Title}}",
    "{{Personal LinkedIn URL}}",
    "{{LinkedIn Username}}",
    "{{Company Name}}",
    "{{Company Domain}}",
    "{{Company Website}}",
    "{{Company LinkedIn URL}}",
    "{{Industry}}",
    "{{Monthly Visits}}",
    "{{Employee Count}}",
    "{{Email Verified}}",
    "{{Email Verified At}}",
    "{{MX Provider}}",
    "{{Has ESG}}",
    "{{Is Catchall}}",
    "{{Is Personal Email}}",
    "{{City}}",
    "{{Country}}",
    "<INFO_TAGS>",
    "<EXTRA_DATA_BUILDER>",
    "<RECIPE_ID_OR_EMPTY>",
    "<RECIPE_VERSION_OR_EMPTY>",
    "{{Selected Approach}}",
    "{{Batch ID}}",
    "{{Email 1 Variant A}}",
    "{{Email 1 Variant B}}",
    "{{Email 2 Variant A}}",
    "{{Email 2 Variant B}}",
    "{{Email 3 Variant A}}",
    "{{Email 3 Variant B}}",
    "{{Company Summary}}",
    "<PERSONALIZATIONS_BUILDER_OR_EMPTY>"
  ]
}
```

---

## What the operator changes per Clay table

Six slots are placeholders (everything in `<...>`). Replace each with a
literal string for that table:

| Slot | Placeholder | What to put | Example |
|---:|---|---|---|
| 2 | `<SEGMENT_ID>` | The segment_id (or comma-separated multi) this Clay table pushes into. Required. | `"54"` (test segment) or `"28,37"` (multi) |
| 24 | `<INFO_TAGS>` | A label tagging which Clay table this came from. Comma-separated for multiple. | `"Gambling Apollo Table, 2026-04-23"` |
| 25 | `<EXTRA_DATA_BUILDER>` | Pipe/semicolon recipe building extra_data jsonb from Clay columns. NOT JSON. | `"product_category|{{Product Category}};aov|{{AOV}}"` or `""` if none |
| 26 | `<RECIPE_ID_OR_EMPTY>` | recipe_id of the active recipe for this segment (only when generating emails). | `"51"` or `""` for enrichment-only |
| 27 | `<RECIPE_VERSION_OR_EMPTY>` | Version of that recipe. | `"1"` or `""` for enrichment-only |
| 37 | `<PERSONALIZATIONS_BUILDER_OR_EMPTY>` | Same pipe format as extra_data, building personalizations jsonb for email_outputs. | `"first_line|{{First Line}};research_report|{{Research Report}}"` or `""` |

The remaining 31 slots are `{{Clay Variable}}` placeholders. Clay's
"Apply template" UI will show each as a dropdown — pick the matching Clay
column. If the Clay table doesn't have that column, leave the dropdown
unmapped and Clay will pass an empty string (the function treats it as
NULL).

---

## Required vs optional

- **Required** (function errors if missing): `Email`, `<SEGMENT_ID>`
- **Optional**: everything else

Empty strings, NULLs, and Clay's `CLAYFORMATVALUE(...)` empty-format
placeholders are all normalized to NULL by the `clay_clean()` helper
inside the function. No row will fail because of empty data — only because
of bad data (e.g. non-int in segment_id, non-existent segment_id, etc.).

---

## What the function returns

Per row, Clay's response cell will show:

```json
[{"upsert_lead": {
    "lead_id": 216125,
    "lead_action": "inserted",
    "segment_ids_applied": [54],
    "output_id": 14
}}]
```

| Field | Meaning |
|---|---|
| `lead_id` | Neon's lead PK. Same lead_id on subsequent calls for the same email. |
| `lead_action` | `"inserted"` (new lead) or `"updated"` (lead existed, fields merged). |
| `segment_ids_applied` | The full int array sent into the upsert (deduped, sorted). |
| `output_id` | `null` if no email content was sent; otherwise the new email_outputs PK. |

---

## Format reference

### `<SEGMENT_ID>` — slot 2

- Single: `"54"`
- Multiple: `"54,28,37"` (comma-separated, whitespace OK)
- The first segment in the list is "primary" — used as `email_outputs.segment_id` when generating emails.
- Function rejects unknown segment_ids with a clear error.

### `<INFO_TAGS>` — slot 24

- Single tag: `"Gambling Apollo Table"`
- Multiple tags: `"Gambling Apollo Table, 2026-04-23, q2-rerun"`
- Stored in `leads.info_tags[]` (deduped + merged with any existing tags on the lead).

### `<EXTRA_DATA_BUILDER>` — slot 25

A pipe/semicolon recipe — **not JSON**.

Format: `"key1|{{Clay Column 1}};key2|{{Clay Column 2}};key3|{{Clay Column 3}}"`

Each pair is separated by `;`. Within a pair, key and value are separated by `|`.

Example for a Clay table that has Product Category, AOV, and CRUX LCP P75:

```
product_category|{{Product Category}};aov|{{AOV}};crux_lcp_p75|{{CRUX LCP P75}}
```

Per row, Clay substitutes `{{...}}` with that row's column value. The
function parses the resulting string into jsonb and merges it into
`leads.extra_data`. Empty values and `CLAYFORMATVALUE(...)` placeholders
are filtered out automatically.

### `<RECIPE_ID_OR_EMPTY>` — slot 26

The recipe_id of the active recipe for the primary segment. Look it up:

```sql
SELECT recipe_id, version, clay_template_name, clay_template_link
FROM recipes
WHERE segment_id = <PRIMARY_SEGMENT> AND status = 'active';
```

For test segment 54 the placeholder recipe is `recipe_id = 51`.

If this Clay table is enrichment-only (not generating emails), put `""`.
The function will skip the email_outputs insert.

### `<RECIPE_VERSION_OR_EMPTY>` — slot 27

The version number of that recipe. Currently most recipes are at version 1.

If enrichment-only, `""`. If generating emails, the version that matches
the recipe_id from slot 26.

### `<PERSONALIZATIONS_BUILDER_OR_EMPTY>` — slot 37

Same format as `<EXTRA_DATA_BUILDER>`. Recipe for building the
`email_outputs.personalizations` jsonb from Clay columns.

Example for a Clay table with First Line and Research Report columns:

```
first_line|{{First Line}};research_report|{{Research Report}}
```

If enrichment-only or no personalizations to capture, `""`.

---

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Stray `e` after a `{{Variable}}` in the body | Value gets concatenated: `true` becomes `truee` | Edit the body, delete the stray character |
| Slot 25/37 typed as JSON `{...}` | Function returns parse error | Use pipe/semicolon format, not JSON |
| `CLAYFORMATVALUE()` literally appearing in stored data | Was happening pre-fix; now `clay_clean()` strips them | If you see this in old rows, it predates the fix — clean with SQL |
| Wrong recipe_id for the segment | Function rejects with `p_recipe_id N does not match the primary segment` | Look up the active recipe with the SQL above |
| Segment doesn't exist in Neon | Function rejects with `These segment_ids do not exist: {N}` | Check the segments table; create the segment first |

---

## See also

- [`db/functions/upsert_lead.sql`](../db/functions/upsert_lead.sql) — the function itself
- [`db/functions/clay_clean.sql`](../db/functions/clay_clean.sql) — the helper that normalizes Clay placeholders
- [`db/README.md`](../db/README.md) — how to redeploy if you edit the function
