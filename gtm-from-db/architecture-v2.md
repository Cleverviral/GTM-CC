# GTM-CC Complete Architecture v2
## One Neon DB. No Duplicate Contacts. Tag-Based Segmentation. All Leads Through Clay.

---

# PART 1: THE DATABASE (Neon)

One Neon DB. Seven tables. Migrating from Supabase — retaining the shared-contact model (no duplicates), tag-based segmentation, COALESCE dedup logic, and extra_data JSONB.

---

## Table 1: `clients`
**Source:** Tally onboarding form webhook
**Updated by:** Strategist (manual approval), Tally webhook (auto)
**Read by:** Strategist (recipe creation context), All roles (dashboards)

| Column | Type | Description |
|--------|------|-------------|
| client_id | serial PK | Auto-generated |
| client_name | text | e.g., "Hector" |
| client_website | text | e.g., "hector.com" |
| client_status | text | in_onboarding / active / paused / churned |
| primary_poc_name | text | Main client contact |
| primary_poc_email | text | |
| target_icp_details | text | Full ICP description (was on segments in v1, belongs here) |
| target_persona | text | Target personas across all segments (VP Marketing, Director Growth, etc.) |
| pain_points | text | Key pain points for this client's prospects |
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
| approved | boolean | Must be true before downstream use |
| created_at | timestamptz | |
| updated_at | timestamptz | |

**Why ICP/persona/pain_points live here, not on segments:** The strategist defines these at the client level. They inform all recipes across all segments. Segments are just groupings of contacts — they don't need their own ICP definitions. A recipe caters to a segment, using the client's ICP context.

---

## Table 2: `segments` (Simplified Registry)
**Source:** Strategist or Clay operator creates when defining contact groupings
**Updated by:** Strategist, Clay operator
**Read by:** All roles (filtering, recipe linking)

| Column | Type | Description |
|--------|------|-------------|
| segment_id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client |
| segment_name | text | e.g., "retail-csuite-30plus", "agency-decision-makers" |
| status | text | active / paused / archived |
| created_at | timestamptz | |

**UNIQUE constraint:** (client_id, segment_name)

**What this table does NOT have:** No pain_points, no persona, no icp_criteria. Those are client-level attributes. This table is purely a registry of valid segment names. It exists so recipes can link to a specific segment via FK, and so queries can filter by segment.

**How segments relate to tags:** The segment_name corresponds to a tag (or tag pattern) used on contacts. When a contact has the tag "hector-retail", it maps to segment_name "retail" under client "Hector." The tag IS the segment assignment.

---

## Table 3: `contacts` (No Duplicates — One Row Per Person)
**Source:** Data team (Apollo, SimilarWeb, etc.) → Clay for verification → Neon
**Updated by:** Clay push-back (enrichment + verification), Supabase import (migration)
**Read by:** All roles

