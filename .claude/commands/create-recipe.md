# Create a New Recipe (Strategist Only)

**ROLE CHECK:** This command is only for the Strategist (Mayank). If the current role is Clay Operator or Campaign Operator, say: "This command is for the Strategist only. Please ask Mayank to create recipes."

Guide the strategist through creating a new recipe for a client-segment.

## Step 1: Select Client

Show clients with `get_clients()`. After selection, show full client context:
```sql
SELECT client_name, target_icp_details, target_persona, pain_points,
       client_usp_differentiators, all_client_sales_resources,
       all_social_proof_brand_names, client_call_to_action,
       complimentary_sales_value, casestudy_or_leadmagnet_links
FROM clients WHERE client_id = $1
```

Display the client context so the strategist has it in view.

## Step 2: Select Segment

Show segments. Check if an active recipe already exists:
```sql
SELECT recipe_id, version, status, created_at
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

### 3b: Value Proposition
> **What's the value prop?** (shared across all approaches)

### 3c: Lead List Context
> **Describe the lead list.** (targeting criteria, why these leads, sales triggers)

### 3d: Data Variables Required
> **Which data variables does this recipe need?**
> Available: monthly_visits, employee_count, lcp, tti, aov, industry, extra_data fields
> List what the email generation needs.

### 3e: Enrichment Sources
> **What Clay enrichment is needed?**
> Options: StoreLeads (AOV), PageSpeed (LCP/TTI), CrUX, SimilarWeb, Claygent scrape, etc.

### 3f: Clay Instructions
> **Instructions for the Clay operator:**
> Step-by-step for setting up the Clay table with this recipe.
> Include: which columns to create, verification setup, formula logic, HTTP column config.

## Step 4: Preview

Show the complete recipe in a clean format. Ask for confirmation.

## Step 5: Save to Database

```sql
-- If there's an existing active recipe, deactivate it
UPDATE recipes SET status = 'inactive' WHERE segment_id = $1 AND status = 'active';

-- Insert new recipe
INSERT INTO recipes (client_id, segment_id, version, status, approach_content, value_prop, ...)
VALUES ($1, $2, $3, 'active', $4, $5, ...);
```

Use `write_query()` with confirmation.

> **Recipe saved!**
> - Client: {client_name}
> - Segment: {segment_name}
> - Version: {version}
> - Status: active
> - Recipe ID: {recipe_id}
>
> **Next step:** Test with `/test-recipe` or hand clay_instructions to the Clay operator.
