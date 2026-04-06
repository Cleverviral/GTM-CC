# Campaign Operator Guide

## Your Role

You take ready batches and make campaigns live. You upload to sequencers, monitor delivery, and handle infrastructure issues.

**Your database access is completely read-only.** You cannot accidentally modify anything.

## Daily Workflow

### 1. Export a Batch
```
/export-csv
```
Claude will ask:
- Which client?
- Which segment?
- What to export (full batch, leads only, or email outputs only)

Then downloads a CSV ready for your sequencer.

### 2. Upload to Sequencer

The CSV includes:
- Lead data: email, name, company, job title
- Email content: 6 email variants (3 emails x 2 variants each)
- **Custom fields:** segment_id, recipe_id, recipe_version, selected_approach

**The custom fields are critical.** They enable performance tracking. Always include them as custom variables in your sequencer.

### 3. Monitor Campaign

Use your sequencer dashboard (Smartlead / Instantly) to track:
- Open rates
- Reply rates
- Domain health

## Check Email Outputs

Want to review what's been generated?
```
/check-outputs
```
Browse email outputs by client, segment, recipe version, or search by lead email.

## What You CAN'T Do
- **Can't modify any data** → Your access is read-only
- **Can't push to Clay** → That's the Clay Operator's job
- **Can't create recipes** → That's the Copy Strategist's job
- **Can't run free SQL** → Use the slash commands

## Need Help?
- For batch/export issues → ask the Clay Operator
- For recipe/strategy issues → ask the Copy Strategist
