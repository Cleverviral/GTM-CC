# GTM-CC Complete System Scope
## One Neon DB. Three Roles. 30 Clients. Every Scenario.

---

# PART 1: THE DATABASE (Neon)

Everything runs on ONE Neon database. Five tables.

---

## Table 1: `clients`
**Source:** Tally onboarding form webhook
**Updated by:** Copy Strategist (manual approval), Tally webhook (auto)
**Read by:** Copy Strategist (recipe creation context), Dashboard (all roles)

| Column | Type | Description |
|--------|------|-------------|
| client_id | serial PK | Auto-generated |
| client_name | text | e.g., "Hector" |
| client_website | text | e.g., "hector.com" |
| client_status | text | in_onboarding / active / paused / churned |
| primary_poc_name | text | Main client contact |
| primary_poc_email | text | |
| target_icp_details | text | ICP description across segments |
| client_usp_differentiators | text | USPs and differentiators |
| all_client_sales_resources | text | Case studies, FAQs, resources |
| all_social_proof_brand_names | text | Logo wall brands |
| client_call_to_action | text | What the client wants prospects to do |
| complimentary_sales_value | text | Free offer / lead magnet |
| casestudy_or_leadmagnet_links | text | Links for autoresponder |
| dnc_list_url | text | Do Not Contact list |
| client_crm | text | hubspot / pipedrive / salesforce / etc |
| notification_channels | text | slack / email / both |
| slack_main_channel_id | text | |
| slack_responder_channel_id | text | |
| ar_client_choice | text | yes / no / tell_me_more |
| ar_mode | text | all_manual / first_auto / all_auto |
| ar_context_doc | text | Link to autoresponder context doc |
| cv_report_link | text | Reporting dashboard link |
| sequencer_client_campaign_name | text | Auto-generated from client_name |
| approved | boolean | Must be true before downstream use |
| created_at | timestamptz | |
| updated_at | timestamptz | |

---

## Table 2: `segments`
**Source:** Copy Strategist creates when defining ICP segments
**Updated by:** Copy Strategist
**Read by:** All roles (filtering leads, recipes, outputs)

| Column | Type | Description |
|--------|------|-------------|
| segment_id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client |
| segment_name | text | e.g., "Retail", "Agency", "Enterprise" |
| segment_tag | text | Human-readable label |
| description | text | |
| target_industry | text | e.g., "Retail ecommerce" |
| target_persona | text | e.g., "VP Marketing, Director of Growth" |
| target_pain_points | text | Key pain points for this segment |
| icp_criteria | text | How to identify leads for this segment |
| value_prop | text | Value proposition for this segment |
| leadlist_context | text | Targeting criteria for this segment |
| status | text | active / paused / archived |
| created_at | timestamptz | |
| updated_at | timestamptz | |

**UNIQUE constraint:** (client_id, segment_name) — no duplicate segments per client.

---

## Table 3: `leads`
**Source:** Data team (Apollo, SimilarWeb, etc.) → Clay for verification → Neon
**Updated by:** Data team (new leads), Clay push-back (enrichment + verification), Sequencer API sync (reply data)
**Read by:** All roles

| Column | Type | Description |
|--------|------|-------------|
| lead_id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client this lead belongs to |
| segment_id | int FK → segments | Which segment |
| segment_name | text | Denormalized for easy queries |
| | | |
| **Identity** | | |
| email | text | Prospect email (unique per client) |
| first_name | text | |
| last_name | text | |
| full_name | text | |
| job_title | text | |
| linkedin_profile_url | text | |
| linkedin_username | text | |
| | | |
| **Company** | | |
| company_name | text | |
| company_domain | text | |
| company_website | text | |
| company_linkedin_url | text | |
| industry | text | |
| | | |
| **Enrichment (approach-agnostic, stays forever)** | | |
| monthly_visits | int | From SimilarWeb or Clay |
| employee_count | int | From Apollo or Clay |
| email_verified | boolean | |
| email_verified_at | timestamptz | Last verification date |
| mx_provider | text | Gmail, Outlook, etc. |
| has_email_security_gateway | boolean | |
| is_catchall | boolean | |
| is_personal_email | boolean | |
| city | text | |
| country | text | |
| LCP | float | Largest Contentful Paint (PageSpeed) |
| TTI | float | Time to Interactive (PageSpeed) |
| AOV | float | Average Order Value (StoreLeads) |
| tags | text | Custom tags |
| extra_data | jsonb | Any additional enrichment fields |
| | | |
| **Status** | | |
| lead_status | text | raw / verified / contacted / replied / dnc |
| contacted_count | int | How many times contacted (across all recipes) |
| last_contacted_at | timestamptz | When last email was sent |
| cooldown_until | timestamptz | Don't contact before this date (last_contacted + 30 days) |
| | | |
| created_at | timestamptz | When lead was added to DB |

**UNIQUE constraint:** (client_id, segment_id, email) — same person can exist for different clients/segments.

