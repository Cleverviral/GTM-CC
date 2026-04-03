# Check Batch Status

Show the operator recent batch history and details.

## Step 1: Show Recent Batches

Use `get_batches()` from db.py to show the 10 most recent batches:

> **Recent Batches:**
> | # | Batch ID | Segment | Leads | Recipe v | Date |
> |---|----------|---------|-------|----------|------|
> | 1 | batch-abc | SpeedSize 1M+ | 100 | v1 | 2026-04-01 |
> ...

## Step 2: Drill Down

Ask:
> **Want details on a specific batch?** (enter number or 'done')

If they pick a batch, show:
- Total leads in batch
- Breakdown by selected_approach
- Sample of 3 email outputs (subject line + first few words of email)
- Recipe version used

## Step 3: Cross-Segment View (Optional)

If they want a broader view:
- Show all batches for a client across segments
- Show total email outputs per client
- Show recipe version history
