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

**35 slots, zero type casts.** `linkedin_username`, `company_domain`, `is_personal_email` are NOT in the body — the function auto-derives them. That's 3 fewer columns for the operator to map per Clay table.

**Slot 23 is `p_clay_table_names`** — a dedicated array column on `leads` that records which Clay tables a lead has been pushed from (e.g. `"TryNow Beauty Apollo Set 1, TryNow Q2 Expansion"`). Same merge rules as `info_tags` — incoming empty leaves existing untouched; incoming with values does a union merge.

**Why zero casts:** every parameter is text in the function signature, parsed internally. So Clay can send `CLAYFORMATVALUE()`, `10.2K`, empty strings, or other garbage in any slot — the function normalizes safely. Bad values become NULL, the row still succeeds. There's nothing in the body that can fail at the type-cast layer.

```json
{
  "query": "SELECT upsert_lead(p_email := $1, p_segment_ids := $2, p_first_name := NULLIF($3, ''), p_last_name := NULLIF($4, ''), p_full_name := NULLIF($5, ''), p_job_title := NULLIF($6, ''), p_linkedin_profile_url := NULLIF($7, ''), p_company_name := NULLIF($8, ''), p_company_website := NULLIF($9, ''), p_company_linkedin_url := NULLIF($10, ''), p_industry := NULLIF($11, ''), p_monthly_visits := NULLIF($12, ''), p_employee_count := NULLIF($13, ''), p_email_verified := NULLIF($14, ''), p_email_verified_at := NULLIF($15, ''), p_mx_provider := NULLIF($16, ''), p_has_email_security_gateway := NULLIF($17, ''), p_is_catchall := NULLIF($18, ''), p_city := NULLIF($19, ''), p_country := NULLIF($20, ''), p_info_tags := NULLIF($21, ''), p_extra_data_pairs := NULLIF($22, ''), p_clay_table_names := NULLIF($23, ''), p_recipe_id := NULLIF($24, ''), p_recipe_version := NULLIF($25, ''), p_selected_approach := NULLIF($26, ''), p_batch_id := NULLIF($27, ''), p_email_1_variant_a := NULLIF($28, ''), p_email_1_variant_b := NULLIF($29, ''), p_email_2_variant_a := NULLIF($30, ''), p_email_2_variant_b := NULLIF($31, ''), p_email_3_variant_a := NULLIF($32, ''), p_email_3_variant_b := NULLIF($33, ''), p_company_summary := NULLIF($34, ''), p_personalizations_pairs := NULLIF($35, ''))",
  "params": [
    "{{Email}}",
    "<SEGMENT_ID>",
    "{{First Name}}",
    "{{Last Name}}",
    "{{Full Name}}",
    "{{Title}}",
    "{{Personal LinkedIn URL}}",
    "{{Company Name}}",
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
    "{{City}}",
    "{{Country}}",
    "<INFO_TAGS>",
    "<EXTRA_DATA_BUILDER>",
    "<CLAY_TABLE_NAMES>",
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

Seven slots are placeholders (everything in `<...>`). Replace each with a
literal string for that table:

| Slot | Placeholder | What to put | Example |
|---:|---|---|---|
| 2 | `<SEGMENT_ID>` | The segment_id (or comma-separated multi) this Clay table pushes into. Required. | `"54"` (test segment) or `"28,37"` (multi) |
| 21 | `<INFO_TAGS>` | Free-form labels for cross-context tagging (legacy/source qualification tags). Comma-separated. | `"q2-rerun, builtwith-data"` |
| 22 | `<EXTRA_DATA_BUILDER>` | Pipe/semicolon recipe building extra_data jsonb from Clay columns. NOT JSON. | `"product_category|{{Product Category}};aov|{{AOV}}"` or `""` if none |
| 23 | `<CLAY_TABLE_NAMES>` | Name(s) of the Clay table(s) this lead is being pushed from. Comma-separated for multi. | `"TryNow Beauty Apollo Set 1, TryNow Q2 Expansion"` |
| 24 | `<RECIPE_ID_OR_EMPTY>` | recipe_id of the active recipe for this segment (only when generating emails). | `"51"` or `""` for enrichment-only |
| 25 | `<RECIPE_VERSION_OR_EMPTY>` | Version of that recipe. | `"1"` or `""` for enrichment-only |
| 35 | `<PERSONALIZATIONS_BUILDER_OR_EMPTY>` | Same pipe format as extra_data, building personalizations jsonb for email_outputs. | `"first_line|{{First Line}};research_report|{{Research Report}}"` or `""` |

The remaining 28 slots are `{{Clay Variable}}` placeholders for per-row
data. Clay's "Apply template" UI shows each as a dropdown — pick the
matching Clay column. For columns your Clay table doesn't have, see the
next section on the "Don't have it" workaround.

### `info_tags` vs `clay_table_names` — when to use which

Both are text[] arrays on `leads`. They represent different semantics:

- **`clay_table_names`** = the list of Clay table names this lead has been pushed from. Operational signal — "this lead came in via the SpeedSize SL 50K-100K table." Always use the actual Clay table name.
- **`info_tags`** = everything else operators want to flag — legacy migration tags (`ss-qualified-feb26`), qualification labels (`builtwith-data`, `madison-class-a`), special campaign markers, etc. Free-form.

Both merge via union on update — incoming empty leaves existing values intact, incoming with values dedupes and merges.

---

## Required vs optional

- **Required on the database side** (function errors if missing): `Email`, `<SEGMENT_ID>`
- **Optional on the database side**: everything else

Empty strings, NULLs, and Clay's `CLAYFORMATVALUE(...)` empty-format
placeholders are all normalized to NULL by the `clay_clean()` helper
inside the function. No row will fail because of empty data — only because
of bad data (e.g. non-int in segment_id, non-existent segment_id, etc.).

### `monthly_visits` accepts Clay display formats

Slot 12 (`p_monthly_visits`) is parsed via `parse_int_flex()`, so you can
map either a raw integer column (e.g. `Visits` = `10200`) or Clay's
display-formatted version (e.g. `Formatted Visits` = `10.2K`) — both work.

| Clay cell value | Stored as |
|---|---:|
| `10200` | 10200 |
| `10.2K` / `10.2k` | 10200 |
| `1.5M` | 1,500,000 |
| `2B` | 2,000,000,000 |
| `10,200` | 10200 |
| `$42.5K` | 42500 |
| `abc` or other junk | NULL (row still succeeds) |

---

## Operator protocol when applying the template

Clay's "Apply template" UI has two quirks that catch operators off guard
every time. Read this before your first push, or you'll spend 15 minutes
debugging a 400.

### Quirk 1: Clay treats every template variable as "required" by default

Even though the database accepts nulls for almost everything, Clay will
block the HTTP column from running until every variable has either (a) a
Clay column mapped, or (b) the **Required toggle turned OFF**.

**What to do:** when you apply the template, walk down the variable list
and **toggle OFF the "Required" switch for every variable except `Email`
and `p_segments_ids`**. Those two stay required. Everything else goes
off.

### Quirk 2: Every variable still needs SOMETHING mapped to run

Even after toggling off "Required", Clay won't fire the HTTP column if a
variable has no mapping. You can't just leave it blank.

**Workaround: the "Don't have it" column.** Create an always-blank column
in every Clay table you use this template with. Call it literally
`Don't have it`. When a template variable asks for a Clay column your
table doesn't have, map it to the `Don't have it` column. Clay sends the
blank value, `clay_clean()` normalizes it to NULL inside the function,
and the row processes fine.

### The minimum Clay columns every table needs for this template

Three non-negotiables for a smooth push:

| Clay column | Type | Purpose |
|---|---|---|
| `Email` | text | Maps to slot 1, the dedup key |
| `p_segments_ids` | text | Maps to slot 2, which segment(s) to file the lead into. Single `"54"` or comma-separated `"54,28"`. |
| `Don't have it` | text (always blank) | Maps to any variable your table doesn't have a real column for |