**Cross-client:** john@acme.com can have:
- Row 1: client=Hector, segment=Retail
- Row 2: client=Owner.com, segment=Restaurant
These are separate rows. No conflict. DNC is per-client.

---

## Table 4: `recipes`
**Source:** Copy Strategist creates via Claude Code + email-approach-generator skill
**Updated by:** Copy Strategist (create, version, deactivate)
**Read by:** Clay operator (instructions), Campaign operator (reuse check), Copy Strategist (performance review)

| Column | Type | Description |
|--------|------|-------------|
| recipe_id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client |
| segment_id | int FK → segments | Which segment |
| segment_name | text | Denormalized |
| | | |
| **Recipe Identity** | | |
| recipe_name | text | e.g., "ROI Calculator", "Insider Remark" |
| version | int | Starts at 1, bumps on ANY change |
| status | text | active / inactive / testing |
| parent_recipe_id | int FK → recipes | Links to previous version (null for v1) |
| | | |
| **Approach Content** | | |
| approach_content | text | Full email approach markdown (reference, NOT pushed to Clay) |
| | | |
| **Data Requirements** | | |
| data_variables_required | text[] | e.g., ARRAY['aov', 'review_count'] |
| enrichment_sources | text[] | e.g., ARRAY['StoreLeads for AOV', 'PageSpeed for LCP'] |
| research_required | boolean | Whether Claygent researcher runs |
| | | |
| **Clay Operator Instructions** | | |
| clay_template_name | text | Which Clay template to clone |
| clay_instructions | text | Step-by-step for the Clay operator (plain text) |
| | | |
| **Meta** | | |
| notes | text | Why created, what changed in this version |
| created_at | timestamptz | |
| updated_at | timestamptz | |

**Version flow:**
- Create recipe → version 1, parent = null, status = testing
- Test and approve → status = active
- Edit recipe → NEW row with version 2, parent = old recipe_id, old row status → inactive
- Kill recipe → status = inactive

**A segment has MULTIPLE active recipes.** Example:
```
Hector Retail:
  recipe_id=47, "ROI Calculator" v2, active
  recipe_id=52, "Insider Remark" v3, active
  recipe_id=61, "Page Speed Angle" v1, testing
  recipe_id=38, "Customer Empathy" v1, inactive (killed)
```

The approach selector formula in Clay picks which recipe each lead gets based on data availability.

---

## Table 5: `email_outputs`
**Source:** Clay push-back (after running recipe) + Sequencer API sync (reply data)
**Updated by:** Clay push-back script (emails), Campaign operator (sent status), Sequencer API sync (replies)
**Read by:** Campaign operator (CSV export, reuse check), Copy Strategist (performance queries)

| Column | Type | Description |
|--------|------|-------------|
| output_id | serial PK | Auto-generated |
| lead_id | int FK → leads | Which lead |
| client_id | int FK → clients | Which client |
| segment_id | int FK → segments | Which segment |
| segment_name | text | Denormalized |
| | | |
| **Recipe Tracking** | | |
| recipe_id | int FK → recipes | Which recipe generated this |
| recipe_name | text | Denormalized (for CSV custom field) |
| recipe_version | int | Which version of the recipe |
| | | |
| **Generated Content** | | |
| selected_approach | text | Which approach ran |
| email_1_variant_a | text | Primary email 1 |
| email_1_variant_b | text | A/B variant |
| email_2_variant_a | text | Primary email 2 |
| email_2_variant_b | text | A/B variant |
| email_3_variant_a | text | Primary email 3 |
| email_3_variant_b | text | A/B variant |
| company_summary | text | Website scrape output |
| | | |
| **Batch Tracking** | | |
| batch_id | text | Groups leads processed together |
| | | |
| **Campaign Lifecycle** | | |
| status | text | generated / sent / replied / bounced |
| campaign_name | text | Sequencer campaign name (set when sent) |
| sequencer_type | text | smartlead / instantly / emailbison |
| sent_at | timestamptz | When uploaded to sequencer |
| | | |
| **Feedback (from Sequencer API)** | | |
| reply_type | text | positive / negative / ooo / bounce / null |
| reply_at | timestamptz | When reply received |
| reply_message | text | First reply text |
| | | |
| created_at | timestamptz | When email was generated |

**Reuse check query:**
```sql
-- For a given lead, does a current-version output exist?
SELECT * FROM email_outputs eo
JOIN recipes r ON eo.recipe_id = r.recipe_id
WHERE eo.lead_id = {lead_id}
  AND r.status = 'active'
  AND eo.recipe_version = r.version
```
If a row exists → REUSE (pull existing emails). If not → GENERATE (send to Clay).

