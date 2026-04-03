# Idea: Batches Table

## Problem
Batch tracking today is just a `batch_id` text string on `email_outputs`. No way to know:
- How many leads were pushed vs how many came back
- When a batch was triggered
- Whether a batch is complete or has missing leads

## Proposed Solution
A `batches` table that logs at push time:

| Column | Source | Notes |
|--------|--------|-------|
| batch_id | text PK | Generated at push time |
| client_id | UUID | |
| segment_id | int | |
| recipe_id | int | |
| recipe_version | int | |
| leads_pushed | int | Logged by /push-to-clay at push time |
| leads_returned | int | COUNT of email_outputs with this batch_id |
| pushed_at | timestamptz | When /push-to-clay ran |
| completed_at | timestamptz | When last HTTP Col 3 response came in |

## What We Can Track Automatically
- leads_pushed — known at push time
- leads_returned — COUNT from email_outputs
- "200 leads missing" — diff between pushed and returned

## What We Can't Get From Clay
- pushed_by (who triggered) — would need to log from Claude Code session
- clay_table_url — Clay doesn't return this, would need manual input
- status (complete/incomplete) — no "done" signal from Clay, would have to infer from pushed vs returned

## Implementation
Log a row at push time from `/push-to-clay`. Email_outputs rows fill in as Clay processes. Query joins batch table with email_outputs counts.
