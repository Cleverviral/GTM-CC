# Idea: Sequencer API Feedback Loop

## Problem
Reply data (positive, negative, OOO, bounce) lives in the sequencer (Smartlead, Instantly, etc.) and never makes it back to the DB. Without it, we can't answer:
- Which approach/recipe version is performing best?
- What's the reply rate per segment?
- Which leads have already been contacted and responded?

## Proposed Solution
Connect sequencer APIs to pull reply data back into Neon.

### What We'd Track (execution_log or similar table)
- lead_id / email
- campaign_name
- sequencer_type (smartlead / instantly / etc.)
- sent_at
- reply_received (boolean)
- reply_type (positive / negative / ooo / bounce)
- reply_at

### Possible Approaches
1. **Sequencer API polling** — scheduled script that pulls campaign stats via API
2. **Webhook from sequencer** — if the sequencer supports webhooks on reply events
3. **Manual CSV import** — export reply data from sequencer dashboard, import to Neon
4. **N8N automation** — trigger on sequencer events, push to Neon

### What This Enables
- Approach performance pivot: approach x segment x version → reply rate
- "This approach got 4% replies on Retail but 1% on Enterprise"
- Auto-flag: campaigns with 0% reply rate after 7+ days → check infrastructure
- Lead history: all approaches this lead has received across all clients
- Inform recipe versioning: data-driven reason to change approach

### Dependencies
- Sequencer API access (API keys, rate limits)
- Mapping between sequencer campaign IDs and our batch_id / recipe_id
- The 4 custom fields (segment_id, recipe_id, recipe_version, selected_approach) we include in the CSV must travel into the sequencer as custom fields so we can map replies back

### Open Questions
- Which sequencer(s) are we using? Do they all have APIs?
- How often should we poll? Real-time vs daily?
- Who owns this integration — is it automated or does the campaign operator trigger it?