**Performance query:**
```sql
SELECT recipe_name, recipe_version,
  COUNT(*) as sent,
  COUNT(CASE WHEN reply_type IS NOT NULL THEN 1 END) as replies,
  COUNT(CASE WHEN reply_type = 'positive' THEN 1 END) as positives,
  ROUND(100.0 * COUNT(CASE WHEN reply_type IS NOT NULL THEN 1 END) / NULLIF(COUNT(*), 0), 1) as reply_rate
FROM email_outputs
WHERE client_id = {client_id} AND segment_name = {segment}
  AND status IN ('sent', 'replied')
  AND sent_at >= {start_date}
GROUP BY recipe_name, recipe_version
ORDER BY reply_rate DESC
```

---

# PART 2: WHAT HAPPENS ON CLAY

Clay is a **disposable processing layer**. Use it, get results, push back to Neon, archive the table.

---

## What Columns the Clay Operator Imports (Neon → Clay)

When the Clay operator receives a CSV of leads that need generation:

| Column in Clay | Source | Purpose |
|----------------|--------|---------|
| lead_id | Neon leads table | To match results back on push-back |
| email | Neon leads table | Lead identification + re-verification |
| first_name | Neon leads table | Used in email copy |
| last_name | Neon leads table | Used in email copy |
| company_name | Neon leads table | Used in email copy |
| company_domain | Neon leads table | Input for StoreLeads enrichment |
| company_website | Neon leads table | Input for website scrape + PageSpeed |
| job_title | Neon leads table | Used in email copy |
| industry | Neon leads table | Used in approach selector |
| monthly_visits | Neon leads table | Pre-filled if already enriched |
| employee_count | Neon leads table | Pre-filled if already enriched |
| email_verified_at | Neon leads table | Clay checks if re-verification needed |
| AOV | Neon leads table | Pre-filled if already enriched (saves Clay credits) |
| LCP | Neon leads table | Pre-filled if already enriched |
| TTI | Neon leads table | Pre-filled if already enriched |
| client_id | Neon leads table | For approach selector |
| segment_name | Neon leads table | For approach selector |

**Key:** Pre-filled enrichment fields mean Clay SKIPS enrichment for those leads. Only enriches NULLs.

---

## What the Clay Table Does (The Recipe Columns)

The Clay operator reads the `clay_instructions` field from the active recipe(s) in Neon. Those instructions tell them exactly which columns to set up. A typical Clay table has:

| Column # | Column Name | Type | What It Does |
|----------|-------------|------|-------------|
| 1-17 | Import columns | Import | All the lead data from the CSV above |
| 18 | Email Re-verify | Enrichment | Re-verifies email. Updates email_verified. Always runs. |
| 19 | StoreLeads AOV | Enrichment | Gets AOV. Only runs if AOV column is empty. |
| 20 | PageSpeed LCP/TTI | Enrichment | Gets LCP + TTI. Only runs if empty. |
| 21 | SimilarWeb Visits | Enrichment | Gets monthly visits. Only runs if empty. |
| 22 | Website Scrape | Claygent | Scrapes company website → 50-100 word summary |
| 23 | Approach Selector | Formula | Checks data availability → picks recipe for each lead |
| 24 | Selected Recipe Text | Formula | Pulls the right approach_content based on selector |
| 25 | Researcher | Claygent | Web research for signals. Only runs when recipe requires it. |
| 26 | Copywriter | Use AI (GPT-4o-mini) | Writes email_1/2/3_variant_a/b |
| 27 | Style Checker | Use AI (GPT-4o-mini) | Fixes spam words, humanizes, breaks linear flow |
| 28 | Recipe Name | Formula | Which recipe this lead got (for tracking) |
| 29 | Recipe Version | Formula | Which version (for tracking) |

**The approach selector formula is part of the recipe instructions.** When the strategist creates recipes, they define the selector logic:
```
IF AOV is not null AND review_count > 50 → "ROI Calculator"
ELSE IF research is available → "Insider Remark"
ELSE → "Page Speed Angle" (or whatever the fallback is)
```
This formula goes in Column 23. The Clay operator pastes it.

---

## What the Clay Operator Pushes Back (Clay → Neon)

After Clay finishes processing, the operator exports a CSV. The push-back script splits this into TWO updates:

**Update 1: → email_outputs table (INSERT)**

| Field | Source Clay Column |
|-------|-------------------|
| lead_id | Column 1 (lead_id from import) |
| recipe_id | Which recipe generated this |
| recipe_version | Column 29 (version number) |
| selected_approach | Which approach ran |
| email_1_variant_a | From style checker output (styled version) |
| email_1_variant_b | A/B variant |
| email_2_variant_a | From copywriter output |
| email_2_variant_b | A/B variant |
| email_3_variant_a | From copywriter output |
| email_3_variant_b | A/B variant |
| company_summary | Column 22 (website scrape) |
| batch_id | Generated at push-back time (e.g., "hector-retail-2026-03-28") |
| client_id, segment_id | From import columns |

**Update 2: → leads table (UPDATE existing rows)**

