# Push Leads to Clay Table

You are guiding the operator through pushing leads to a Clay table via webhook. Follow these steps IN ORDER.

## Prerequisites

If the operator hasn't run `/pull-leads` yet in this session, tell them:
> **You need to pull leads first.** Run `/pull-leads` to select your client, segment, and leads.

## Step 1: Get Webhook URL

Ask:
> **Paste the Clay webhook URL.**
> (It should look like: `https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-...`)

Validate:
- Must start with `https://api.clay.com/`
- Must contain `webhook`

If invalid, ask again.

## Step 2: Confirm Table Setup

Ask:
> **Is this a blank Clay table (not a template)?**
> Clay auto-creates columns from our JSON keys on blank tables.
> If you're using a template, column mapping may fail.

## Step 3: Preview Push Data

Show what will be sent for the first lead:
> **Here's what each lead will include:**
> - Identity: email, first_name, last_name, full_name, job_title
> - Company: company_name, company_domain, company_website, industry, employee_count
> - Enrichment: monthly_visits, lcp, tti, aov, extra_data
> - Verification: email_verified, email_verified_at, is_catchall, mx_provider
> - Segment: segment_id, segment_name, segment_tag
> - Recipe: recipe_id, recipe_version
> - Existing outputs (if any): subject_line_1/2, email variants
>
> **Total leads to push: {count}**

## Step 4: Test Push (1 Lead)

Ask:
> **Push 1 test lead first to verify it works?** (recommended)

If yes:
- POST the first lead as a single JSON object to the webhook URL
- Use `urllib.request` — same pattern as in `scripts/db.py`
- Show the response status code
- Ask operator to check Clay table: "Go to your Clay table and verify the columns look correct."

Wait for confirmation before proceeding.

## Step 5: Push All Leads

> **Pushing {count} leads to Clay (one at a time)...**

For each lead:
1. Build a flat JSON object with all fields (no nesting)
2. Convert segment_ids array to a string representation
3. Convert extra_data dict to a JSON string
4. POST to webhook URL
5. Show progress every 25 leads: "Pushed 25/{total}..."

Handle errors gracefully:
- If a POST fails, log the lead email and error, continue with next lead
- At the end, show: "{success} pushed, {failed} failed"

## Step 6: Summary

> **Push complete!**
> - Leads pushed: {success}
> - Failed: {failed}
> - Clay table: [check your Clay table]
>
> **Next steps for the Clay table:**
> 1. Set up the verification waterfall
> 2. Configure the 3 HTTP push-back columns (see recipe instructions)
> 3. Run the table
>
> When Clay finishes processing, results auto-push to Neon via HTTP columns.

## Important Notes

- ALWAYS push one lead at a time (single JSON object per POST, NOT arrays)
- Clay webhook does NOT accept arrays — it must be one object per request
- Use a 0.1s delay between requests to avoid rate limiting
- If the push fails on ALL leads, the webhook URL might be wrong — ask to verify
