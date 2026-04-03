# Clay Operator Guide (Kuldeep)

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
- Ask for the webhook URL
- Preview what will be sent
- Push 1 test lead first
- Ask you to verify in Clay
- Then push all remaining leads

### 3. Set Up Clay Table
After leads land in Clay:
1. Set up the verification waterfall (same as always)
2. Configure the 3 HTTP push-back columns:
   - **HTTP Column 1:** Verification → Neon (email_verified, is_catchall)
   - **HTTP Column 2:** Enrichment → Neon (LCP, TTI, AOV + extra_data)
   - **HTTP Column 3:** Email Outputs → Neon (all email variants + approach)
3. Set up email generation pipeline per recipe instructions
4. Run the table

### 4. Export for Campaign Operator
```
/export-csv
```
Choose "Full batch for campaign operator" — includes all custom fields for tracking.
Hand the CSV to Hasan.

## What You CAN'T Do (and Why)
- **Can't modify recipes** → That's Mayank's job. If the approach needs changing, tell him.
- **Can't create segments** → Also Mayank. If you need a new segment, ask him.
- **Can't write free SQL** → Use the commands. They handle everything safely.

## Common Scenarios

### "I need to re-run leads for a new recipe version"
Just run `/pull-leads` again. The system will show which leads have outputs from the old version (they'll be REGENERATE in Clay).

### "Clay processed but I need to check what pushed back to Neon"
Run `/check-batch` to see the latest batch and output counts.

### "I got an error pushing to Clay"
- Check the webhook URL — is it correct?
- Make sure the Clay table is **blank** (not a template)
- Try pushing 1 test lead first

## Need Help?
Ask Mayank. Don't try to work around the system — it's there to prevent mistakes.