| Field | Source Clay Column | Notes |
|-------|-------------------|-------|
| email_verified | Column 18 output | Updated to current status |
| email_verified_at | NOW() | If Clay re-verified |
| AOV | Column 19 output | Only if was NULL, now enriched |
| LCP | Column 20 output | Only if was NULL, now enriched |
| TTI | Column 20 output | Only if was NULL, now enriched |
| monthly_visits | Column 21 output | Only if was NULL, now enriched |

**Important:** Enrichment data goes to `leads` table (permanent, approach-agnostic). Email content goes to `email_outputs` table (per recipe, versioned).

---

# PART 3: A TYPICAL DAY — EVERY SCENARIO

30 clients. Each has 1-4 segments. Each segment has 1-5 active recipes.

---

## COPY STRATEGIST'S DAY (Mayank)

### Morning: Weekly Planning (Monday, 30 min)

```
Opens Claude Code (GTM-CC project).

"Show me all clients' status"

Claude Code queries Neon:

CLIENT STATUS — WEEK OF MARCH 28
──────────────────────────────────────────────────────────────
Client          | Segments | Active Recipes | Pending Leads | Action
Hector          | 3        | 7              | 12,400        | On track
Owner.com       | 2        | 4              | 3,200         | Need new recipe for Catering segment
Acme Corp       | 1        | 3              | 8,900         | On track
BrightFlow      | 2        | 5              | 1,100         | LOW — needs TAM expansion
ClientX         | 1        | 2              | 15,000        | On track
... (25 more clients)
──────────────────────────────────────────────────────────────

Actions:
1. Owner.com needs a recipe for the new Catering segment
2. BrightFlow running low on TAM — flag data team
3. Review performance for Hector (recipe changes last week)
```

### Task 1: Create New Recipe (Owner.com Catering)

```
"Pull up Owner.com"

Claude Code queries Neon (clients table):
  Shows: USPs, case studies, pain points, ICP details

"Pull Owner.com leads in the Catering segment"

Claude Code queries Neon (leads table):
  Shows: 850 leads, 780 verified, 0 contacted

"Create a recipe for Owner.com Catering"

→ Runs email-approach-generator skill
→ Uses Owner.com context from Neon
→ Copy Strategist brainstorms with Claude Code
→ Creates recipe: "Commission Savings"
→ Declares: needs AOV + delivery_platform data
→ Writes Clay instructions:
    "Column A: StoreLeads enrichment (domain → AOV)
     Column B: Re-verify email
     Column C: Website Scrape (Claygent) — [prompt]
     Column D: Copywriter (Use AI) — paste approach below
     Column E: Style Checker (Use AI) — [prompt]
     No approach selector needed (single recipe for now)"

"Test on 50 leads"

→ Claude Code pulls 50 leads from Neon
→ Runs pipeline (HTTP fetch + GPT-4o-mini)
→ Shows 10 emails in chat:
    "Lead 1: Marco, Sal's Catering — email about commission savings"
    "Lead 2: Sofia, Casa Catering — email about direct ordering"
    ...
→ Copy Strategist reviews, gives feedback
→ "The opener is too aggressive. Soften the proxy language."
→ Claude Code adjusts approach_content
→ Reruns on 10 leads
→ "Good. Save it."

"Save recipe for Owner.com Catering, version 1, status active"

→ Claude Code inserts into Neon recipes table
→ Done. 15 minutes.
```

### Task 2: Update Existing Recipe (Hector Retail)

```
"Show Hector Retail performance last 30 days"

Claude Code queries Neon (email_outputs):

HECTOR RETAIL — MARCH 2026
───────────────────────────────────
ROI Calculator v2:  1,200 sent → 3.0% reply
Insider Remark v3:  900 sent → 2.0% reply
Page Speed v1:      500 sent → 0.8% reply  ← underperforming
───────────────────────────────────

"Page Speed is not working. Let me rework the opener."

→ "Show me Page Speed v1 approach content"
→ Claude Code pulls from Neon recipes table
→ Copy Strategist edits the opener
→ Tests on 10 leads
→ "Better. Save as Page Speed v2."

Claude Code:
→ Inserts new row: Page Speed Angle v2, status=active
→ Old row: Page Speed Angle v1, status=inactive
→ Updates clay_instructions if enrichment changed
→ Done. 10 minutes.
```

### Task 3: Review and Decide (Across All Clients)

```
"Show me bottom 5 recipes by reply rate across all clients this month"

Claude Code queries Neon:

LOWEST PERFORMING RECIPES — MARCH 2026
───────────────────────────────────
Client     | Segment  | Recipe              | Sent  | Reply%
BrightFlow | Agency   | Cold Intro v1       | 800   | 0.2%
Acme       | Enter.   | Value Stack v2      | 600   | 0.5%
ClientX    | Retail   | Product Demo v1     | 1,200 | 0.6%
Hector     | Retail   | Page Speed v1       | 500   | 0.8%
Owner.com  | Rest.    | Customer Empathy v1 | 400   | 0.9%
───────────────────────────────────

Decisions:
- Kill BrightFlow Cold Intro (0.2% is infrastructure issue or bad recipe)
- Rework Acme Value Stack
- Page Speed already updated to v2
- Customer Empathy: test one more month before killing
```

