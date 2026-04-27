---
globs: ["**"]
---

# Clay Operator Rules

When the session role is Clay Operator:

## Allowed Actions
- SELECT from any table (read access to everything)
- INSERT leads — via /add-leads command (CSV import with dedup)
- UPDATE leads via the `upsert_lead()` function — Clay's HTTP column hits Neon's SQL-over-HTTP endpoint and the function does the merge. Never write raw `UPDATE leads ...` from this role. The function only touches the columns it's designed to update:
  - email_verified, email_verified_at, is_catchall, mx_provider, has_email_security_gateway
  - monthly_visits, employee_count
  - city, country, is_personal_email
  - linkedin_username, company_linkedin_url
  - extra_data (JSONB merge — never replaces the whole blob; incoming empty leaves existing untouched)
  - info_tags (union merge — incoming empty leaves existing untouched)
  - clay_table_names (union merge — same rule as info_tags)
  - segment_ids (union merge, never removes)
- Push leads to Clay via webhook (through /push-to-clay command)
- Generate HTTP push-back body for a Clay table (through /generate-http-query — produces the universal `upsert_lead()` body)
- Inspect data via /inspect-extra-data and /pull-leads
- Export data as CSV

## Controlled-Environment Guarantees
The Clay Operator never writes raw SQL. All writes go through:
1. `/add-leads` — inserts with dedup, append-only segment_ids
2. `/push-to-clay` — webhook out to Clay, no DB writes
3. Clay's HTTP column → `upsert_lead()` — function enforces "new data never destroys old data" merge rules across scalar (COALESCE), array (union with empty-incoming guard), and jsonb (`||` with empty-incoming guard). All inputs are text, parsed safely; bad data becomes NULL, no row crashes the table.

This means a Clay Operator running unaudited Clay tables cannot:
- Wipe existing enrichment by pushing empty cells
- Remove a lead from a segment
- Overwrite verified data with garbage
- Bypass dedup and create duplicate leads

Any change to these guarantees requires editing `db/functions/upsert_lead.sql` (Copy Strategist territory) and redeploying.

**Note:** `lcp`, `tti`, `aov` are NOT dedicated columns — they flow through `extra_data` as JSONB keys (e.g. `crux_lcp_p75`, `aov`) via the universal HTTP body.

**Note:** `clay_table_names` is a dedicated `text[]` column on `leads` (not part of `info_tags`, not inside `extra_data`). It records which Clay tables a lead has been pushed from. Slot 23 of the universal HTTP body fills it.

## Forbidden Actions
- CANNOT modify clients table (redirect to Copy Strategist)
- CANNOT modify segments table (redirect to Copy Strategist)
- CANNOT modify recipes table (redirect to Copy Strategist)
- CANNOT insert email_outputs manually (the `upsert_lead()` function inserts them when the Clay column sends email content)
- CANNOT run free-form SQL — must use slash commands
- CANNOT write raw `UPDATE leads ...` or `INSERT INTO email_outputs ...` queries — all push-back goes through `upsert_lead()`
- CANNOT delete or remove leads
- CANNOT redeploy `upsert_lead()` or any function in `db/functions/` (Copy Strategist task)

## Guided Workflows
- When pulling leads: ALWAYS ask for client, segment, and filters
- When pushing to Clay: ALWAYS show recipe info + clay_template_name first, validate webhook URL, and send test lead first
- When exporting: ALWAYS verify the export includes custom fields for tracking
- If the operator asks to do something outside their role, say:
  "That's a Copy Strategist task. Please ask the Copy Strategist to handle this."

## Common Mistakes to Prevent
- Pulling leads without specifying a segment → BLOCK, ask for segment
- Pushing to a template table instead of blank table → WARN about column mapping
- Forgetting to include existing email outputs in the push → ALWAYS include all core fields (identity, company, enrichment, verification, client, segment, batch+recipe, existing outputs) + every `leads.extra_data` key flattened
- Not verifying the webhook URL format → VALIDATE before pushing
- Treating `lcp`/`tti`/`aov` as dedicated columns → they're not, they live in `extra_data`
- Forgetting to fill slot 23 (`<CLAY_TABLE_NAMES>`) in the HTTP body → leaves lineage blank for new pushes
- Adding a `::int` cast in the HTTP body → the function takes everything as text on purpose; casts cause "invalid syntax for integer" errors
- Stray characters after `{{Variable}}` (e.g. `{{Email Verified}}e`) → produce `truee`/`falsee` in the DB; spot-check on the test row
