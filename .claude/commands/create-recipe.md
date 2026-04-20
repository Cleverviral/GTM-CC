# Create a New Recipe (Copy Strategist Only)

**ROLE CHECK:** This command is only for the Copy Strategist. If the current role is Clay Operator or Campaign Operator, say: "This command is for the Copy Strategist only."

Guide the strategist through creating a new recipe for a client-segment.

## Step 1: Select Client

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query

clients = read_query("""
    SELECT client_id, client_name, client_website,
           target_icp_details, client_usp_differentiators,
           client_call_to_action, complimentary_sales_value,
           all_client_sales_resources, all_social_proof_brand_names
    FROM clients
    WHERE client_status::text = 'active'
    LIMIT 50
""")
```

Show numbered list. After selection, display the full client context (ICP, USPs, CTA, sales resources, social proof).

## Step 2: Select Segment

```python
segments = read_query("SELECT segment_id, segment_name, segment_tag, value_prop, leadlist_context FROM segments WHERE client_id = $1 LIMIT 50", [str(client_id)])
```

Show segments. Verify that `value_prop` and `leadlist_context` are populated on the chosen segment:
- If `value_prop` is NULL: "Value prop is not set on this segment. Please provide one now or set it before creating the recipe."
- If `leadlist_context` is NULL: "Leadlist context is not set on this segment. Please provide one now or set it before creating the recipe."

Check if an active recipe already exists:
```sql
SELECT recipe_id, version, status, clay_template_name, created_at
FROM recipes WHERE segment_id = $1 ORDER BY version DESC LIMIT 5
```

If active recipe exists:
> **Active recipe exists:** v{version} (created {date})
> Creating a new recipe will be version {version + 1}.
> The old version will be marked 'inactive'.

## Step 3: Recipe Content

Recipes in the TAM + Recipe DB are lightweight pointers to Clay templates. The approach itself lives in the Clay template (or in the sample email repo for Notion-based static approaches). Collect only what's needed:

### 3a: Clay Template Name
> **What is the saved Clay template name for this recipe?**
> (e.g., `"[14/04/26] -> SpeedSize [Post Sagi's Feedback Recipe]"`)
> If the approach is Notion-based (no Clay template), answer `Refer to sample email repo`.

### 3b: Clay Template Link
> **Paste the full Clay template URL.**
> (e.g., `https://app.clay.com/workspaces/.../tables/.../views/...`)
> If the approach is Notion-based, answer `Refer to sample email repo`.

### 3c: Recipe Notes
> **What changed in this version?** Or for v1: what's the approach in 1–2 sentences.
> This is for version tracking and operator context.

## Step 4: Preview

Show the complete recipe in a clean format. Ask for confirmation.

## Step 5: Save to Database

```sql
-- Get the previous active recipe (if any) so we can link lineage
SELECT recipe_id, version FROM recipes
WHERE segment_id = $1 AND status = 'active' LIMIT 1;

-- Deactivate the previous active recipe
UPDATE recipes SET status = 'inactive', updated_at = NOW()
WHERE segment_id = $1 AND status = 'active';

-- Insert new recipe
INSERT INTO recipes (
    client_id, segment_id, version, status,
    parent_recipe_id,
    clay_template_name, clay_template_link, recipe_notes
) VALUES ($1, $2, $3, 'active', $4, $5, $6, $7);
```

Params: `[client_id, segment_id, new_version, prev_recipe_id_or_null, clay_template_name, clay_template_link, recipe_notes]`

Use `write_query()` with confirmation.

> **Recipe saved!**
> - Client: {client_name}
> - Segment: {segment_name}
> - Version: {version}
> - Status: active
> - Clay Template: {clay_template_name}
>
> **Next step:** Test with `/test-recipe` or share the `clay_template_link` + `recipe_notes` with the Clay operator.