---

## CAMPAIGN OPERATOR'S DAY (Hassan)

### Morning: Check Slack (8:00 AM, 5 min)

```
SLACK BOT ALERT — DAILY CAMPAIGN STATUS
────────────────────────────────────────

🔴 URGENT (< 2 days of leads):
  Owner.com Restaurant: 180 leads left, ~1.5 days
  BrightFlow Enterprise: 50 leads left, ~0.5 days

🟡 PREPARE (< 5 days):
  Hector Retail: 600 leads left, ~4 days
  ClientX Retail: 400 leads left, ~3 days

🟢 ON TRACK (5+ days):
  Acme Corp Agency: 2,100 leads left, ~14 days
  ... (25 more clients)

🔴 INFRA ALERT:
  BrightFlow Enterprise Campaign #14: 0% reply after 8 days. Check domains.
────────────────────────────────────────
```

### Scenario A: Need More Leads, Same Recipe (Most Common — 60% of days)

```
"Owner.com Restaurant needs 2,000 leads. Same recipes."

Campaign operator queries Neon (or dashboard):

OWNER.COM RESTAURANT — BATCH PREP
──────────────────────────────────
Active recipes: Math v2, Insider Remark v3
Eligible leads: 3,200
  - 1,400 already have email_outputs with current recipe versions → REUSE
  - 1,800 need generation → SEND TO CLAY

Action plan:
  1. Export 1,400 REUSE leads CSV from Neon (instant)
  2. Export 800 GENERATE leads CSV for Clay operator
     (only need 800 more to hit 2,000 total, not all 1,800)
  3. Hand GENERATE CSV to Clay operator with note:
     "Owner.com Restaurant. 800 leads. Recipes: Math v2 + Insider Remark v3."
  4. Wait for Clay operator to push back results
  5. Combine REUSE + GENERATE → final 2,000-lead CSV
  6. Upload to Smartlead → new campaign
  7. Update email_outputs: status → "sent", campaign_name, sent_at

Time: 15 min (excluding Clay processing wait)
```

### Scenario B: Recipe Changed, Need to Regenerate (Weekly — 20% of days)

```
"Hector Retail: strategist updated Page Speed to v2.
Need to run next batch with new recipe."

Campaign operator queries Neon:

HECTOR RETAIL — BATCH PREP
──────────────────────────────────
Active recipes: ROI Calculator v2, Insider Remark v3, Page Speed v2 (NEW)
Eligible leads: 2,500
  - 800 have ROI Calculator v2 outputs → REUSE
  - 600 have Insider Remark v3 outputs → REUSE
  - 0 have Page Speed v2 outputs → ALL need generation (v1 outputs exist but outdated)
  - 1,100 completely new leads → need generation

Split:
  REUSE: 1,400 leads (ROI Calculator + Insider Remark, current versions)
  GENERATE: 1,100 leads (new leads + leads eligible for Page Speed v2)

Action:
  1. Export 1,400 REUSE CSV from Neon (instant)
  2. Export 1,100 GENERATE CSV for Clay operator
     "Hector Retail. 1,100 leads. NOTE: Page Speed recipe updated to v2.
      Clay operator needs to update the approach text in the Clay template."
  3. Wait for Clay push-back
  4. Combine → final CSV → Smartlead

Time: 15 min + Clay wait
```

### Scenario C: Bad Infrastructure, Rerun Same Emails (Monthly — 10% of days)

```
"BrightFlow Enterprise: 0% reply rate after 8 days. Bad domains."

Campaign operator decision: same emails, new infrastructure.

Action:
  1. Query Neon email_outputs:
     "All email_outputs for BrightFlow Enterprise, campaign #14, status=sent"
     → 500 leads with their email_1/2/3_variant_a/b
  2. Export CSV from Neon (instant — emails already stored)
  3. NO Clay run needed. No regeneration. No cost.
  4. Upload to Smartlead → NEW campaign with fresh sending domains
  5. Update email_outputs:
     - Old campaign #14 rows: keep as-is (historical)
     - Create new email_output rows? No — same emails, just resent
     - Update campaign_name on existing rows? Or create new batch?
     → DECISION: Create new email_output rows with same emails,
       new campaign_name, new sent_at. This way both sends are tracked.

Time: 10 min. Zero Clay credits.
```

### Scenario D: New Client, First Campaign Ever (Monthly — 5% of days)

