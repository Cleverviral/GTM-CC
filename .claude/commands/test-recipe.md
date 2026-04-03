# Test a Recipe on Sample Leads (Strategist Only)

**ROLE CHECK:** Strategist only. Redirect Clay/Campaign operators to Mayank.

## Step 1: Select Recipe

Show active recipes:
```sql
SELECT r.recipe_id, r.version, r.status, r.created_at,
       c.client_name, s.segment_name
FROM recipes r
JOIN clients c ON c.client_id = r.client_id
JOIN segments s ON s.segment_id = r.segment_id
WHERE r.status = 'active'
ORDER BY r.created_at DESC
```

> **Which recipe do you want to test?** (numbered list)

## Step 2: Pull Sample Leads

Pull 5-10 sample leads from the segment:
```python
from db import get_leads_for_segment
samples = get_leads_for_segment(segment_id, limit=10)
```

Show diversity: "Here are 10 sample leads with varying company sizes, industries, and enrichment data."

## Step 3: Show Recipe Match Check

For each sample lead, show:
- Does this lead have existing email outputs?
- If yes, what recipe version? Does it match the current active version?
- Decision: PASS_THRU / REGENERATE / NEW

> **Decision Matrix Preview:**
> | Lead | Company | Existing Output? | Recipe Match? | Decision |
> |------|---------|-------------------|---------------|----------|
> | john@acme.com | Acme Corp | v1 | v1 = v1 ✓ | PASS_THRU |
> | jane@beta.com | Beta Inc | None | N/A | REGENERATE |

## Step 4: Generate Sample Emails (Optional)

Ask:
> **Want me to generate 3 sample emails using this recipe's approach?**
> I'll use the approach content + lead data to draft emails.

If yes, generate using the recipe's approach content applied to 3 diverse leads.
Show: subject line, email body, which approach was selected.

## Step 5: Summary

> **Recipe test complete.**
> - Leads in segment: {count}
> - Would PASS_THRU: {x} (have current version outputs)
> - Would REGENERATE: {y} (new or version mismatch)
> - Sample emails look good? Ready to hand to Clay operator.