| Column | Type | Description |
|--------|------|-------------|
| contact_id | serial PK | Auto-generated |
| | | |
| **Identity** | | |
| email | text | Unique, indexed. Primary dedup key. |
| first_name | text | |
| last_name | text | |
| full_name | text | Auto-generated from first+last if not provided |
| job_title | text | |
| linkedin_profile_url | text | |
| linkedin_username | text | Extracted from URL, indexed. Secondary dedup key. |
| | | |
| **Company** | | |
| company_name | text | |
| company_domain | text | Normalized on write (strip https://, www., paths). Indexed. |
| company_website | text | |
| company_linkedin_url | text | |
| industry | text | |
| | | |
| **Enrichment (approach-agnostic, stays forever)** | | |
| monthly_visits | int | From SimilarWeb or Clay |
| employee_count | text | TEXT — Clay sends ranges like "11-50" |
| email_verified | text | TEXT — Clay sends "yes", "true", "catchall" etc. |
| email_verified_at | timestamptz | Last verification date |
| mx_provider | text | Gmail, Outlook, etc. |
| has_email_security_gateway | text | TEXT for richer values from Clay |
| is_catchall | text | TEXT — "yes", "no", "catchall" |
| is_personal_email | boolean | Computed — true if email domain is Gmail/Yahoo/Outlook etc. |
| city | text | |
| country | text | |
| LCP | float | Largest Contentful Paint (PageSpeed) |
| TTI | float | Time to Interactive (PageSpeed) |
| AOV | float | Average Order Value (StoreLeads) |
| | | |
| **Flexible** | | |
| tags | text[] | Tag-based segmentation. e.g., ARRAY['hector-retail', 'csuite', '30plus-employees'] |
| extra_data | jsonb | Catch-all for non-standard fields from Clay. Default {}. |
| | | |
| created_at | timestamptz | |

**Constraint:** At least one of `email` or `linkedin_username` must exist.

**Dedup logic (carried from Supabase):**
1. Look up by email (primary key)
2. If not found, look up by linkedin_username
3. If found → UPDATE using COALESCE (never overwrite non-null with null)
4. If not found → INSERT

**No duplicates:** john@acme.com is ONE row, regardless of how many clients he belongs to. The `client_contacts` junction handles the per-client relationship.

**Tags:** Flexible segmentation. Tags like "hector-retail", "owner-restaurant" encode client + segment membership. Tags like "csuite", "30plus-employees" encode lead attributes. Tags are additive (merged without duplicates on update).

---

## Table 4: `client_contacts` (Junction — Per-Client Relationship + Lifecycle)
**Source:** Clay push-back, data team import, push-to-clay operations
**Updated by:** Clay operator (linking contacts to clients), Sequencer API sync (lifecycle updates)
**Read by:** All roles

| Column | Type | Description |
|--------|------|-------------|
| id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client this contact belongs to |
| contact_id | int FK → contacts | Which contact |
| segment_id | int FK → segments | Which segment (nullable — can be set later) |
| | | |
| **Per-Client Lifecycle** | | |
| lead_status | text | raw / verified / contacted / replied / dnc / bounced |
| last_contacted_at | timestamptz | When last email was actually sent (from sequencer API) |
| cooldown_until | timestamptz | last_contacted_at + 30 days |
| contacted_count | int | How many times contacted for THIS client |
| | | |
| **Audit** | | |
| clay_table_names | text[] | Which Clay tables this contact came through. Append-only. |
| added_at | timestamptz | When this contact was linked to this client |

**UNIQUE constraint:** (client_id, contact_id) — a contact links to a client exactly once.

**Why lifecycle is HERE, not on contacts:** Cooldown, contact count, and lead status are per-client. john@acme.com might be "contacted" for Hector but "verified" (not yet contacted) for Owner.com. DNC is per-client. Cooldown is per-client.

**Cross-client example:**
```
client_contacts:
  id=1 | client=Hector   | contact=john@acme.com | status=contacted | cooldown=Apr 5
  id=2 | client=Owner.com | contact=john@acme.com | status=verified  | cooldown=NULL

John is in cooldown for Hector (was contacted March 5), but available for Owner.com.
John opts out of Hector (DNC) → does NOT affect Owner.com relationship.
```

---

## Table 5: `recipes` (One Per Client-Segment, Versioned)
**Source:** Strategist creates via Claude Code + email-approach-generator skill
**Updated by:** Strategist (create, version, deactivate)
**Read by:** Clay operator (instructions), Campaign operator (reuse check), Strategist (performance review)

| Column | Type | Description |
|--------|------|-------------|
| recipe_id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client |
| segment_id | int FK → segments | Which segment |
| | | |
| **Recipe Identity** | | |
| version | int | Starts at 1, bumps on ANY change |
| status | text | active / inactive / testing |
| parent_recipe_id | int FK → recipes | Links to previous version (null for v1) |
| | | |
| **Approach Content** | | |
| approach_content | text | Full markdown: ALL approaches + approach selector logic |
| value_prop | text | Value prop text |
| lead_list_context | text | Lead list context |
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

**Only ONE active recipe per client-segment at any time.**

**Naming convention:** date-client-segment-version (e.g., 2026-03-28-hector-retail-v3)

**Version flow:**
- Create recipe → version 1, parent = null, status = testing
- Test and approve → status = active
- Edit recipe → NEW row with version 2, parent = old recipe_id, old status → inactive
- Kill recipe → status = inactive

**What's inside approach_content:** ALL the email approaches for this segment, PLUS the approach selector formula. A recipe is the complete package. When the strategist changes one approach's CTA, the whole recipe versions up.

**How clay_instructions flow to the Clay operator:**
1. Strategist writes clay_instructions as part of recipe creation
2. Saved to Neon recipes table
3. Clay operator queries: "Show me instructions for Hector Retail"
4. Gets back step-by-step: which template to clone, which columns to set up, which prompts to paste
5. If recipe version bumps → Clay operator checks if instructions changed
6. If changed → updates the Clay template accordingly
7. If only approach_content changed → operator updates the prompt columns in the template

---

## Table 6: `email_outputs` (Per Contact Per Recipe Run)
**Source:** Clay push-back (via webhook)
**Updated by:** Sequencer API sync (sent status, reply data)
**Read by:** Campaign operator (CSV export, reuse check), Strategist (performance queries)

| Column | Type | Description |
|--------|------|-------------|
| output_id | serial PK | Auto-generated |
| contact_id | int FK → contacts | Which contact |
| client_id | int FK → clients | Which client |
| segment_id | int FK → segments | Which segment |
| | | |
| **Recipe Tracking** | | |
| recipe_id | int FK → recipes | Which recipe generated this |
| recipe_version | int | Which version of the recipe |
| | | |
| **Generated Content** | | |
| subject_line | text | |
| email_1 | text | |
| email_2 | text | |
| email_3 | text | |
| company_summary | text | Website scrape output |
| research_report | text | Researcher output (if ran) |
| spam_flags | text | Flagged spam words |
| | | |
| **Campaign Lifecycle** | | |
| campaign_id | int FK → campaigns | Which sequencer campaign this went into |
| status | text | generated / sent / replied / bounced |
| sent_at | timestamptz | Actual send timestamp (from sequencer API) |
| | | |
| **Feedback (from Sequencer API)** | | |
| reply_type | text | positive / negative / ooo / bounce / null |
| reply_at | timestamptz | When reply received |
| reply_message | text | First reply text |
| | | |
| created_at | timestamptz | When email was generated |

**Never overwritten.** New recipe version = new row. Old rows preserved for history.

**Reuse check:** Does this contact have an email_output row with the current active recipe version? If yes → PASS_THRU in Clay. If no → REGENERATE.

---

## Table 7: `campaigns` (Sequencer Bridge)
**Source:** Campaign operator registers when uploading to sequencer
**Updated by:** Campaign operator (registration), Sequencer API sync (status)
**Read by:** Sync script (mapping), Strategist (performance), Campaign operator (monitoring)

| Column | Type | Description |
|--------|------|-------------|
| campaign_id | serial PK | Auto-generated |
| client_id | int FK → clients | Which client |
| segment_id | int FK → segments | Which segment |
| recipe_version | int | Which recipe version was used |
| sequencer_type | text | smartlead / instantly / emailbison |
| sequencer_campaign_id | text | The ID from the sequencer's API |
| campaign_name | text | e.g., "2026-03-28-hector-retail-v3" |
| status | text | active / completed / paused |
| created_at | timestamptz | |

**Purpose:** The sync script queries this table to know which sequencer campaign belongs to which client + segment. Without this, there's no way to map sequencer data back to Neon leads.

---

# PART 2: THREE ROLES

---

## Strategist (Mayank)
**Creates recipes. Owns strategy. Reviews performance.**

Daily tasks:
- Pull client context from Neon
- Create recipes using Claude Code + email-approach-generator skill
- All approaches, selector logic, data requirements, Clay instructions — all inside one recipe
- Test on 50 sample leads (GPT-4o-mini pipeline)
- Review 10 emails in chat, iterate, approve
- Save recipe to Neon (versioned)
- Review performance: which recipe version is working?
- Decide: keep, kill, or rework

Does NOT touch Clay or sequencers.

---

## Clay Operator (Sahil)
**Manages leads + TAM. Runs Clay. Pushes results back.**

Daily tasks:
- Sources new leads, expands TAM, works with data team
- Checks Neon: which contacts are eligible? (fresh + cooldown-cleared)
- Pulls eligible contacts WITH existing email outputs from Neon
- Pushes ALL contacts to Clay via MCP (no CSV export/import)
- Sets up or updates Clay table per recipe's clay_instructions
- Clay processes: re-verify every email → check recipe match → generate if needed
- Webhook pushes results back to Neon automatically
- Hands clean batch (verified contacts with emails) to campaign operator
- Archives Clay table after processing

Does NOT make recipe decisions or touch sequencers.

---

## Campaign Operator (Hassan)
**Makes campaigns live. Monitors delivery. Handles infra.**

Daily tasks:
- Receives ready batch from Clay operator
- Uploads to sequencer (Smartlead / Instantly / etc.)
- Registers campaign in Neon (campaigns table)
- Makes campaign live
- Monitors reply rates, domain health, inbox placement
- Bad infra? Same emails from Neon, fresh sending domains
- Does NOT manage leads, TAM, or Clay

---

# PART 3: THE COMPLETE FLOW

---

## Step 1: Strategist Creates Recipe
- Opens Claude Code, pulls client context from Neon
- Creates recipe: all approaches + selector logic + enrichment config + Clay instructions
- Tests on 50 sample leads (GPT-4o-mini)
- Reviews 10 emails in chat, iterates, approves
- Saves to Neon: recipe v1, status = active

## Step 2: Clay Operator Pulls Eligible Contacts
- Queries Neon: fresh contacts (never contacted for this client) + cooldown-cleared contacts (30+ days since last contact)
- Query joins contacts + client_contacts: WHERE lead_status IN ('verified', 'contacted') AND (cooldown_until IS NULL OR cooldown_until < NOW())
- Also pulls existing email_outputs for each contact (last_recipe_version, existing emails)
- Result: a list of contacts with their data + any existing outputs

## Step 3: Push ALL Contacts to Clay via MCP
- Claude Code pushes ALL eligible contacts to Clay via MCP (no CSV)
- Each contact carries: lead data + pre-filled enrichment + existing email outputs + current recipe version
- Fresh contacts have NULLs in existing output columns
- Cooldown-cleared contacts have their previous outputs populated

## Step 4: Clay Processes (Decision Matrix)
- Email re-verification runs on EVERY contact (always)
- Recipe match check (formula): does last_recipe_version = current active version?
- Four outcomes:
  - PASS_THRU: verified + recipe matches → existing emails pass through, no pipeline
  - REGENERATE: verified + recipe doesn't match (or new contact) → full pipeline runs
  - HOLD: not verified + recipe matches → excluded from batch, status updated
  - DEAD: not verified + recipe doesn't match → excluded, no pipeline wasted

## Step 5: Webhook Pushes Results to Neon
- Clay webhook fires for each processed contact
- For REGENERATE contacts: INSERT new email_output row (new emails, current recipe version)
- For ALL contacts: UPDATE contacts table (fresh verification status, new enrichment if any)
- For HOLD/DEAD contacts: UPDATE contacts table (email_verified = false)

## Step 6: Clay Operator Hands Batch to Campaign Operator
- Clean batch: only PASS_THRU + REGENERATE contacts (verified, with emails)
- HOLD/DEAD excluded
- Handoff is direct — campaign operator does NOT go back to DB for a separate query

## Step 7: Campaign Operator Uploads to Sequencer
- Uploads batch to sequencer
- Registers campaign in Neon campaigns table (maps sequencer campaign → client + segment + recipe version)
- Makes campaign live
- recipe_version travels as a custom field in the sequencer

## Step 8: Sequencer API Syncs Back to Neon
- Automated sync script runs every 4 hours
- Queries Neon campaigns table: get all active campaigns with their client_id, segment_id, sequencer info
- For each campaign, calls sequencer API: pull lead statuses
- Matches by email + client_id → finds exact contact and client_contacts row
- Updates:
  - SENT: email_outputs.sent_at, client_contacts.last_contacted_at, client_contacts.cooldown_until = sent_at + 30 days
  - REPLIED: email_outputs.reply_type/reply_at/reply_message, client_contacts.lead_status = 'replied'
  - BOUNCED: email_outputs.status = 'bounced', contacts.email_verified = 'false'

---

# PART 4: CLAY INTEGRATION

---

## What Gets Pushed TO Clay (via MCP)

| Column | Source | Purpose |
|--------|--------|---------|
| contact_id | contacts table | Match results back on push-back |
| email | contacts table | Re-verification + email copy |
| first_name, last_name | contacts table | Email copy |
| company_name | contacts table | Email copy |
| company_domain | contacts table | StoreLeads enrichment input |
| company_website | contacts table | Website scrape + PageSpeed input |
| job_title | contacts table | Email copy |
| industry | contacts table | Approach selector |
| monthly_visits | contacts table | Pre-filled if already enriched (Clay skips) |
| employee_count | contacts table | Pre-filled if already enriched |
| email_verified | contacts table | Current verification status |
| email_verified_at | contacts table | When last verified |
| is_catchall | contacts table | Verification context |
| mx_provider | contacts table | Verification context |
| has_email_security_gateway | contacts table | Verification context |
| AOV | contacts table | Pre-filled if already enriched |
| LCP | contacts table | Pre-filled if already enriched |
| TTI | contacts table | Pre-filled if already enriched |
| existing_subject_line | email_outputs table | For reuse check (NULL if new) |
| existing_email_1 | email_outputs table | For reuse check |
| existing_email_2 | email_outputs table | For reuse check |
| existing_email_3 | email_outputs table | For reuse check |
| last_recipe_version | email_outputs table | For recipe match check |
| current_recipe_version | recipes table | Compare against last_recipe_version |
| client_id | client_contacts | For tracking |
| segment_name | segments table | For approach selector |

---

## Clay Template Structure (from actual template export)

The Clay re-verification template has these columns:

**Import columns:**
Webhook, First Name, Last Name, Job Title, Company Name, Company Domain, Linkedin Profile Url, Email, Email Verified, Email Verified At, Is Catchall, Mx Provider, Has Email Security Gateway

**Verification waterfall:**
- Reveify Email — primary re-verification
- normal reverify — reverification for standard emails
- catchall reverify — reverification for catchall emails
- Reoon Again — secondary verification service (Reoon)

**Decision columns:**
- Verified Normal Email — is the normal email verified after reverification?
- Catchall reverifier — is the catchall email verified?
- TLDR — summary decision
- Verified Catchalls — final status on catchalls

**Output columns:**
- Reverified Emails — final set of reverified emails
- Final Email — the email to use going forward
- Updated Email Validity — status to push back to DB
- Email Verified Date — timestamp
- Update Email Validity — HTTP API callback column that pushes status back to Neon

**For the full pipeline (email generation), additional columns follow:**
- StoreLeads → AOV (conditional, skips if pre-filled)
- PageSpeed → LCP, TTI (conditional)
- Website Scrape (Claygent)
- Approach Selector (Formula)
- Selected Approach Text (Formula)
- Researcher (Claygent, conditional)
- Copywriter (GPT-4o-mini)
- Style Checker (GPT-4o-mini)
- Recipe Version (static value)
- Lead Action (PASS_THRU / REGENERATE / HOLD / DEAD)
- Final output columns (IF formulas merging pass-thru + generated)

---

## Clay Decision Matrix

Every contact gets re-verified. Every contact's last recipe version is compared to the current active version.

```
                    | Recipe MATCHES        | Recipe DOESN'T MATCH
--------------------|-----------------------|------------------------
Email VERIFIED      | PASS-THROUGH          | REGENERATE
                    | Use existing emails   | Run full pipeline
                    | No credits spent      | New email_output row
                    |                       |
Email NOT VERIFIED  | HOLD                  | DEAD (for now)
                    | Can't send, excluded  | Bad email + stale recipe
                    | DB updated            | Don't waste credits
```

---

## What Comes BACK From Clay (via Webhook)

**To email_outputs table (INSERT — only for REGENERATE/NEW contacts):**
contact_id, recipe_version, subject_line, email_1, email_2, email_3, company_summary, research_report, spam_flags, status = "generated"

**To contacts table (UPDATE — for ALL contacts):**
email_verified (fresh), email_verified_at = NOW(), AOV/LCP/TTI/monthly_visits (if newly enriched via COALESCE — only if was NULL)

**To client_contacts table (UPDATE — for HOLD/DEAD contacts):**
No status change needed — they just don't make it into the batch.

---

# PART 5: SEQUENCER INTEGRATION

---

## Campaigns Table — The Bridge

When the campaign operator uploads a batch and makes it live:
1. Creates campaign in sequencer (Smartlead/Instantly/etc.)
2. Registers in Neon campaigns table:
   - client_id, segment_id, recipe_version
   - sequencer_type, sequencer_campaign_id
   - campaign_name (e.g., "2026-03-28-hector-retail-v3")

This mapping enables the sync script to route sequencer data to the correct client + segment.

---

## API Sync — Automated Feedback Loop

Script runs every 4 hours:

1. Query Neon: all active campaigns (gets client_id, segment_id, sequencer info)
2. For each campaign, call sequencer API: pull lead statuses
3. Match leads by email + client_id (via campaigns table mapping)
4. Update Neon:

**When sequencer reports "SENT":**
- email_outputs: status = 'sent', sent_at = actual timestamp from sequencer
- client_contacts: last_contacted_at = sent timestamp, cooldown_until = sent_at + 30 days, contacted_count += 1, lead_status = 'contacted'

**When sequencer reports "REPLIED":**
- email_outputs: status = 'replied', reply_type = positive/negative/ooo, reply_at = timestamp, reply_message = text
- client_contacts: lead_status = 'replied'

**When sequencer reports "BOUNCED":**
- email_outputs: status = 'bounced'
- contacts: email_verified = 'false'
- client_contacts: lead_status = 'bounced'

---

## Cooldown Lifecycle

Cooldown is API-driven. No manual "mark as sent" step.

```
Day 1:  Contact added to Neon. lead_status = 'verified'. cooldown = NULL.
         → Eligible for batch.

Day 5:  Goes through Clay. Emails generated. Webhook pushes to Neon.
         → email_output row created, status = 'generated'.

Day 6:  Campaign operator uploads to sequencer. Campaign registered.
         → No DB change yet. Sequencer starts dripping.

Day 8:  Sequencer actually sends the email (after warmup/caps).
         API sync picks it up → updates sent_at, last_contacted_at, cooldown_until.
         → Cooldown starts from ACTUAL send date, not upload date.

Day 8-38: In cooldown. Excluded from all future batches for this client.

Day 38+: cooldown_until < NOW(). Eligible again.
          Goes back through Clay with existing outputs. Cycle repeats.
```

**Why API-driven is better:** The sequencer drips 2,000 leads over 10-15 days. With manual confirmation, all 2,000 get the same cooldown start date. With API sync, each contact gets its actual send date. Lead #1 sent March 28, lead #1,800 sent April 10 — each gets an accurate 30-day cooldown.

---

# PART 6: TAG-BASED SEGMENTATION

---

## How Tags Work

Tags are a TEXT[] array on the contacts table. They are the primary mechanism for segmentation.

**Tag types:**
- **Client-segment tags:** "hector-retail", "owner-restaurant", "speedsize-enterprise"
- **Attribute tags:** "csuite", "30plus-employees", "verified", "high-aov"
- **Campaign tags:** "march-batch-1", "reapproach-april"

**How tags relate to segments:**
The segment_name in the segments table corresponds to a tag (or tag convention) used on contacts. "hector-retail" tag = segment_name "retail" under client "Hector."

**Why tags, not just segment_id on client_contacts:**
Tags are more flexible. A contact can have multiple tags without schema changes. New segmentation criteria = new tag, no migration needed. This is how Supabase works today and it scales.

**Do we need recipe version tags?** No. Recipe version tracking lives on email_outputs (recipe_version column). Tags are for segmentation, not for recipe tracking. The reuse check compares email_outputs.recipe_version against recipes.version — no tags involved.

---

# PART 7: RECIPE MANAGEMENT

---

## How a Recipe Gets Created

1. Strategist opens Claude Code
2. "Create a recipe for Hector Retail"
3. Claude Code pulls Hector's client context from Neon (ICP, USPs, case studies, pain points)
4. Strategist brainstorms with Claude Code
5. Creates approach_content: all email approaches + selector formula
6. Declares data_variables_required: ['aov', 'lcp', 'review_count']
7. Declares enrichment_sources: ['StoreLeads for AOV', 'PageSpeed for LCP']
8. Writes clay_instructions: step-by-step for the Clay operator
9. Tests on 50 sample leads (GPT-4o-mini pipeline, run locally)
10. Reviews 10 emails in chat, iterates
11. Saves to Neon: recipe v1, status = active

---

## How Clay Instructions Flow

**What clay_instructions contains:**
```
Clay Instructions for Hector Retail v3:

1. Clone template: "Hector-Retail-Template"
2. Import columns: lead_id, email, first_name, last_name, company_name,
   company_domain, company_website, job_title, industry, AOV, LCP, TTI,
   monthly_visits, email_verified, existing_email_1, existing_email_2,
   existing_subject_line, last_recipe_version

3. Column A: Email Re-verification
   - Enrichment: Neverbounce (or Reoon)
   - Always runs on every row

4. Column B: Recipe Match Check
   - Formula: IF(last_recipe_version = 3, "MATCH", "NO_MATCH")
   - IF last_recipe_version is empty: "NEW"

5. Column C: Action Decision
   - Formula: IF(Col_A = "valid" AND Col_B = "MATCH", "PASS_THRU",
              IF(Col_A = "valid", "REGENERATE", "HOLD"))

6. Column D: StoreLeads Enrichment
   - Input: company_domain
   - Output: AOV
   - ONLY runs if Col_C = "REGENERATE" AND AOV is empty

7. Column E: PageSpeed
   - Input: company_website
   - Output: LCP, TTI
   - ONLY runs if Col_C = "REGENERATE" AND LCP is empty

8. Column F: Website Scrape (Claygent)
   - Prompt: [pasted below]
   - ONLY runs if Col_C = "REGENERATE"

9. Column G: Approach Selector
   - Formula: [pasted below]
   - Picks which approach each lead gets based on data availability

10. Column H: Copywriter (GPT-4o-mini, Use AI)
    - Prompt: [pasted below]
    - Uses approach from selector + lead data + company summary

11. Column I: Style Checker (GPT-4o-mini, Use AI)
    - Prompt: [pasted below]

12. Column J: Final Subject Line
    - Formula: IF(Col_C = "PASS_THRU", existing_subject_line, Col_H_subject)

13. Column K: Final Email 1
    - Formula: IF(Col_C = "PASS_THRU", existing_email_1, Col_I_output)

14. Column L: Final Email 2
    - Formula: IF(Col_C = "PASS_THRU", existing_email_2, Col_H_email2)

15. Column M: Recipe Version
    - Static: 3

16. Column N: Lead Action
    - = Col_C (PASS_THRU / REGENERATE / HOLD)

17. Column O: Update Neon (HTTP API / Webhook)
    - Pushes results back to Neon
    - Fires for all rows

APPROACH SELECTOR FORMULA:
IF(AOV is not null AND review_count > 50, "ROI Calculator",
IF(research available, "Insider Remark",
"Page Speed Angle"))

APPROACH TEXTS:
[Full approach markdown pasted here]

COPYWRITER PROMPT:
[Full copywriter prompt pasted here]

STYLE CHECKER PROMPT:
[Full style checker prompt pasted here]
```

**When recipe versions up:**
- Strategist updates approach_content and/or clay_instructions
- Clay operator checks: "What changed in Hector Retail v4?"
- If only approach text changed → operator updates the copywriter prompt column
- If selector logic changed → operator updates the formula column
- If enrichment sources changed → operator adds/removes enrichment columns
- Template structure stays mostly the same across versions

---

# PART 8: CAMPAIGN SCENARIOS

---

## A: New Client, First Campaign (~5% of days)
All contacts are new. All go through Clay (REGENERATE for all). Full pipeline. Clay operator hands batch to campaign operator. First campaign registered.

## B: Same Recipe, More Leads (~60% of days)
Mix of fresh + cooldown-cleared contacts. All go to Clay. Fresh = REGENERATE. Cooldown-cleared with current recipe = PASS_THRU (just re-verified, existing emails reused). Combined output handed to campaign operator.

## C: Recipe Changed (~20% of days)
Version bumped. All contacts go to Clay. Recipe match check fails for everyone (no one has outputs for new version). All = REGENERATE. New email_output rows. Old preserved for history/comparison.

## D: Bad Infrastructure (~10% of days)
0% reply rate = bad sending domains. Pull same email outputs from Neon directly (no Clay needed — emails are fine, just need fresh infra). New sequencer campaign with fresh domains. Zero regeneration.

## E: Re-approach After Cooldown (Monthly per client)
Contacts contacted 30+ days ago, no reply. Go through Clay. If recipe unchanged = PASS_THRU (existing emails reused, fresh verification). If recipe changed = REGENERATE. New campaign either way.

## F: A/B Test Recipe Versions (As needed)
Split contacts: half go through Clay with recipe v2, half with v3. Different approach selector settings. After 2 weeks, compare reply rates by recipe_version in Neon.

---

# PART 9: MIGRATION FROM SUPABASE

---

## What Carries Over (Same Patterns)

| Pattern | Status |
|---------|--------|
| Shared contacts, no duplicates | KEEP — one row per person |
| client_contacts junction table | KEEP — now carries lifecycle data (cooldown, status) |
| COALESCE dedup on upsert | KEEP — never lose enriched data |
| Domain normalization on write | KEEP — strip https://, www., paths |
| Tags for segmentation | KEEP — TEXT[] on contacts |
| extra_data JSONB catch-all | KEEP — flexible non-standard fields |
| employee_count as TEXT | KEEP — Clay sends ranges |
| email_verified/is_catchall as TEXT | KEEP — richer values from Clay |
| is_personal_email computed | KEEP — auto-detect Gmail/Yahoo |

## What Changes

| Supabase Pattern | Neon Change | Why |
|-----------------|-------------|-----|
| PostgREST REST API for Clay | Clay MCP (push) + webhook (return) | Direct integration, no REST layer needed |
| push-to-clay edge function | Claude Code MCP push | MCP handles the push |
| upsert_contact RPC per row | Webhook listener + upsert function | Same logic, different trigger |
| No segments table | Add segments (simple registry) | Needed for recipe linkage |
| No recipes table | Add recipes (versioned) | Core of the system |
| No email_outputs table | Add email_outputs | Track generated emails + lifecycle |
| No campaigns table | Add campaigns | Bridge Neon to sequencers for API sync |
| client_contacts (simple junction) | client_contacts (+ lifecycle fields) | Cooldown, status tracked per-client |
| companies (view only) | Keep as view for now | Can upgrade to real table later |

## Migration Steps

1. Create 7 tables on Neon
2. Migrate clients from Supabase (6 → expand to 30)
3. Migrate contacts from Supabase (~69K contacts)
4. Migrate client_contacts from Supabase (add lifecycle columns)
5. Create segments from existing tag patterns
6. Build upsert function on Neon (replicate COALESCE logic)
7. Set up webhook listener for Clay push-back
8. Set up sequencer API sync script
9. Test with one client (Hector) end-to-end
10. Cut over remaining clients

---

# PART 10: BUILD ORDER — 6 PHASES

---

**Phase 1: Neon Schema**
Create all 7 tables. Replicate upsert_contact logic. Test with sample data.
Needs: Neon access. Unblocks: everything.

**Phase 2: Recipe Management + Sample Testing**
CRUD for recipes via Claude Code. Test 50 leads through GPT-4o-mini pipeline. Show 10 in chat. Save to Neon.
Needs: P1 + OpenAI API + SerpAPI. Unblocks: recipe creation workflow.

**Phase 3: Clay Integration (MCP Push + Webhook Return)**
Push contacts to Clay via MCP. Receive results via webhook. Clay decision matrix (PASS_THRU / REGENERATE / HOLD). Automated push-back to Neon.
Needs: P1 + Clay MCP access + webhook endpoint. Unblocks: full pipeline.

**Phase 4: Campaigns Table + Sequencer API Sync**
Campaign registration. Automated sync: pull sends, replies, bounces from sequencer APIs. Update email_outputs + client_contacts (cooldown, status).
Needs: P3 + sequencer API access. Unblocks: feedback loop + cooldown tracking.

**Phase 5: Performance Queries + Strategist Dashboard**
Recipe version performance. Cross-client views. Bottom performers. Lead lifecycle queries.
Needs: P4. Unblocks: data-driven recipe decisions.

**Phase 6: Slack Alerts + Monitoring**
Daily check: contacts remaining per campaign. Alert when low. Flag 0% reply rate. Proactive campaign management.
Needs: P5 + Slack webhook. Unblocks: proactive ops.
