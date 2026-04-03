#!/usr/bin/env python3
"""Generate GTM-CC Architecture v3.1 PDF — simplified, V1-focused."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# Colors
BLUE = HexColor('#2563eb')
DARK_BLUE = HexColor('#1e3a5f')
PURPLE = HexColor('#7c3aed')
ORANGE = HexColor('#ea580c')
RED = HexColor('#dc2626')
TEAL = HexColor('#0d9488')
GREEN = HexColor('#16a34a')
DARK = HexColor('#18181b')
GRAY = HexColor('#71717a')
LIGHT_GRAY = HexColor('#e4e4e7')
BG_BLUE = HexColor('#eff6ff')
BG_GREEN = HexColor('#f0fdf4')
BG_ORANGE = HexColor('#fff7ed')
BG_RED = HexColor('#fef2f2')
BG_PURPLE = HexColor('#faf5ff')
BG_TEAL = HexColor('#f0fdfa')
BG_GRAY = HexColor('#f4f4f5')
BG_YELLOW = HexColor('#fefce8')
YELLOW = HexColor('#ca8a04')
WHITE = HexColor('#ffffff')

output_path = os.path.join(os.path.dirname(__file__), 'architecture-v3.pdf')
doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=25*mm, rightMargin=25*mm, topMargin=20*mm, bottomMargin=20*mm)
styles = getSampleStyleSheet()

styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=22, textColor=DARK, spaceAfter=4))
styles.add(ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11, textColor=GRAY, spaceAfter=20))
styles.add(ParagraphStyle('SH2', parent=styles['Heading2'], fontSize=13, textColor=DARK, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle('SH3', parent=styles['Heading3'], fontSize=11, textColor=PURPLE, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, textColor=DARK, leading=14, spaceAfter=6))
styles.add(ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=8.5, textColor=GRAY, leading=12, spaceAfter=4))
styles.add(ParagraphStyle('TC', parent=styles['Normal'], fontSize=8, leading=11))
styles.add(ParagraphStyle('TH', parent=styles['Normal'], fontSize=8, leading=11, fontName='Helvetica-Bold', textColor=WHITE))
styles.add(ParagraphStyle('PT', parent=styles['Heading1'], fontSize=14, textColor=WHITE, spaceBefore=0, spaceAfter=0))

story = []
W = doc.width

def sp(h=6): story.append(Spacer(1, h))
def hr():
    sp(8); story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY)); sp(8)

def part(text, color):
    t = Table([[Paragraph(text, styles['PT'])]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(-1,-1),14),('ROUNDEDCORNERS',[6,6,6,6])]))
    story.append(t); sp(10)

def tbl(headers, rows, cw=None):
    hp = [Paragraph(h, styles['TH']) for h in headers]
    data = [hp] + [[Paragraph(str(c), styles['TC']) for c in r] for r in rows]
    if not cw: cw = [W/len(headers)]*len(headers)
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),WHITE),('ALIGN',(0,0),(-1,-1),'LEFT'),('VALIGN',(0,0),(-1,-1),'TOP'),('FONTSIZE',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('GRID',(0,0),(-1,-1),0.5,LIGHT_GRAY),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,BG_GRAY])]))
    story.append(t); sp(8)

def box(text, bg=BG_BLUE, tc=BLUE):
    p = Paragraph(text, ParagraphStyle('bx', parent=styles['Body'], fontSize=9, textColor=tc, leading=13))
    t = Table([[p]], colWidths=[W-4])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('ROUNDEDCORNERS',[4,4,4,4])]))
    story.append(t); sp(8)

# ==================== TITLE ====================
story.append(Paragraph('GTM-CC Architecture v3.1', styles['Title2']))
story.append(Paragraph('5 Tables \u00b7 No Duplicate Contacts \u00b7 segment_ids[] Segmentation \u00b7 All Leads Through Clay \u00b7 3 HTTP Columns Push-Back', styles['Subtitle']))
story.append(Paragraph('V1 Scope: Multiple Clients \u00b7 ~250K-500K Leads \u00b7 No lifecycle tracking \u00b7 No sequencer API sync \u00b7 Manual performance tracking via CSV custom fields', styles['BodySmall']))
hr()

# ==================== PART 1: DATABASE ====================
part('PART 1: THE DATABASE \u2014 5 Tables on Neon', DARK_BLUE)

story.append(Paragraph('Migrating from Supabase. Retaining: shared contacts (no duplicates), COALESCE dedup, extra_data JSONB. Adding: segments registry, recipes, email_outputs. Outputs pushed from Clay via 3 HTTP columns directly to Neon SQL-over-HTTP.', styles['Body']))

# --- clients ---
story.append(Paragraph('Table 1: clients', styles['SH2']))
story.append(Paragraph('<b>Source:</b> Tally onboarding webhook &nbsp;|&nbsp; <b>1 per client</b> &nbsp;|&nbsp; <b>ICP, persona, pain_points live HERE</b>', styles['BodySmall']))
tbl(['Column','Type','Description'], [
    ['client_id','serial PK','Auto-generated'],
    ['client_name','text','e.g., "Hector"'],
    ['client_website','text','e.g., "hector.com"'],
    ['client_status','text','in_onboarding / active / paused / churned'],
    ['primary_poc_name / email','text','Main client contact'],
    ['target_icp_details','text','Full ICP description \u2014 lives on client, NOT segment'],
    ['target_persona','text','Target personas across all segments (VP Marketing, etc.)'],
    ['pain_points','text','Key pain points \u2014 client-level, informs all recipes'],
    ['client_usp_differentiators','text','USPs and differentiators'],
    ['all_client_sales_resources','text','Case studies, FAQs, resources'],
    ['all_social_proof_brand_names','text','Logo wall brands'],
    ['client_call_to_action','text','What client wants prospects to do'],
    ['complimentary_sales_value','text','Free offer / lead magnet'],
    ['casestudy_or_leadmagnet_links','text','Links for autoresponder'],
    ['dnc_list_url','text','Do Not Contact list'],
    ['client_crm','text','hubspot / pipedrive / salesforce'],
    ['notification_channels','text','slack / email / both'],
    ['slack_main_channel_id','text',''],
    ['ar_mode','text','all_manual / first_auto / all_auto'],
    ['ar_context_doc','text','Autoresponder context doc link'],
    ['approved','boolean','Must be true before downstream use'],
    ['created_at / updated_at','timestamptz',''],
], [W*0.22, W*0.12, W*0.66])

box('<b>ICP, persona, pain_points are CLIENT-level.</b> They inform all recipes across all segments. Segments are just groupings \u2014 they don\'t need their own ICP definitions.', BG_BLUE, BLUE)

# --- segments ---
story.append(Paragraph('Table 2: segments (Registry)', styles['SH2']))
story.append(Paragraph('<b>Purpose:</b> Registry of valid segments per client. segment_id (PK) is what lives on leads.segment_ids[]. &nbsp;|&nbsp; <b>2\u20135 per client</b>', styles['BodySmall']))
tbl(['Column','Type','Description'], [
    ['segment_id','serial PK','Auto-generated. This ID is stored in leads.segment_ids[].'],
    ['client_id','int FK \u2192 clients','Which client'],
    ['segment_name','text','e.g., "1M+ Qualified"'],
    ['segment_tag','text','Human-readable label (e.g., "speedsize-1m-plus-qualified"). For display.'],
    ['description','text','What this segment targets'],
    ['status','text','active / paused / archived'],
    ['created_at','timestamptz',''],
], [W*0.20, W*0.18, W*0.62])

box('<b>segment_id is the key link.</b> leads.segment_ids[] stores an array of segment_id integers. To query leads for a segment: WHERE segment_id = ANY(segment_ids). One lead can belong to multiple segments across multiple clients.', BG_PURPLE, PURPLE)

# --- leads ---
story.append(Paragraph('Table 3: leads (One Row Per Person \u2014 No Duplicates)', styles['SH2']))
story.append(Paragraph('<b>Source:</b> Data team + Clay enrichment. Migrated from Supabase contacts table. &nbsp;|&nbsp; <b>250K-500K rows</b>', styles['BodySmall']))
tbl(['Column','Type','Description'], [
    ['lead_id','serial PK','Auto-generated'],
    ['','',''],
    ['\u2014 IDENTITY \u2014','',''],
    ['email','text','Unique, indexed. Primary dedup key.'],
    ['first_name / last_name','text',''],
    ['full_name','text','Auto-generated from first+last'],
    ['job_title','text',''],
    ['linkedin_profile_url','text',''],
    ['linkedin_username','text','Extracted from URL. Secondary dedup key. Indexed.'],
    ['','',''],
    ['\u2014 COMPANY \u2014','',''],
    ['company_name','text',''],
    ['company_domain','text','Normalized on write (strip https://, www., paths). Indexed.'],
    ['company_website','text',''],
    ['company_linkedin_url','text',''],
    ['industry','text',''],
    ['','',''],
    ['\u2014 ENRICHMENT \u2014','',''],
    ['monthly_visits','int','From SimilarWeb or Clay'],
    ['employee_count','text','TEXT \u2014 Clay sends ranges like "11-50"'],
    ['email_verified','text','TEXT \u2014 Clay sends "yes", "true", "catchall"'],
    ['email_verified_at','timestamptz','Last verification date'],
    ['mx_provider','text','Google, Microsoft, etc.'],
    ['has_email_security_gateway','text','TEXT for richer Clay values'],
    ['is_catchall','text','TEXT \u2014 "yes", "no", "catchall"'],
    ['is_personal_email','boolean','Computed: true if Gmail/Yahoo/Outlook'],
    ['city / country','text',''],
    ['LCP','float','Largest Contentful Paint (PageSpeed)'],
    ['TTI','float','Time to Interactive (PageSpeed)'],
    ['AOV','float','Average Order Value (StoreLeads)'],
    ['','',''],
    ['\u2014 SEGMENTATION \u2014','',''],
    ['segment_ids','int[]','Array of segment IDs. Values from segments.segment_id. e.g., [1, 5] means this lead belongs to segment 1 and segment 5.'],
    ['info_tags','text[]','Additional context tags. Free-form with prefix convention. e.g., ["src:apollo", "qualified:feb26"]'],
    ['','',''],
    ['\u2014 FLEXIBLE \u2014','',''],
    ['extra_data','jsonb','Catch-all for non-standard Clay fields. Default {}. Merged with || operator (new keys added, existing preserved).'],
    ['','',''],
    ['created_at','timestamptz',''],
], [W*0.24, W*0.12, W*0.64])

box('<b>ONE row per person. No duplicates. segment_ids INT[]</b> stores which segments (across clients) a lead belongs to. Query: WHERE segment_id = ANY(segment_ids). info_tags = free-form context (source, qualification, batch markers). Same lead can have segment_ids for multiple clients. Dedup: email first, linkedin_username second. COALESCE on update. <b>No lifecycle fields in V1.</b>', BG_GREEN, GREEN)

story.append(PageBreak())

# --- recipes ---
story.append(Paragraph('Table 4: recipes (One Per Client-Segment, Versioned)', styles['SH2']))
story.append(Paragraph('<b>Source:</b> Strategist via Claude Code &nbsp;|&nbsp; <b>~200-400 rows</b> (with version history)', styles['BodySmall']))
tbl(['Column','Type','Description'], [
    ['recipe_id','serial PK','Auto-generated'],
    ['client_id','int FK \u2192 clients','Which client'],
    ['segment_id','int FK \u2192 segments','Which segment'],
    ['version','int','Starts at 1, bumps on ANY change'],
    ['status','text','active / inactive / testing'],
    ['parent_recipe_id','int FK \u2192 recipes','Links to previous version (null for v1)'],
    ['','',''],
    ['\u2014 APPROACH CONTENT \u2014','',''],
    ['approach_content','text','ALL approaches as markdown (structure TBD \u2014 Clay recipe being redesigned)'],
    ['value_prop','text','Value proposition document (shared across all approaches)'],
    ['lead_list_context','text','Lead list context (targeting criteria, sales triggers)'],
    ['','',''],
    ['\u2014 DATA REQUIREMENTS \u2014','',''],
    ['data_variables_required','text[]','e.g., [\'aov\', \'review_count\']'],
    ['enrichment_sources','text[]','e.g., [\'StoreLeads for AOV\', \'PageSpeed for LCP\']'],
    ['','',''],
    ['\u2014 CLAY OPERATOR INSTRUCTIONS \u2014','',''],
    ['clay_template_name','text','Which Clay template to clone'],
    ['clay_instructions','text','Step-by-step for Clay operator (full text)'],
    ['','',''],
    ['notes','text','What changed in this version'],
    ['created_at / updated_at','timestamptz',''],
], [W*0.22, W*0.13, W*0.65])

box('<b>Only ONE active recipe per client-segment.</b> Any change (even one approach\'s CTA) = new version row, old \u2192 inactive. <b>approach_content structure is being redesigned</b> \u2014 old BQRS methodology does not apply to new Clay table format.', BG_PURPLE, PURPLE)

# --- email_outputs ---
story.append(Paragraph('Table 5: email_outputs (Per Lead Per Recipe Run)', styles['SH2']))
story.append(Paragraph('<b>Source:</b> Clay HTTP Column 3 push-back &nbsp;|&nbsp; <b>500K-1M+ rows</b> &nbsp;|&nbsp; <b>Multi-variant structure</b>', styles['BodySmall']))
tbl(['Column','Type','Description'], [
    ['output_id','serial PK','Auto-generated'],
    ['lead_id','int FK \u2192 leads','Which lead'],
    ['client_id','int FK \u2192 clients','Which client (denormalized for queries)'],
    ['segment_id','int FK \u2192 segments','Which segment'],
    ['','',''],
    ['\u2014 RECIPE TRACKING \u2014','',''],
    ['recipe_id','int FK \u2192 recipes','Which recipe generated this'],
    ['recipe_version','int','Which version (denormalized)'],
    ['selected_approach','text','Which approach from the recipe ran: "Industry Insider", "ROI Calculator", etc.'],
    ['','',''],
    ['\u2014 GENERATED CONTENT \u2014','',''],
    ['subject_line_1','text','Primary subject line'],
    ['subject_line_2','text','Alternative subject line'],
    ['email_1_variant_a / b / c','text','Email 1 \u2014 three variants (A/B/C)'],
    ['email_2_variant_a / b / c','text','Email 2 \u2014 three variants (A/B/C)'],
    ['email_3_variant_a / b / c','text','Email 3 \u2014 three variants (A/B/C)'],
    ['company_summary','text','Website scrape output'],
    ['','',''],
    ['\u2014 BATCH \u2014','',''],
    ['batch_id','text','Groups leads processed in the same Clay run'],
    ['created_at','timestamptz','When email was generated'],
], [W*0.22, W*0.15, W*0.63])

box('<b>Never overwritten.</b> New recipe version = new row. Old preserved. Multi-variant structure: 2 subject lines + 3 emails \u00d7 3 variants = 11 content columns. selected_approach tracks which approach each lead got. Query by client + segment: WHERE client_id = X AND segment_id = Y. <b>Not stored in V1:</b> campaign_id, status, sent_at, reply data. Performance tracked via sequencer dashboards + CSV custom fields.', BG_TEAL, TEAL)

story.append(Paragraph('CSV Output for Campaign Operator', styles['SH3']))
story.append(Paragraph('The CSV that the campaign operator uploads to the sequencer includes these as custom fields for manual performance tracking:', styles['Body']))
tbl(['Custom Field','Source','Purpose'], [
    ['segment_id','From leads query','Know which segment this lead belongs to'],
    ['recipe_id','From recipe','Know which recipe generated this email'],
    ['recipe_version','From recipe','Compare v2 vs v3 performance'],
    ['selected_approach','From Clay output','Know which approach ran: "Industry Insider" vs "ROI Calculator"'],
], [W*0.22, W*0.28, W*0.50])

story.append(Paragraph('What\'s NOT in V1', styles['SH3']))
tbl(['Excluded','Reason','When'], [
    ['Lifecycle tracking (last_contacted_at, cooldown_until, contacted_count)','Requires deciding manual vs API-driven. Will figure out later.','V2+'],
    ['Campaigns table','Sequencer mapping is too complex for V1.','V2+'],
    ['Sequencer API sync','No automated send/reply/bounce tracking.','V2+'],
    ['Reply storage in DB','Performance tracked via CSV custom fields in sequencer.','V2+'],
    ['research_report in email_outputs','Research is consumed during Clay processing, not needed downstream.','Never (stays in Clay)'],
], [W*0.35, W*0.40, W*0.25])

story.append(PageBreak())

# ==================== PART 2: APPROACH CONTENT ====================
part('PART 2: APPROACH CONTENT \u2014 TBD (Redesigning)', PURPLE)

story.append(Paragraph('The Clay table recipe structure is being redesigned. The details below capture what we know so far and what\'s changing.', styles['Body']))

story.append(Paragraph('What We Know', styles['SH2']))
story.append(Paragraph('\u2022 approach_content is a single TEXT field in the recipes table<br/>\u2022 It contains the complete email generation playbook for a client-segment<br/>\u2022 Multiple approaches per recipe, each with its own strategy and logic<br/>\u2022 A selector picks which approach runs for each lead<br/>\u2022 GPT-4o-mini is the only model used in the Clay pipeline<br/>\u2022 The Clay operator follows clay_instructions to set up the table', styles['Body']))

story.append(Paragraph('What\'s Changing From the Old Methodology', styles['SH2']))
tbl(['Old (from CSV export)','New','Why'], [
    ['BQRS (Boolean Query Research System) for research','TBD \u2014 may not use boolean search','New methodology doesn\'t rely on BQRS'],
    ['email_body \u2014 one email output','2 subject lines + 3 emails \u00d7 3 variants (11 columns)','Multi-variant structure for A/B testing and sequencer flexibility'],
    ['Specific selector agent structure','TBD \u2014 selector logic will change','Approach selection mechanism being redesigned'],
    ['Approach documents with fixed sections','TBD \u2014 structure will change','Tied to new Clay column layout'],
    ['Clay column layout (38-40 columns)','TBD \u2014 will be redesigned','Follows from approach structure changes'],
], [W*0.30, W*0.30, W*0.40])

box('<b>Next step: design the new Clay table recipe format together.</b> Once the Clay column layout is decided, the approach_content structure and clay_instructions format will follow. Do not build this yet.', BG_YELLOW, YELLOW)

story.append(PageBreak())

# ==================== PART 3: ROLES ====================
part('PART 3: THREE ROLES', DARK)

story.append(Paragraph('Strategist (Mayank)', styles['SH2']))
story.append(Paragraph('<b>Creates recipes. Owns strategy. Reviews performance.</b><br/><br/>\u2022 Pull client context from Neon (ICP, USPs, case studies, pain_points)<br/>\u2022 Create recipes: approach documents + selector logic + enrichment config + Clay instructions<br/>\u2022 Test on sample leads (GPT-4o-mini pipeline, run locally via Claude Code)<br/>\u2022 Review emails in chat, iterate, approve<br/>\u2022 Save recipe to Neon (versioned \u2014 any change = new version)<br/>\u2022 Review performance (via sequencer dashboards + CSV custom fields)<br/>\u2022 Decide: keep, kill, or rework', styles['Body']))
box('Does NOT touch Clay or sequencers.', BG_PURPLE, PURPLE)

story.append(Paragraph('Clay Operator', styles['SH2']))
story.append(Paragraph('<b>Manages leads + TAM. Runs Clay. Hands off to campaign operator.</b><br/><br/>\u2022 Sources new leads, expands TAM, works with data team<br/>\u2022 Checks Neon: which leads are available for a given segment_id?<br/>\u2022 Pulls leads WITH existing email outputs from Neon<br/>\u2022 Claude Code pushes leads to Clay table (one lead per webhook POST)<br/>\u2022 Sets up Clay table per recipe\'s clay_instructions<br/>\u2022 Clay processes: re-verify \u2192 recipe match check \u2192 generate if needed<br/>\u2022 3 HTTP columns auto-push results back to Neon (verification, enrichment, email outputs)<br/>\u2022 Hands clean batch (CSV) to campaign operator<br/>\u2022 Archives Clay table', styles['Body']))
box('Does NOT make recipe decisions or touch sequencers.', BG_ORANGE, ORANGE)

story.append(Paragraph('Campaign Operator', styles['SH2']))
story.append(Paragraph('<b>Makes campaigns live. Monitors delivery. Handles infra.</b><br/><br/>\u2022 Receives ready batch from Clay operator (CSV with emails + custom fields)<br/>\u2022 CSV includes: segment_id, recipe_id, recipe_version, selected_approach as custom fields<br/>\u2022 Uploads to sequencer (Smartlead / Instantly / etc.)<br/>\u2022 Makes campaign live, monitors delivery<br/>\u2022 Bad infra (0% reply)? Pull same emails from Neon, fresh domains<br/>\u2022 Tracks performance via sequencer dashboard', styles['Body']))
box('Delivery only. No Clay, no recipes, no DB writes.', BG_RED, RED)

hr()

# ==================== PART 4: COMPLETE FLOW ====================
part('PART 4: THE COMPLETE FLOW \u2014 6 Steps (V1)', DARK)

story.append(Paragraph('No lifecycle tracking in V1. No cooldown mechanism. The flow is: create recipe \u2192 pull leads \u2192 push to Clay \u2192 Clay processes \u2192 3 HTTP columns push back to Neon \u2192 hand off to campaign operator.', styles['Body']))

steps = [
    ('Step 1', 'Strategist Creates Recipe', 'Opens Claude Code \u2192 pulls client context from Neon \u2192 creates recipe with all approaches, selector logic, Clay instructions \u2192 tests on sample leads (GPT-4o-mini) \u2192 saves to Neon.', 'Strategist', PURPLE),
    ('Step 2', 'Clay Operator Pulls Leads', 'Queries Neon: leads WHERE segment_id = ANY(segment_ids). Also pulls existing email_outputs for those leads (for reuse/recipe match check).', 'Clay Operator', ORANGE),
    ('Step 3', 'Push Leads to Clay via Webhook', 'Claude Code POSTs one lead at a time to Clay webhook URL. Lead data + pre-filled enrichment + existing email outputs + current recipe version all travel as JSON keys. Fresh leads have NULLs in existing output columns.', 'Clay Operator via Claude Code', ORANGE),
    ('Step 4', 'Clay Processes (Decision Matrix)', 'Re-verify every email (always). Check recipe match (formula). Outcomes:<br/>\u2022 <b>PASS_THRU:</b> verified + recipe matches \u2192 existing emails reused, no pipeline<br/>\u2022 <b>REGENERATE:</b> verified + no match or new \u2192 full pipeline runs, selected_approach assigned<br/>\u2022 <b>HOLD:</b> not verified \u2192 excluded from batch, lead marked unverified', 'Clay (automated)', ORANGE),
    ('Step 5', '3 HTTP Columns Push Results to Neon', 'Three HTTP API enrichment columns fire per row, POSTing directly to Neon\'s SQL-over-HTTP endpoint:<br/>\u2022 <b>HTTP Col 1 (Verification):</b> UPDATE leads \u2192 email_verified, email_verified_at, is_catchall<br/>\u2022 <b>HTTP Col 2 (Enrichment):</b> UPDATE leads \u2192 LCP, TTI, AOV, monthly_visits + extra_data JSONB merge<br/>\u2022 <b>HTTP Col 3 (Email Outputs):</b> INSERT email_outputs \u2192 all email variants, subject lines, selected_approach', 'Clay HTTP \u2192 Neon /sql', BLUE),
    ('Step 6', 'Hand Off + Upload to Sequencer', 'Clay operator exports clean batch: only PASS_THRU + REGENERATE leads (verified, with emails). CSV includes lead data + emails + custom fields (segment_id, recipe_id, recipe_version, selected_approach). Campaign operator uploads to sequencer.', 'Clay Op \u2192 Campaign Op', RED),
]

for sn, title, desc, who, color in steps:
    data = [[Paragraph(f'<b>{sn}</b>', ParagraphStyle('s', parent=styles['Body'], textColor=color, fontSize=10)),
             Paragraph(f'<b>{title}</b><br/>{desc}<br/><i>{who}</i>', styles['Body'])]]
    t = Table(data, colWidths=[W*0.10, W*0.90])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    story.append(t)

story.append(PageBreak())

# ==================== PART 5: CLAY INTEGRATION ====================
part('PART 5: CLAY INTEGRATION \u2014 Webhook Push + Decision Matrix + 3 HTTP Columns', ORANGE)

story.append(Paragraph('What Gets Pushed TO Clay (via Webhook)', styles['SH2']))
story.append(Paragraph('Claude Code queries Neon and POSTs one lead at a time to the Clay webhook URL. Each POST is a single JSON object \u2014 Clay auto-creates columns from JSON keys on a blank table.', styles['Body']))
tbl(['Data','Source','Purpose'], [
    ['lead_id, email, name, company, job_title, industry','leads table','Lead data for email generation'],
    ['segment_ids','leads table','Confirm segment membership'],
    ['company_domain, company_website','leads table','Enrichment inputs (StoreLeads, PageSpeed, scrape)'],
    ['AOV, LCP, TTI, monthly_visits, employee_count','leads table','Pre-filled enrichment (Clay skips if filled \u2192 saves credits)'],
    ['email_verified, email_verified_at, is_catchall, mx_provider','leads table','Current verification status (Clay re-verifies all)'],
    ['existing subject_line_1/2, email variants','email_outputs table','For reuse check (NULL if new lead)'],
    ['last_recipe_version, last_selected_approach','email_outputs table','For recipe match check'],
    ['current_recipe_version','recipes table','Compare against last_recipe_version'],
    ['Lead List Context, Value Prop','recipes table','Static \u2014 same for all leads in batch'],
    ['Approach texts','recipes.approach_content','Each approach as its own Clay column'],
], [W*0.30, W*0.25, W*0.45])

story.append(Paragraph('Clay Decision Matrix', styles['SH2']))
story.append(Paragraph('Every lead gets re-verified. Every lead\'s last recipe version is compared to current. Four outcomes:', styles['Body']))

mx = [
    [Paragraph('', styles['TH']), Paragraph('<b>Recipe MATCHES</b>', styles['TH']), Paragraph('<b>Recipe DOESN\'T MATCH / NEW</b>', styles['TH'])],
    [Paragraph('<b>Email VERIFIED</b>', ParagraphStyle('m1', parent=styles['TC'], textColor=GREEN)),
     Paragraph('<b>PASS-THROUGH</b><br/>Use existing emails. No pipeline. Zero credits on generation.', styles['TC']),
     Paragraph('<b>REGENERATE</b><br/>Full pipeline: enrich \u2192 select approach \u2192 generate email. New email_output row with selected_approach.', styles['TC'])],
    [Paragraph('<b>Email NOT VERIFIED</b>', ParagraphStyle('m2', parent=styles['TC'], textColor=RED)),
     Paragraph('<b>HOLD</b><br/>Can\'t send. Excluded from batch. Lead marked unverified in Neon.', styles['TC']),
     Paragraph('<b>HOLD</b><br/>Bad email + stale recipe. Don\'t waste credits. Lead parked.', styles['TC'])],
]
t = Table(mx, colWidths=[W*0.22, W*0.39, W*0.39])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DARK),('BACKGROUND',(1,1),(1,1),BG_GREEN),('BACKGROUND',(2,1),(2,1),BG_BLUE),('BACKGROUND',(1,2),(1,2),BG_ORANGE),('BACKGROUND',(2,2),(2,2),BG_RED),('GRID',(0,0),(-1,-1),0.5,LIGHT_GRAY),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
story.append(t); sp(10)

story.append(Paragraph('What Comes BACK From Clay (via 3 HTTP Columns)', styles['SH2']))
story.append(Paragraph('Each Clay table has three HTTP API enrichment columns that POST directly to Neon\'s SQL-over-HTTP endpoint. Auth is a static Neon connection string in the header (never expires).', styles['Body']))

tbl(['HTTP Column','Target','Fields','Pattern'], [
    ['Col 1: Verification','UPDATE leads','email_verified, email_verified_at = NOW(), is_catchall','COALESCE(NULLIF($1, \'\'), existing) \u2014 blanks don\'t overwrite'],
    ['Col 2: Enrichment','UPDATE leads','LCP, TTI, AOV, monthly_visits, employee_count, city, country + extra_data JSONB merge','COALESCE for known fields. extra_data || for JSONB merge (new keys added, existing preserved)'],
    ['Col 3: Email Outputs','INSERT email_outputs','subject_line_1/2, email_1/2/3_variant_a/b/c, selected_approach, company_summary, recipe_id, recipe_version, batch_id','INSERT \u2014 REGENERATE leads only. New row per run.'],
], [W*0.14, W*0.14, W*0.36, W*0.36])

story.append(Paragraph('<b>Not pushed back:</b> research_report (consumed in Clay), spam check results (stay in Clay)', styles['Body']))

story.append(PageBreak())

# ==================== PART 6: CLAY TEMPLATE ====================
part('PART 6: CLAY TEMPLATE STRUCTURE \u2014 Partially TBD', ORANGE)

story.append(Paragraph('Re-Verification Template (Stays As-Is)', styles['SH2']))
tbl(['Column Group','Columns','Purpose'], [
    ['Import (from Neon)','First Name, Last Name, Job Title, Company Name, Company Domain, LinkedIn URL, Email, Email Verified, Email Verified At, Is Catchall, Mx Provider, Has Email Security Gateway','Lead data from DB'],
    ['Verification Waterfall','Reveify Email \u2192 normal reverify \u2192 catchall reverify \u2192 Reoon Again','Multi-step email verification'],
    ['Decision Logic','Verified Normal Email, Catchall reverifier, TLDR, Verified Catchalls','Determines final verification status'],
    ['Output','Reverified Emails, Final Email, Updated Email Validity, Email Verified Date','Final verified email + status to push back'],
    ['Push-back','3 HTTP columns \u2192 Neon /sql','Auto-push verification, enrichment, email outputs to Neon'],
], [W*0.16, W*0.52, W*0.32])

story.append(Paragraph('Full Pipeline Template (Being Redesigned)', styles['SH2']))
story.append(Paragraph('The old pipeline assumed BQRS research methodology and a single email_body output. The new structure produces 2 subject lines + 3 emails \u00d7 3 variants.', styles['Body']))

story.append(Paragraph('What stays the same:', styles['SH3']))
story.append(Paragraph('\u2022 Import phase (lead data + existing outputs + recipe version)<br/>\u2022 Verification phase (Neverbounce / Reoon waterfall)<br/>\u2022 Decision phase (PASS_THRU / REGENERATE / HOLD formula)<br/>\u2022 Enrichment phase (StoreLeads, PageSpeed \u2014 skips if pre-filled)<br/>\u2022 GPT-4o-mini as the generation model<br/>\u2022 3 HTTP columns push-back to Neon', styles['Body']))

story.append(Paragraph('What\'s changing:', styles['SH3']))
story.append(Paragraph('\u2022 Approach column structure \u2014 TBD<br/>\u2022 Selector mechanism \u2014 TBD<br/>\u2022 Research methodology \u2014 may not use BQRS<br/>\u2022 Output format \u2014 2 subject lines + 3 emails \u00d7 3 variants (11 content columns)<br/>\u2022 Exact column count and order \u2014 TBD', styles['Body']))

box('<b>Next step: design the new Clay table recipe format together.</b> The re-verification template is production-ready. The full pipeline template needs to be redesigned before building.', BG_YELLOW, YELLOW)

hr()

# ==================== PART 7: SEGMENT_IDS SEGMENTATION ====================
part('PART 7: segment_ids[] SEGMENTATION', DARK)

story.append(Paragraph('Leads use segment_ids INT[] to store which segments they belong to. info_tags TEXT[] stores free-form contextual metadata.', styles['Body']))

story.append(Paragraph('segment_ids (Segment Membership)', styles['SH3']))
tbl(['Concept','How It Works','Example'], [
    ['Segment ID','segments.segment_id (PK) is stored in leads.segment_ids[].','segments row: segment_id=1, client=SpeedSize, name="1M+ Qualified"'],
    ['Lead assignment','Append segment_id to leads.segment_ids[] when a lead is assigned to a client-segment.','john@acme.com: segment_ids = [1]'],
    ['Query leads','WHERE segment_id = ANY(segment_ids) to get all leads for a segment.','WHERE 1 = ANY(segment_ids) \u2192 returns all SpeedSize 1M+ leads'],
    ['Multi-client','Same lead can have segment_ids for multiple clients. One row, shared enrichment.','john@acme.com: segment_ids = [1, 5] \u2192 SpeedSize 1M+ and Solara segment'],
    ['Dedup on add','If lead already exists (UNIQUE email), just append the new segment_id.','Data team adds same person for Solara \u2192 append segment_id, don\'t duplicate'],
], [W*0.18, W*0.42, W*0.40])

story.append(Paragraph('info_tags (Additional Context)', styles['SH3']))
tbl(['Prefix','Meaning','Examples'], [
    ['src:','Where the lead data came from','src:apollo, src:builtwith, src:salesnav, src:hubspot'],
    ['qualified:','When/how they were qualified','qualified:feb26, qualified:manual'],
    ['batch:','Which Clay batch processed them','batch:ss-100k-1m-set1'],
    ['(no prefix)','Legacy or general markers','hubspot-lead, 20k-plus-new'],
], [W*0.18, W*0.32, W*0.50])

box('<b>segment_ids = strict, system-driving.</b> Integer IDs from segments.segment_id. Used for queries, recipe matching, pipeline routing. <b>info_tags = free-form, contextual.</b> Source, qualification, batch markers. Useful for filtering and analysis but doesn\'t drive the pipeline.', BG_GREEN, GREEN)

hr()

# ==================== PART 8: CAMPAIGN SCENARIOS ====================
part('PART 8: CAMPAIGN SCENARIOS', DARK)

scenarios = [
    ('A: New Client, First Campaign', '~5%', 'All leads new \u2192 all REGENERATE. Full pipeline. selected_approach tracked per lead. Clay operator hands CSV to campaign operator.', GREEN),
    ('B: Same Recipe, More Leads', '~60%', 'Mix of fresh + previously processed leads. All go to Clay. Fresh = REGENERATE. Previously processed with current recipe = PASS_THRU (re-verified, existing emails reused). One batch out.', BLUE),
    ('C: Recipe Changed', '~20%', 'Version bumped. Recipe match fails for everyone. All = REGENERATE. New email_output rows. Old preserved. New selected_approach per lead.', ORANGE),
    ('D: Bad Infrastructure', '~10%', 'Same emails from Neon directly (no Clay). New sequencer campaign, fresh domains. Zero regeneration, zero cost.', RED),
    ('E: A/B Test Approaches', 'As needed', 'Same recipe, random selector assigns different approaches. selected_approach travels as a custom field to the sequencer. Reply rate comparison happens in the sequencer dashboard \u2014 DB tracks what was sent, sequencer tracks results.', PURPLE),
]
for t2, freq, desc, color in scenarios:
    data = [[Paragraph(f'<b>{t2}</b> ({freq})', ParagraphStyle('s', parent=styles['Body'], textColor=color, fontSize=9.5)),
             Paragraph(desc, styles['Body'])]]
    t = Table(data, colWidths=[W*0.32, W*0.68])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    story.append(t)

hr()

# ==================== PART 9: MIGRATION + BUILD ORDER ====================
part('PART 9: MIGRATION FROM SUPABASE + BUILD ORDER', DARK_BLUE)

story.append(Paragraph('What Carries Over', styles['SH2']))
tbl(['Pattern','Status'], [
    ['One row per person (no duplicates)','KEEP'],
    ['COALESCE dedup on upsert (never lose enriched data)','KEEP'],
    ['Domain normalization (strip https://, www.)','KEEP'],
    ['segment_ids INT[] for segmentation','KEEP \u2014 migrated from tags TEXT[] to integer IDs'],
    ['extra_data JSONB catch-all + merge with || operator','KEEP'],
    ['employee_count as TEXT (Clay sends ranges)','KEEP'],
    ['email_verified as TEXT (richer Clay values)','KEEP'],
    ['is_personal_email computed column','KEEP'],
], [W*0.50, W*0.50])

story.append(Paragraph('What Changes', styles['SH2']))
tbl(['Change','Why'], [
    ['contacts \u2192 leads (rename)','Same table, better name. No lifecycle fields in V1.'],
    ['client_contacts junction \u2192 REMOVED','segment_ids[] handles client-segment assignment.'],
    ['tags TEXT[] \u2192 segment_ids INT[]','Integer FK references instead of free-form tag strings.'],
    ['No segments \u2192 Add segments (registry)','Recipe linkage. segment_id is the key.'],
    ['No recipes \u2192 Add recipes (versioned)','Core of the system. Approach content + Clay instructions.'],
    ['No email_outputs \u2192 Add email_outputs','Track generated emails (multi-variant) + selected_approach + recipe version.'],
    ['PostgREST \u2192 Neon SQL-over-HTTP','Direct /sql endpoint. Static auth (connection string). No JWT expiry.'],
    ['push-to-clay edge function \u2192 Claude Code webhook push','Claude Code POSTs one lead at a time to Clay webhook URL.'],
    ['Supabase HTTP API \u2192 3 Clay HTTP columns','Clay pushes results directly to Neon via 3 HTTP API enrichment columns.'],
], [W*0.45, W*0.55])

story.append(Paragraph('Build Order \u2014 4 Phases (V1)', styles['SH2']))
phases = [
    ('P1','Neon Schema + Migration','Create 5 tables. Replicate upsert logic with COALESCE. Indexes on email, linkedin_username, company_domain. Migrate contacts as leads with segment_ids.','Neon access','Everything',GREEN),
    ('P2','Recipe Management + Testing','CRUD for recipes via Claude Code. Test sample leads (GPT-4o-mini). Show emails in chat. Save to Neon. Track selected_approach.','P1 + OpenAI API','Recipe workflow',PURPLE),
    ('P3','Clay Integration','Webhook push to Clay. 3 HTTP columns return. Decision matrix. Auto push-back to Neon. selected_approach tracked.','P1 + Clay webhook + HTTP columns','Full pipeline',ORANGE),
    ('P4','Operational Queries + CSV Export','Lead counts per segment_id. Batch history. Recipe version history. CSV export with custom fields for sequencer.','P3','Operational workflow',BLUE),
]
for num, title, desc, needs, unblocks, color in phases:
    data = [[Paragraph(f'<b>{num}</b>', ParagraphStyle('p', parent=styles['Body'], textColor=color, fontSize=11, alignment=TA_CENTER)),
             Paragraph(f'<b>{title}</b><br/>{desc}<br/><i>Needs: {needs} | Unblocks: {unblocks}</i>', styles['Body'])]]
    t = Table(data, colWidths=[W*0.08, W*0.92])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    story.append(t)

story.append(Paragraph('V2+ Phases (Not in V1)', styles['SH3']))
tbl(['Phase','What','Why Later'], [
    ['P5: Lifecycle Tracking','Add cooldown, last_contacted_at, contacted_count. Decide manual vs API-driven.','Requires deciding on cooldown mechanism'],
    ['P6: Campaigns + Sequencer API','Map sequencer campaigns to client+segment. Automated send/reply/bounce tracking.','Complex integration, not needed for V1'],
    ['P7: Performance Dashboard','Cross-client queries in Neon. Approach-level analysis. Automated recommendations.','Needs reply data in DB (requires P6)'],
], [W*0.22, W*0.40, W*0.38])

hr()

# ==================== DATA FLOW ====================
part('DATA FLOW SUMMARY (V1)', DARK)

flows = [
    ('Strategist \u2192 Neon','Recipe: all approaches + selector + Clay instructions + value prop + lead list context. Versioned.',PURPLE),
    ('Neon \u2192 Clay (Webhook)','Claude Code queries Neon, POSTs one lead at a time to Clay webhook URL. Lead data + segment_ids + enrichment + existing outputs + current recipe version + approach texts.',ORANGE),
    ('Clay \u2192 Neon (3 HTTP Cols)','HTTP Col 1: verification update. HTTP Col 2: enrichment + extra_data JSONB merge. HTTP Col 3: INSERT email_outputs with all variants (REGENERATE only). All via Neon /sql endpoint with static auth.',ORANGE),
    ('Clay Op \u2192 Campaign Op','CSV: verified leads with final emails + segment_id, recipe_id, recipe_version, selected_approach as custom fields.',RED),
    ('Campaign Op \u2192 Sequencer','Upload CSV. Custom fields enable performance tracking by segment \u00d7 recipe \u00d7 approach.',RED),
    ('Neon \u2192 Strategist','Lead counts per segment_id. Email output history. Recipe version tracking. Performance reviewed manually via sequencer dashboards.',PURPLE),
]
for label, desc, color in flows:
    data = [[Paragraph(f'<b>{label}</b>', ParagraphStyle('f', parent=styles['Body'], textColor=color, fontSize=9)),
             Paragraph(desc, styles['Body'])]]
    t = Table(data, colWidths=[W*0.25, W*0.75])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(t)

sp(12)
box('<b>V2+ additions:</b> Lifecycle tracking (cooldown), Campaigns table + Sequencer API sync, Performance dashboard with cross-client queries.', BG_GRAY, GRAY)

doc.build(story)
print(f"PDF generated: {output_path}")