```
"New client FreshMart just onboarded. Copy Strategist created 2 recipes.
Data team verified 2,000 leads. First campaign."

Action:
  1. ALL leads are new → ALL need generation → ALL go to Clay
  2. Export 2,000 leads from Neon → CSV for Clay operator
  3. "FreshMart Retail. 2,000 leads. First run.
      Recipes: Value Prop v1 + Social Proof v1.
      Clay template: create new template per instructions."
  4. Wait for Clay push-back
  5. Export final CSV → upload to sequencer
  6. Update email_outputs: status → "sent"

Time: 20 min + Clay processing (~30-45 min for 2,000 leads)
```

### Scenario E: Re-approach After 30-Day Cooldown (Monthly per client)

```
"Hector Retail: 1,800 leads contacted in February, no reply.
30-day cooldown passed. Eligible for re-approach."

Query Neon:
  leads WHERE client=Hector, segment=Retail,
    lead_status='contacted', cooldown_until < NOW(),
    lead_status != 'replied', lead_status != 'dnc'
  → 1,800 eligible

These leads HAVE email_outputs from February, but we WANT new emails
because research will find different signals and the copy should be fresh.

Decision: REGENERATE all 1,800 through Clay.
  (Even if same recipe, the researcher + copywriter will produce
   different output because of new research findings.)

Action:
  1. Export 1,800 leads → Clay
  2. Clay runs recipe → generates fresh emails
  3. Push back → NEW email_output rows (old ones preserved for history)
  4. Export CSV → sequencer → new campaign

Time: 20 min + Clay processing
```

### Scenario F: Add Leads to Existing Live Campaign (Rare — 5% of days)

```
"Hector Retail Campaign #22 is running well (3% reply rate).
Want to add 500 more leads to the same campaign."

This is NOT adding to the same sequencer campaign.
This is a NEW sequencer campaign with the same recipe configuration.

Action:
  1. Pull 500 new leads (or reuse-eligible leads)
  2. Same flow as Scenario A or B
  3. Upload to sequencer as NEW campaign (Campaign #23)
  4. Track separately but same recipe_name/version for performance

Note: You never add leads to a running sequencer campaign.
Each batch = new campaign = clean tracking.
```

### End of Day: Mark Sent Batches

```
For each batch uploaded today:
  Update email_outputs:
    status → "sent"
    campaign_name → "hector_retail_march_batch3"
    sequencer_type → "smartlead"
    sent_at → NOW()
```

---

## CLAY OPERATOR'S DAY

### Morning: Check Assignments (8:30 AM)

```
Opens dashboard (or Neon query):

PENDING CLAY RUNS
───────────────────────────────────────────────
Assignment                  | Leads | Recipes          | From
Owner.com Restaurant        | 800   | Math v2, IR v3   | Campaign Operator
Hector Retail               | 1,100 | ROI v2, IR v3, PS v2 | Campaign Operator
FreshMart Retail (NEW)      | 2,000 | VP v1, SP v1     | Campaign Operator
───────────────────────────────────────────────
Total: 3,900 leads to process today
```

### For Each Assignment: Step by Step

```
ASSIGNMENT: Owner.com Restaurant, 800 leads

STEP 1: Read recipe instructions
  → Query Neon: SELECT clay_instructions FROM recipes
    WHERE client_id = {owner_com} AND segment_name = 'Restaurant' AND status = 'active'
  → Gets step-by-step instructions for each active recipe

STEP 2: Prepare Clay table
  → Clone "Owner.com Restaurant Template" (if exists)
  → OR create new table and follow clay_instructions:
    "Column 1-17: Import lead data
     Column 18: Email re-verification (Neverbounce enrichment)
     Column 19: StoreLeads enrichment → input: company_domain → output: AOV
     Column 20: Website Scrape Claygent → [prompt text]
     Column 21: Approach Selector → [formula: IF AOV not null → 'Math', ELSE → 'Insider Remark']
     Column 22: Selected Approach Text → [formula: pulls approach_content based on selector]
     Column 23: Researcher Claygent → [prompt text] → only runs when selector picks Insider Remark
     Column 24: Copywriter Use AI → [prompt text with variables]
     Column 25: Style Checker Use AI → [prompt text]
     Column 26: Recipe Name → [formula from selector]
     Column 27: Recipe Version → [static: current version number]"

STEP 3: Import leads
  → Import the 800-lead CSV that campaign operator prepared
  → Pre-filled AOV/LCP values stay (Clay won't re-enrich those)

STEP 4: Run the table
  → Clay processes all rows: verify → enrich → scrape → select → research → write → style
  → Processing time: ~20-40 min for 800 leads

STEP 5: Check results
  → Spot-check 5-10 rows: are emails generated? Any errors?
  → If some rows failed: check error column, may need to rerun individual rows

STEP 6: Export and push back
  → Export full Clay table as CSV
  → Run push-back script:
    python push_to_neon.py --csv clay_export.csv --client owner-com --segment restaurant --batch-id "owner-com-rest-2026-03-28"
  → Script splits output:
    - email_outputs table: emails + recipe tracking
    - leads table: enrichment updates (AOV, email_verified_at, etc.)

STEP 7: Confirm and archive
  → Check Neon: "800 new email_output rows for Owner.com Restaurant? ✓"
  → Archive Clay table (or delete)
  → Notify campaign operator: "Owner.com Restaurant batch ready in Neon."

Time per assignment: ~10 min setup + 20-40 min processing + 10 min push-back = ~40-60 min
```

