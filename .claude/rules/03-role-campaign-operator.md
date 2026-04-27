---
globs: ["**"]
---

# Campaign Operator Rules

When the session role is Campaign Operator:

## Allowed Actions
- SELECT from any table (read-only access)
- Export data as CSV (via /export-csv)
- View email output stats incl. personalizations and clay_table_names lineage (via /check-outputs)
- Inspect extra_data keys + fill rates (via /inspect-extra-data)
- Search for specific leads by email (within the bounded slash commands)

## Forbidden Actions
- CANNOT INSERT into any table
- CANNOT UPDATE any table
- CANNOT push to Clay
- CANNOT modify recipes or client data
- CANNOT run free-form SQL — must use slash commands
- CANNOT call `/generate-http-query`, `/push-to-clay`, `/add-leads`, or any function-deployment script

## Controlled-Environment Guarantees
The Campaign Operator only has three slash commands available — `/export-csv`, `/check-outputs`, `/inspect-extra-data` — all of which are SELECT-only behind `read_query()`. There is no path from this role to a write. If they ask to change something, the answer is always to redirect.

## This Role is READ-ONLY
The campaign operator should never be able to modify any data in the database.
If they ask to change something, say:
"The database is read-only for your role. If something needs to be changed, please ask the Clay Operator or Copy Strategist."

## Guided Workflows
- When exporting: ALWAYS include the 4 custom fields (segment_id, recipe_id, recipe_version, selected_approach)
- When checking outputs: filter by client+segment, show approach distribution and sample emails

## Typical Daily Workflow
1. `/export-csv` — download a ready batch with emails
2. Upload CSV to sequencer (Smartlead / Instantly)
3. Set up campaign with custom fields
4. Monitor delivery
