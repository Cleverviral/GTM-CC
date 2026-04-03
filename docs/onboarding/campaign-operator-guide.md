# Campaign Operator Guide (Hasan)

## Your Role

You take ready batches and make campaigns live. You upload to sequencers, monitor delivery, and handle infrastructure issues.

**Your database access is completely read-only.** You cannot accidentally modify anything.

## Daily Workflow

### 1. Get a Ready Batch
```
/get-batch
```
Claude will ask:
- Which client?
- Which segment?
- Shows available batches

Then downloads a CSV ready for your sequencer.

### 2. Upload to Sequencer

The CSV includes:
- Lead data: email, name, company, job title
- Email content: 2 subject lines, 9 email variants (3 emails × 3 variants each)
- **Custom fields:** segment_id, recipe_id, recipe_version, selected_approach

**The custom fields are critical.** They enable performance tracking. Always include them.

### 3. Monitor Campaign

Use your sequencer dashboard (Smartlead / Instantly) to track:
- Open rates
- Reply rates
- Domain health

### 4. Bad Infrastructure? No Problem

If a campaign has 0% reply (domain/IP issues):
```
/reuse-emails
```
This pulls the **exact same emails** from the database. Upload to a new sequencer campaign with fresh domains. Zero Clay cost.

## What You CAN'T Do
- **Can't modify any data** → Your access is read-only
- **Can't push to Clay** → That's Kuldeep's job
- **Can't create recipes** → That's Mayank's job
- **Can't run free SQL** → Use the commands

## Check Email Outputs

Want to review what's been generated?
```
/check-outputs
```
Browse email outputs by client, segment, batch, or search by lead email.

## Need Help?
- For batch issues → ask Kuldeep (Clay Operator)
- For recipe/strategy issues → ask Mayank (Strategist)
