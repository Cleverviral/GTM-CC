---
globs: ["**"]
---

# Copy Strategist Rules

When the session role is Copy Strategist:

## Allowed Actions
- Full read access to all tables
- INSERT/UPDATE on segments, recipes
- Run custom SQL queries (with safety rules)
- Create and version recipes
- All Clay Operator and Campaign Operator commands
- This role is the admin for TAM + Recipe DB

## Do NOT edit `clients` directly
The `clients` table is a **subscriber** — it auto-syncs from the CleverViral Prod Neon database. Never write to `clients` here. To add/change a client, update it in CleverViral Prod; the change replicates in.

## Recipe Versioning Rules
- Only ONE active recipe per (client_id, segment_id) at a time
- Any change (even a small CTA tweak) = new version row
- Old version must be set to 'inactive' before new version is activated
- Version numbers always increment (never reuse a version number)
- New row's `parent_recipe_id` = the deactivated row's `recipe_id` (preserves lineage)
- Always include `recipe_notes` explaining what changed

## Recipe Creation Checklist
Before saving a recipe, verify:
- [ ] Client context pulled (ICP, USPs, CTA, sales resources from the `clients` table)
- [ ] Segment identified
- [ ] Value prop set on the segment (`segments.value_prop`)
- [ ] Leadlist context set on the segment (`segments.leadlist_context`)
- [ ] Clay template name specified (or `"Refer to sample email repo"` for Notion-based static approaches)
- [ ] Clay template link specified (or sentinel for Notion-based)
- [ ] Recipe notes written (what's new in this version)
- [ ] Previous version (if any) will be deactivated and set as `parent_recipe_id`

## Custom Queries
The Copy Strategist can run custom SQL, but:
- Safety rules still apply (no DELETE, DROP, TRUNCATE, ALTER, or UPDATE without WHERE)
- Use `read_query()` for SELECT, `write_query()` for modifications
- Large modifications should still go through confirmation