### When Recipe Has Changed Since Last Run

```
ASSIGNMENT: Hector Retail, 1,100 leads
NOTE FROM CAMPAIGN OPERATOR: "Page Speed recipe updated to v2.
  Update approach text in Column 22 and Style Checker in Column 25."

Clay operator:
  1. Opens existing Hector Retail Clay template
  2. Updates Column 22 (Copywriter prompt) with new Page Speed v2 approach_content
     → Gets the new text from Neon: SELECT approach_content FROM recipes
       WHERE recipe_name = 'Page Speed Angle' AND version = 2
  3. Updates Column 25 (Style Checker) if it changed
  4. Everything else stays the same (enrichment columns, selector, etc.)
  5. Import leads, run, export, push back — same as always

Time: +5 min for the template update. Rest is same.
```

### When It's a Brand New Client (No Template Exists)

```
ASSIGNMENT: FreshMart Retail (NEW), 2,000 leads

Clay operator:
  1. No existing template → create from scratch
  2. Read clay_instructions from Neon (very detailed, step by step)
  3. Set up each column per instructions
  4. This takes longer: ~30-45 min for first-time setup
  5. Save as "FreshMart Retail Template" for future runs
  6. Import leads, run, export, push back

Time: ~45 min setup (first time only) + processing + push-back
```

---

## AUTOMATED PROCESSES (Running in Background)

### Sequencer API Sync (Every 4 Hours)

```
Script/cron job runs:

FOR each sequencer (Smartlead, Instantly, EmailBison):
  1. Connect to sequencer API
  2. Pull all lead statuses updated since last sync
  3. For each lead:
     - Match by email + campaign_name to find email_output row in Neon
     - Update:
       status → "replied" (if replied)
       reply_type → positive / negative / ooo / bounce
       reply_at → timestamp
       reply_message → first reply text (if available)
  4. Log: "Synced 47 new replies across 12 clients"
```

### Low-Leads Slack Alert (Daily, 8:00 AM)

```
Script queries Neon:

FOR each active client + segment:
  total_leads = COUNT leads WHERE status = 'verified' or 'contacted'
  leads_in_active_campaigns = COUNT email_outputs WHERE status = 'sent'
  leads_remaining = leads_in_active_campaigns (pending in sequencer)

  -- Estimate from sequencer API or from send rate
  daily_send_rate = AVG leads sent per day (last 7 days)
  days_remaining = leads_remaining / daily_send_rate

  IF days_remaining < 2: → 🔴 URGENT alert
  IF days_remaining < 5: → 🟡 PREPARE alert

  -- Also check for 0% reply rate
  FOR each campaign sent > 7 days ago:
    IF reply_rate = 0%: → 🔴 INFRA ALERT

Post to Slack channel.
```

### Email Verification Check (Weekly)

```
Script queries Neon:

SELECT COUNT(*) FROM leads
WHERE email_verified_at < NOW() - INTERVAL '30 days'
  AND lead_status NOT IN ('dnc', 'replied')
GROUP BY client_id, segment_name

"2,400 leads across 8 clients need re-verification.
 These will be re-verified when they go through the next Clay run."

(No separate verification job needed — Clay handles it in the recipe.)
```

---

# PART 4: EDGE CASES AND SCENARIOS

---

## Scenario: Same Lead, Different Clients

```
john@acme.com is a lead for BOTH Hector (Retail) and Owner.com (Restaurant).

leads table:
  Row 1: lead_id=1234, client=Hector, segment=Retail, john@acme.com
  Row 2: lead_id=5678, client=Owner.com, segment=Restaurant, john@acme.com

email_outputs table:
  Output 1: lead=1234, recipe="ROI Calculator v2", email about Amazon ads
  Output 2: lead=5678, recipe="Insider Remark v3", email about delivery commissions

No conflict. Each client's pipeline is independent.

If John replies "not interested" to Hector:
  → Update lead #1234: lead_status = 'dnc' (for Hector only)
  → Lead #5678 (Owner.com) is unaffected, still contactable
```

## Scenario: Lead Gets Different Recipe on Re-approach

```
March: Lead #1234 goes through Hector Retail pipeline
  → Approach selector picks "ROI Calculator" (AOV data available)
  → email_output created: recipe=ROI Calculator v2

April: Same lead, 30-day cooldown passed, goes through pipeline again
  → New recipe added: "Page Speed Angle v1" (LCP data now enriched)
  → Approach selector might pick "Page Speed Angle" this time
     (depends on selector logic — e.g., rotate to avoid same recipe)
  → NEW email_output created: recipe=Page Speed Angle v1
  → Old ROI Calculator output preserved
  → Lead now has TWO email_output rows (March + April)

Tracking:
  execution_log or email_outputs shows:
  March: ROI Calculator v2 → no reply
  April: Page Speed Angle v1 → replied (positive)
  → Insight: Page Speed works better for this type of lead
```

