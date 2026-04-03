# Review Performance (Strategist Only)

**ROLE CHECK:** Strategist only.

Show batch history, output stats, and segment health for a client.

## Step 1: Select Client

Show clients with `get_clients()`. After selection, show overview:

```sql
-- Segments for this client
SELECT s.segment_id, s.segment_name,
       (SELECT COUNT(*) FROM leads WHERE s.segment_id = ANY(segment_ids)) as lead_count,
       (SELECT COUNT(*) FROM email_outputs WHERE segment_id = s.segment_id) as output_count,
       (SELECT version FROM recipes WHERE segment_id = s.segment_id AND status = 'active' LIMIT 1) as active_recipe_version
FROM segments s
WHERE s.client_id = $1
ORDER BY s.segment_id
```

> **{client_name} Overview:**
> | Segment | Leads | Outputs | Active Recipe |
> |---------|-------|---------|---------------|
> | 1M+ Qualified | 100 | 3 | v1 |
> | 100K-1M | 250 | 0 | None |

## Step 2: Deep Dive Options

> **What would you like to review?**
> 1. Segment details (leads + outputs for one segment)
> 2. Batch history (all batches across segments)
> 3. Recipe version history
> 4. Output comparison (compare approaches or versions)
> 5. Done

### Option 1: Segment Details
Show lead breakdown: verified vs unverified, enrichment coverage (% with LCP, AOV, etc.), output coverage.

### Option 2: Batch History
Use `get_batches()` — show all batches with counts, dates, recipe versions.

### Option 3: Recipe Version History
```sql
SELECT recipe_id, version, status, notes, created_at
FROM recipes WHERE client_id = $1
ORDER BY segment_id, version DESC
```

### Option 4: Output Comparison
Compare two batches or two recipe versions side by side:
- Show 3 sample emails from each
- Show approach distribution (how many leads got each approach)
- Note: reply rate comparison requires sequencer data (not in DB)

## Summary
> **This review is based on what's in the database.**
> For reply rates and campaign performance, check the sequencer dashboard.
> The custom fields (segment_id, recipe_id, recipe_version, selected_approach) in the sequencer enable filtering.
