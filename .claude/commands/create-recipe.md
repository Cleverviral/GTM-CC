# Create a New Recipe (Copy Strategist Only)

**ROLE CHECK:** This command is only for the Copy Strategist. If the current role is Clay Operator or Campaign Operator, say: "This command is for the Copy Strategist only."

Guide the strategist through creating a new recipe for a client-segment.

## Step 1: Select Client

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query

clients = read_query("SELECT client_id, client_name, target_icp_details, target_persona, pain_points, client_usp_differentiators FROM clients WHERE client_status = 'active' LIMIT 50")
```

Show numbered list. After selection, display the full client context.

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

Guide through each section:

### 3a: Approach Content
> **Describe the email approach(es) for this segment.**
> Include: angle, tone, CTA, what makes this different.
> You can define multiple approaches (the selector will pick one per lead).

### 3b: Data Variables Required
> **Which data variables does this recipe need?**
> Available: monthly_visits, employee_count, lcp, tti, aov, industry, extra_data fields
> List what the email generation needs.

### 3c: Clay Template Name
> **What is the saved Clay template name for this recipe?**
> This is the template the Clay operator will use when setting up the Clay table.
> (e.g., "speedsize-1m-plus-v1")

### 3d: Clay Instructions
> **Instructions for the Clay operator:**
> Step-by-step for setting up the Clay table with this recipe.
> Include: which columns to create, verification setup, formula logic, HTTP column config.

### 3e: Sample Email ID
> **What is the Sample Email ID from the Notion repo?**
> This is the ID from the sample email repo in Notion. The campaign operator adds it to the campaign name so the reporting dashboard can link the campaign to the email copy.
> (e.g., "SE-0042")
>
> If you haven't created the sample email page yet, you can add this later.

### 3f: Notes
> **What changed in this version?** (for version tracking)

## Step 4: Preview

Show the complete recipe in a clean format. Ask for confirmation.

## Step 5: Save to Database

```sql
-- If there's an existing active recipe, deactivate it
UPDATE recipes SET status = 'inactive', updated_at = NOW() WHERE segment_id = $1 AND status = 'active';

-- Insert new recipe
INSERT INTO recipes (client_id, segment_id, version, status, approach_content, data_variables_required, clay_template_name, clay_instructions, sample_email_id, notes)
VALUES ($1, $2, $3, 'active', $4, $5, $6, $7, $8, $9);
```

Use `write_query()` with confirmation.

> **Recipe saved!**
> - Client: {client_name}
> - Segment: {segment_name}
> - Version: {version}
> - Status: active
> - Clay Template: {clay_template_name}
>
> **Next step:** Test with `/test-recipe` or share clay_instructions with the Clay operator.
