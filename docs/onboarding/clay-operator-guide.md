# Clay Operator Guide

## Your Role

You manage leads and run Clay tables. You pull leads from the database, push them to Clay for processing, and the results automatically flow back to the database via HTTP columns.

## Daily Workflow

### 1. Pull Leads
```
/pull-leads
```
Claude will ask:
- Which client? (shows a list)
- Which segment? (shows segments with lead counts)
- Any filters? (verified only, min visits, country)

Then shows a preview and asks you to confirm.

### 2. Push to Clay
```
/push-to-clay
```
Before this:
- Create a **blank** Clay table (not a template)
- Copy the webhook URL from the Clay table source

Claude will:
- Show the active recipe info (template name + instructions)
- Ask for the webhook URL
- Preview what will be sent (38 fields per lead)
- Push 1 test lead first
- Ask you to verify in Clay
- Then push all remaining leads

### 3. Set Up Clay Table
After leads land in Clay:
1. Set up the verification waterfall (same as always)
2. Configure the 3 HTTP push-back columns using `/generate-http-query`:
   - **HTTP Column 1:** Verification → Neon (email_verified, is_catchall, mx_provider)
   - **HTTP Column 2:** Enrichment → Neon (LCP, TTI, AOV + extra_data JSONB)
   - **HTTP Column 3:** Email Outputs → Neon (email variants + approach)
3. Set up email generation pipeline per recipe instructions
4. Run the table

### 4. Generate HTTP Queries
```
/generate-http-query
```
This generates the exact HTTP body (query + params) you need for Clay's HTTP columns. Just copy-paste into Clay — no editing needed.

### 5. Export for Campaign Operator
```
/export-csv
```
Choose "Full batch for campaign operator" — includes all custom fields for tracking.

## What You CAN'T Do (and Why)
- **Can't modify recipes** → That's a Copy Strategist task. If the approach needs changing, let them know.
- **Can't create segments** → Also Copy Strategist. If you need a new segment, ask them.
- **Can't write free SQL** → Use the slash commands. They handle everything safely.

## Common Scenarios

### "I need to re-run leads for a new recipe version"
Just run `/pull-leads` again. The system will show which leads have outputs from the old version (they'll be REGENERATE in Clay).

### "Clay processed but I need to check what pushed back to Neon"
Run `/check-outputs` to see output counts by segment and recipe version.

### "I need to add a new enrichment data point to the HTTP push-back"
Run `/generate-http-query` and tell it the new Clay column names. It will regenerate the query with the new fields added to extra_data.

### "I got an error pushing to Clay"
- Check the webhook URL — is it correct?
- Make sure the Clay table is **blank** (not a template)
- Try pushing 1 test lead first

## Need Help?
Ask the Copy Strategist. Don't try to work around the system — it's there to prevent mistakes.
