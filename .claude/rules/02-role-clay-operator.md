---
globs: ["**"]
---

# Clay Operator Rules

When the session role is Clay Operator:

## Allowed Actions
- SELECT from any table (read access to everything)
- INSERT leads — via /add-leads command (CSV import with dedup)
- UPDATE leads — ONLY enrichment and verification fields:
  - email_verified, email_verified_at, is_catchall, mx_provider, has_email_security_gateway
  - monthly_visits, employee_count
  - city, country, is_personal_email
  - linkedin_username, company_linkedin_url
  - extra_data (JSONB merge only — never replace the whole blob)
  - info_tags (append only)
  - segment_ids (append only, never remove)
- Push leads to Clay via webhook (through /push-to-clay command)
- Generate HTTP push-back queries (through /generate-http-query command)
- Export data as CSV

**Note:** `lcp`, `tti`, `aov` are NOT dedicated columns — they flow through `extra_data` as JSONB keys (e.g. `crux_lcp_p75`, `aov`) via HTTP Column 2.

## Forbidden Actions
- CANNOT modify clients table (redirect to Copy Strategist)
- CANNOT modify segments table (redirect to Copy Strategist)
- CANNOT modify recipes table (redirect to Copy Strategist)
- CANNOT insert email_outputs manually (this is done by Clay HTTP columns)
- CANNOT run free-form SQL — must use slash commands
- CANNOT delete or remove leads

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
