---
globs: ["**"]
---

# Campaign Operator Rules (Hasan)

When the session role is Campaign Operator:

## Allowed Actions
- SELECT from any table (read-only access)
- Export data as CSV
- View email outputs and batch history
- Search for specific leads by email

## Forbidden Actions
- CANNOT INSERT into any table
- CANNOT UPDATE any table
- CANNOT push to Clay
- CANNOT modify recipes or client data
- CANNOT run free-form SQL — must use slash commands

## This Role is READ-ONLY
The campaign operator should never be able to modify any data in the database.
If they ask to change something, say:
"The database is read-only for your role. If something needs to be changed, please ask Kuldeep (Clay Operator) or Mayank (Strategist)."

## Guided Workflows
- When getting a batch: ALWAYS filter to verified leads only
- When exporting: ALWAYS include the 4 custom fields (segment_id, recipe_id, recipe_version, selected_approach)
- For bad-infra re-sends: use /reuse-emails — pull exact same emails, no Clay needed

## Typical Daily Workflow
1. `/get-batch` — download a ready batch
2. Upload CSV to sequencer (Smartlead / Instantly)
3. Set up campaign with custom fields
4. Monitor delivery
5. If bad infra → `/reuse-emails` → fresh domains
