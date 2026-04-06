---
globs: ["**"]
---

# Clay Operator Rules

When the session role is Clay Operator:

## Allowed Actions
- SELECT from any table (read access to everything)
- UPDATE leads — ONLY enrichment and verification fields:
  - email_verified, email_verified_at, is_catchall, mx_provider
  - lcp, tti, aov, monthly_visits, employee_count
  - city, country
  - extra_data (JSONB merge only)
  - segment_ids (append only, never remove)
- Push leads to Clay via webhook (through /push-to-clay command)
- Generate HTTP push-back queries (through /generate-http-query command)
- Export data as CSV

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
- Forgetting to include existing email outputs in the push → ALWAYS include all 38 fields
- Not verifying the webhook URL format → VALIDATE before pushing