### Operator checklist for each new Clay table

1. Add `Email`, `p_segments_ids`, and `Don't have it` columns if missing.
2. Populate `p_segments_ids` with the segment_id(s) for this table.
3. Add the HTTP column, paste the URL + headers + body from this doc.
4. Replace the 6 `<...>` placeholders in the body with this table's values.
5. In the "Apply template" variable panel, toggle OFF "Required" for every
   variable except `Email` and `p_segments_ids`.
6. Map each `{{Clay Variable}}` dropdown:
   - If the table has a matching column → pick it.
   - If the table doesn't → pick `Don't have it`.
7. Run on 1 row first. Check Neon. If clean, run the rest.

## Auto-derived fields

The function fills these in automatically if the operator doesn't provide
them — Clay doesn't need a dedicated column for each:

| Field | Auto-derived from | When |
|---|---|---|
| `full_name` | `first_name` + `last_name` | If `full_name` is null/empty |
| `company_domain` | `company_website` (strip https://, www., path) | If `company_domain` is null/empty |
| `linkedin_username` | `linkedin_profile_url` (part after `/in/`) | If `linkedin_username` is null/empty |
| `is_personal_email` | Email domain vs known personal providers (gmail/yahoo/hotmail/outlook/etc.) | If `is_personal_email` not passed |

These used to be automatic on Supabase — now reimplemented in
`db/functions/clay_helpers.sql`. If the operator DOES provide a value,
the provided value wins over auto-derivation.

**This is why `linkedin_username`, `company_domain`, and
`is_personal_email` are NOT in the body's 34 slots** — the function
handles them. The operator only needs to provide `linkedin_profile_url`,
`company_website`, and `email` (which is the dedup key anyway). Saves 3
Clay column mappings per table.

## recipe_id — can be left empty

Slots 24 (`p_recipe_id`) and 25 (`p_recipe_version`) can both be `""` even
when generating emails. The function auto-falls back to the **active
recipe for the primary segment** (first segment_id in slot 2). Only pass
an explicit recipe_id when you need a specific one (e.g. testing a
non-active version).

If no active recipe exists for the primary segment, the function returns
a clear error: `No active recipe found for segment N`.

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

### `<CLAY_TABLE_NAMES>` — slot 23

The Clay table name(s) this lead is being pushed from. Comma-separated
for multiple. Stored in `leads.clay_table_names[]` (deduped + merged
with any existing names on the lead).

Example: `"TryNow Beauty Apollo Set 1"` for one table, or
`"TryNow Beauty Apollo Set 1, TryNow Q2 Expansion"` if you're pushing
from a Clay table that consolidated multiple sources.

This is the operational lineage column — when a lead exists in multiple
Clay tables across time, this array shows all of them. Same merge rule
as `info_tags`: incoming empty leaves existing untouched.

### `<RECIPE_ID_OR_EMPTY>` — slot 24

The recipe_id of the active recipe for the primary segment. Look it up:

```sql
SELECT recipe_id, version, clay_template_name, clay_template_link
FROM recipes
WHERE segment_id = <PRIMARY_SEGMENT> AND status = 'active';
```

For test segment 54 the placeholder recipe is `recipe_id = 51`.

If this Clay table is enrichment-only (not generating emails), put `""`.
The function will skip the email_outputs insert.

### `<RECIPE_VERSION_OR_EMPTY>` — slot 25

The version number of that recipe. Currently most recipes are at version 1.

If enrichment-only, `""`. If generating emails, the version that matches
the recipe_id from slot 24.

### `<PERSONALIZATIONS_BUILDER_OR_EMPTY>` — slot 35

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