## Scenario: Copy Strategist Wants to A/B Test a New Recipe

```
"I want to test 'Brand Authority' against 'ROI Calculator'
for Hector Retail. Give 250 leads to each."

Campaign operator:
  1. Pull 500 leads from Neon (no existing outputs for either recipe)
  2. Split: 250 leads go to Clay with ONLY "Brand Authority" active in selector
     250 leads go to Clay with ONLY "ROI Calculator" active in selector
  3. Or: put both active in the approach selector and let data eligibility decide
  4. Push back both batches
  5. After 2 weeks: query performance by recipe_name
     → Brand Authority: 250 sent, 2.2% reply
     → ROI Calculator: 250 sent, 3.1% reply
     → Decision: ROI Calculator wins, Brand Authority needs work

Note: The selector handles distribution automatically if both recipes are active.
But for a clean A/B test, you might want to force one recipe per batch.
```

## Scenario: Data Team Adds New TAM Mid-Month

```
Data team sources 5,000 new leads for Hector Retail.
They verify emails, push to Neon leads table.

Impact:
  - New leads have lead_status = 'verified', no email_outputs
  - Next time campaign operator queries: these appear as GENERATE leads
  - They go through Clay with the current active recipes
  - No disruption to existing campaigns or recipes
```

## Scenario: Client Churns

```
Client "BadFit Inc" churns.

Copy Strategist:
  → Update clients table: client_status = 'churned'
  → All recipes for this client: status → 'inactive'
  → All leads remain in DB (historical data, don't delete)
  → No new campaigns, no new Clay runs
  → Sequencer campaigns left to finish naturally

If client reactivates later:
  → All data is still in Neon
  → Recipes can be reactivated or new ones created
  → email_outputs from before can be reused if recipes haven't changed
```

## Scenario: Clay Table Fails Mid-Processing

```
Clay processes 600 of 800 leads, then hits a rate limit or error.

Clay operator:
  1. Export what's done (600 leads with results)
  2. Push 600 to Neon (email_outputs + enrichment)
  3. Identify 200 failed leads (no email_1 populated)
  4. Re-import 200 leads to a new Clay table
  5. Rerun recipe on just those 200
  6. Push 200 to Neon

Net result: all 800 processed, just took two passes.
```

## Scenario: Campaign Operator Uploads Wrong CSV

```
Campaign operator accidentally uploads Hector Retail CSV
to Owner.com's sequencer campaign.

Impact:
  - Wrong emails sent to wrong leads under wrong client
  - email_outputs in Neon still correctly show Hector Retail recipe
  - The sequencer campaign name will be wrong
  - No DB corruption — the error is only on the sequencer side

Fix:
  - Pause the wrong sequencer campaign immediately
  - Upload correct CSV to correct campaign
  - The Neon data is fine, no changes needed

Prevention:
  - CSV filename includes client + segment: "hector-retail-2026-03-28.csv"
  - Campaign naming convention: "{client}_{segment}_{month}_{batch}"
```

---

# PART 5: SUMMARY

## What Each Role Does Daily

| Role | Daily Tasks | Time/Day | Tools Used |
|------|------------|----------|------------|
| Copy Strategist | Review performance, update recipes, create new recipes, test on samples | 1-2 hours (across 30 clients, not per client) | Claude Code + Neon DB |
| Campaign Operator | Check Slack alerts, run reuse checks, export CSVs, upload to sequencer, track sent status | 2-3 hours | Dashboard + Neon + Sequencers |
| Clay Operator | Read recipe instructions, set up Clay tables, import leads, run tables, push results back | 3-4 hours (3-5 Clay runs per day) | Clay + Neon + push-back script |

## Neon DB Tables

| Table | Rows (at 30 clients) | Growth Rate |
|-------|---------------------|-------------|
| clients | 30 | Slow (new clients) |
| segments | ~90 (3 per client avg) | Slow |
| leads | 250K-500K | ~20K-30K/month (new TAM) |
| recipes | ~200-400 (with versions) | ~20-30/month (new + version bumps) |
| email_outputs | 500K-1M+ | ~80K-100K/month (generated emails) |

## Cost

| Item | Monthly Cost |
|------|-------------|
| Neon DB | $19-69/mo (Pro plan for this volume) |
| Clay | Per usage (existing cost, no change) |
| GPT-4o-mini (via Clay Use AI) | ~$0.005/lead × 80K = ~$400 |
| SerpAPI (via Clay Claygent) | Included in Clay cost |
| Sequencer API sync (compute) | Minimal (cron job or small server) |
| Slack notifications | Free (webhook) |
| **Total new cost** | **~$20-70/mo for Neon** (Clay cost stays the same) |
