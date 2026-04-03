---
globs: ["**"]
---

# Strategist Rules (Mayank)

When the session role is Strategist:

## Allowed Actions
- Full read access to all tables
- INSERT/UPDATE on clients, segments, recipes
- Run custom SQL queries (with safety rules)
- Create and version recipes
- All Clay Operator and Campaign Operator commands

## Recipe Versioning Rules
- Only ONE active recipe per client-segment at a time
- Any change (even a small CTA tweak) = new version row
- Old version must be set to 'inactive' before new version is activated
- Version numbers always increment (never reuse a version number)
- Always include notes explaining what changed

## Recipe Creation Checklist
Before saving a recipe, verify:
- [ ] Client context pulled (ICP, USPs, pain points)
- [ ] Segment identified
- [ ] Approach content defined
- [ ] Value prop written
- [ ] Data variables listed
- [ ] Enrichment sources specified
- [ ] Clay instructions written for the Clay operator
- [ ] Previous version (if any) will be deactivated

## Custom Queries
The Strategist can run custom SQL, but:
- Safety rules still apply (no DELETE, DROP, etc.)
- Use `read_query()` for SELECT, `write_query()` for modifications
- Large modifications should still go through confirmation
