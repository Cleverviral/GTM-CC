#!/usr/bin/env python3
"""Generate GTM-CC Architecture v2 PDF from markdown."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
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
YELLOW = HexColor('#ca8a04')
DARK = HexColor('#18181b')
GRAY = HexColor('#71717a')
LIGHT_GRAY = HexColor('#e4e4e7')
BG_BLUE = HexColor('#eff6ff')
BG_GREEN = HexColor('#f0fdf4')
BG_ORANGE = HexColor('#fff7ed')
BG_RED = HexColor('#fef2f2')
BG_PURPLE = HexColor('#faf5ff')
BG_TEAL = HexColor('#f0fdfa')
BG_YELLOW = HexColor('#fefce8')
BG_GRAY = HexColor('#f4f4f5')
WHITE = HexColor('#ffffff')

output_path = os.path.join(os.path.dirname(__file__), 'architecture-v2.pdf')

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=25*mm, rightMargin=25*mm,
    topMargin=20*mm, bottomMargin=20*mm
)

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=22, textColor=DARK, spaceAfter=4))
styles.add(ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11, textColor=GRAY, spaceAfter=20))
styles.add(ParagraphStyle('SectionHead', parent=styles['Heading1'], fontSize=16, textColor=BLUE, spaceBefore=20, spaceAfter=8))
styles.add(ParagraphStyle('SectionHead2', parent=styles['Heading2'], fontSize=13, textColor=DARK, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle('SectionHead3', parent=styles['Heading3'], fontSize=11, textColor=PURPLE, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, textColor=DARK, leading=14, spaceAfter=6))
styles.add(ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=8.5, textColor=GRAY, leading=12, spaceAfter=4))
styles.add(ParagraphStyle('CodeBlock2', parent=styles['Normal'], fontSize=8, fontName='Courier', textColor=DARK, leading=11, leftIndent=12, spaceAfter=8, backColor=BG_GRAY))
styles.add(ParagraphStyle('Highlight', parent=styles['Normal'], fontSize=9, textColor=GREEN, leading=13, spaceAfter=4))
styles.add(ParagraphStyle('Warning', parent=styles['Normal'], fontSize=9, textColor=ORANGE, leading=13, spaceAfter=4))
styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=8, leading=11))
styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=8, leading=11, fontName='Helvetica-Bold', textColor=WHITE))
styles.add(ParagraphStyle('PartTitle', parent=styles['Heading1'], fontSize=14, textColor=WHITE, spaceBefore=0, spaceAfter=0))

story = []

def add_spacer(h=6):
    story.append(Spacer(1, h))

def add_hr():
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY))
    story.append(Spacer(1, 8))

def add_part_header(text, color):
    data = [[Paragraph(text, styles['PartTitle'])]]
    t = Table(data, colWidths=[doc.width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('ROUNDEDCORNERS', [6,6,6,6]),
    ]))
    story.append(t)
    add_spacer(10)

def add_table(headers, rows, col_widths=None):
    header_paras = [Paragraph(h, styles['TableHeader']) for h in headers]
    data = [header_paras]
    for row in rows:
        data.append([Paragraph(str(c), styles['TableCell']) for c in row])

    if col_widths is None:
        col_widths = [doc.width / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_GRAY]),
    ]))
    story.append(t)
    add_spacer(8)

def add_info_box(text, bg_color=BG_BLUE, text_color=BLUE):
    p = Paragraph(text, ParagraphStyle('box', parent=styles['Body'], fontSize=9, textColor=text_color, leading=13))
    data = [[p]]
    t = Table(data, colWidths=[doc.width - 4])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    story.append(t)
    add_spacer(8)

# ==================== TITLE ====================
story.append(Paragraph('GTM-CC Complete Architecture v2', styles['Title2']))
story.append(Paragraph('One Neon DB · No Duplicate Contacts · Tag-Based Segmentation · All Leads Through Clay · MCP Push + Webhook Return · Sequencer API Feedback Loop', styles['Subtitle']))
story.append(Paragraph('7 Tables · 3 Roles · 30 Clients · ~250K-500K Contacts · 80K-100K Emails/Month', styles['BodySmall']))

add_hr()

# ==================== PART 1: DATABASE ====================
add_part_header('PART 1: THE DATABASE (Neon) — 7 Tables', DARK_BLUE)

story.append(Paragraph('One Neon DB. Seven tables. Migrating from Supabase — retaining the shared-contact model (no duplicates), tag-based segmentation, COALESCE dedup logic, and extra_data JSONB.', styles['Body']))

# --- clients ---
story.append(Paragraph('Table 1: clients', styles['SectionHead2']))
story.append(Paragraph('<b>Source:</b> Tally onboarding form webhook &nbsp;&nbsp;|&nbsp;&nbsp; <b>~30 rows</b>', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['client_id', 'serial PK', 'Auto-generated'],
        ['client_name', 'text', 'e.g., "Hector"'],
        ['client_website', 'text', 'e.g., "hector.com"'],
        ['client_status', 'text', 'in_onboarding / active / paused / churned'],
        ['target_icp_details', 'text', 'Full ICP description (lives here, NOT on segments)'],
        ['target_persona', 'text', 'Target personas across all segments'],
        ['pain_points', 'text', 'Key pain points for prospects'],
        ['client_usp_differentiators', 'text', 'USPs and differentiators'],
        ['all_client_sales_resources', 'text', 'Case studies, FAQs, resources'],
        ['client_call_to_action', 'text', 'What client wants prospects to do'],
        ['complimentary_sales_value', 'text', 'Free offer / lead magnet'],
        ['dnc_list_url', 'text', 'Do Not Contact list'],
        ['client_crm', 'text', 'hubspot / pipedrive / salesforce'],
        ['slack_main_channel_id', 'text', 'Slack channel for alerts'],
        ['ar_mode', 'text', 'all_manual / first_auto / all_auto'],
        ['approved', 'boolean', 'Must be true before downstream use'],
    ],
    [doc.width*0.22, doc.width*0.13, doc.width*0.65]
)

add_info_box('<b>Why ICP/persona/pain_points live here:</b> The strategist defines these at the client level. They inform all recipes. Segments are just groupings of contacts — they don\'t need their own ICP definitions.', BG_BLUE, BLUE)

# --- segments ---
story.append(Paragraph('Table 2: segments (Simplified Registry)', styles['SectionHead2']))
story.append(Paragraph('<b>Purpose:</b> Registry of valid segment names for recipe linkage &nbsp;&nbsp;|&nbsp;&nbsp; <b>~90 rows</b>', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['segment_id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK → clients', 'Which client'],
        ['segment_name', 'text', 'e.g., "retail-csuite-30plus"'],
        ['status', 'text', 'active / paused / archived'],
        ['created_at', 'timestamptz', ''],
    ],
    [doc.width*0.22, doc.width*0.18, doc.width*0.60]
)

add_info_box('<b>No pain_points, no persona, no ICP criteria.</b> Those are client-level. This table exists so recipes can link to a segment via FK. The segment_name corresponds to a tag used on contacts.', BG_PURPLE, PURPLE)

# --- contacts ---
story.append(Paragraph('Table 3: contacts (No Duplicates — One Row Per Person)', styles['SectionHead2']))
story.append(Paragraph('<b>Source:</b> Data team + Clay enrichment &nbsp;&nbsp;|&nbsp;&nbsp; <b>250K-500K rows</b> &nbsp;&nbsp;|&nbsp;&nbsp; Migrated from Supabase ~69K', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['contact_id', 'serial PK', 'Auto-generated'],
        ['— Identity —', '', ''],
        ['email', 'text', 'Unique, indexed. Primary dedup key.'],
        ['first_name / last_name', 'text', ''],
        ['full_name', 'text', 'Auto-generated from first+last'],
        ['job_title', 'text', ''],
        ['linkedin_username', 'text', 'Extracted from URL. Secondary dedup key. Indexed.'],
        ['— Company —', '', ''],
        ['company_name', 'text', ''],
        ['company_domain', 'text', 'Normalized on write (strip https://, www.). Indexed.'],
        ['industry', 'text', ''],
        ['— Enrichment —', '', ''],
        ['monthly_visits', 'int', 'From SimilarWeb or Clay'],
        ['employee_count', 'text', 'TEXT — Clay sends ranges like "11-50"'],
        ['email_verified', 'text', 'TEXT — Clay sends "yes", "true", "catchall"'],
        ['email_verified_at', 'timestamptz', 'Last verification date'],
        ['mx_provider', 'text', 'Gmail, Outlook, etc.'],
        ['is_catchall', 'text', 'TEXT — richer values from Clay'],
        ['has_email_security_gateway', 'text', 'TEXT for richer values'],
        ['is_personal_email', 'boolean', 'Computed: true if Gmail/Yahoo/Outlook domain'],
        ['AOV', 'float', 'Average Order Value (StoreLeads)'],
        ['LCP / TTI', 'float', 'PageSpeed metrics'],
        ['— Flexible —', '', ''],
        ['tags', 'text[]', 'Tag-based segmentation. e.g., ["hector-retail", "csuite"]'],
        ['extra_data', 'jsonb', 'Catch-all for non-standard Clay fields. Default {}.'],
    ],
    [doc.width*0.25, doc.width*0.12, doc.width*0.63]
)

add_info_box('<b>No duplicates:</b> john@acme.com is ONE row, regardless of clients. Dedup: lookup by email first, then linkedin_username. COALESCE on update (never overwrite non-null with null). Tags merged without duplicates.', BG_GREEN, GREEN)

# --- client_contacts ---
story.append(Paragraph('Table 4: client_contacts (Junction — Per-Client Lifecycle)', styles['SectionHead2']))
story.append(Paragraph('<b>Purpose:</b> Links contacts to clients. Tracks per-client lifecycle (cooldown, status, DNC).', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK → clients', 'Which client'],
        ['contact_id', 'int FK → contacts', 'Which contact'],
        ['segment_id', 'int FK → segments', 'Which segment (nullable)'],
        ['— Lifecycle —', '', ''],
        ['lead_status', 'text', 'raw / verified / contacted / replied / dnc / bounced'],
        ['last_contacted_at', 'timestamptz', 'Actual send date (from sequencer API)'],
        ['cooldown_until', 'timestamptz', 'last_contacted_at + 30 days'],
        ['contacted_count', 'int', 'Times contacted for THIS client'],
        ['— Audit —', '', ''],
        ['clay_table_names', 'text[]', 'Which Clay tables this contact came through'],
        ['added_at', 'timestamptz', 'When linked to this client'],
    ],
    [doc.width*0.22, doc.width*0.18, doc.width*0.60]
)

add_info_box('<b>UNIQUE: (client_id, contact_id).</b> Lifecycle is per-client: john@acme.com can be "contacted" for Hector but "verified" for Owner.com. DNC is per-client. Cooldown is per-client.', BG_ORANGE, ORANGE)

story.append(PageBreak())

# --- recipes ---
story.append(Paragraph('Table 5: recipes (One Per Client-Segment, Versioned)', styles['SectionHead2']))
story.append(Paragraph('<b>Source:</b> Strategist via Claude Code &nbsp;&nbsp;|&nbsp;&nbsp; <b>~200-400 rows</b> (with version history)', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['recipe_id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK → clients', 'Which client'],
        ['segment_id', 'int FK → segments', 'Which segment'],
        ['version', 'int', 'Starts at 1, bumps on ANY change'],
        ['status', 'text', 'active / inactive / testing'],
        ['parent_recipe_id', 'int FK → recipes', 'Links to previous version (null for v1)'],
        ['approach_content', 'text', 'ALL approaches + approach selector formula'],
        ['value_prop', 'text', 'Value prop text'],
        ['lead_list_context', 'text', 'Lead list context'],
        ['data_variables_required', 'text[]', 'e.g., [\'aov\', \'review_count\']'],
        ['enrichment_sources', 'text[]', 'e.g., [\'StoreLeads for AOV\']'],
        ['research_required', 'boolean', 'Whether Claygent researcher runs'],
        ['clay_template_name', 'text', 'Which Clay template to clone'],
        ['clay_instructions', 'text', 'Step-by-step for Clay operator (full text)'],
        ['notes', 'text', 'What changed in this version'],
    ],
    [doc.width*0.22, doc.width*0.13, doc.width*0.65]
)

add_info_box('<b>Only ONE active recipe per client-segment.</b> Naming: 2026-03-28-hector-retail-v3. All approaches + selector logic + Clay instructions in one package. Any change = new version row, old row → inactive.', BG_PURPLE, PURPLE)

# --- email_outputs ---
story.append(Paragraph('Table 6: email_outputs (Per Contact Per Recipe Run)', styles['SectionHead2']))
story.append(Paragraph('<b>Source:</b> Clay webhook push-back &nbsp;&nbsp;|&nbsp;&nbsp; <b>500K-1M+ rows</b>', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['output_id', 'serial PK', 'Auto-generated'],
        ['contact_id', 'int FK → contacts', 'Which contact'],
        ['client_id', 'int FK → clients', 'Which client'],
        ['segment_id', 'int FK → segments', 'Which segment'],
        ['recipe_id', 'int FK → recipes', 'Which recipe generated this'],
        ['recipe_version', 'int', 'Which version (denormalized for queries)'],
        ['subject_line', 'text', ''],
        ['email_1 / email_2 / email_3', 'text', 'Generated email copies'],
        ['company_summary', 'text', 'Website scrape output'],
        ['research_report', 'text', 'Researcher output (if ran)'],
        ['spam_flags', 'text', 'Flagged spam words'],
        ['campaign_id', 'int FK → campaigns', 'Which sequencer campaign (set on upload)'],
        ['status', 'text', 'generated / sent / replied / bounced'],
        ['sent_at', 'timestamptz', 'Actual send timestamp (from sequencer API)'],
        ['reply_type', 'text', 'positive / negative / ooo / bounce / null'],
        ['reply_at', 'timestamptz', 'When reply received'],
        ['reply_message', 'text', 'First reply text'],
    ],
    [doc.width*0.22, doc.width*0.18, doc.width*0.60]
)

add_info_box('<b>Never overwritten.</b> New recipe version = new row. Old preserved. Status updated by sequencer API sync (generated → sent → replied/bounced).', BG_TEAL, TEAL)

# --- campaigns ---
story.append(Paragraph('Table 7: campaigns (Sequencer Bridge)', styles['SectionHead2']))
story.append(Paragraph('<b>Purpose:</b> Maps sequencer campaigns to Neon client + segment &nbsp;&nbsp;|&nbsp;&nbsp; <b>~200-500 rows</b>', styles['BodySmall']))

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['campaign_id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK → clients', 'Which client'],
        ['segment_id', 'int FK → segments', 'Which segment'],
        ['recipe_version', 'int', 'Which recipe version used'],
        ['sequencer_type', 'text', 'smartlead / instantly / emailbison'],
        ['sequencer_campaign_id', 'text', 'ID from the sequencer API'],
        ['campaign_name', 'text', 'e.g., "2026-03-28-hector-retail-v3"'],
        ['status', 'text', 'active / completed / paused'],
    ],
    [doc.width*0.22, doc.width*0.18, doc.width*0.60]
)

add_info_box('<b>The bridge:</b> Sync script queries this table to know which sequencer campaign belongs to which client + segment. Without this, there\'s no way to map sequencer data back to Neon.', BG_YELLOW, YELLOW)

story.append(PageBreak())

# ==================== PART 2: THREE ROLES ====================
add_part_header('PART 2: THREE ROLES — Clear Boundaries', PURPLE)

# Strategist
story.append(Paragraph('Strategist (Mayank)', styles['SectionHead2']))
story.append(Paragraph('<b>Creates recipes. Owns strategy. Reviews performance.</b>', styles['Body']))
story.append(Paragraph('• Pull client context from Neon<br/>• Create recipes: all approaches + selector + enrichment config + Clay instructions<br/>• Test on 50 sample leads (GPT-4o-mini)<br/>• Review 10 emails in chat, iterate, approve<br/>• Save recipe to Neon (versioned)<br/>• Review performance by recipe version<br/>• Decide: keep, kill, or rework', styles['Body']))
add_info_box('Does NOT touch Clay or sequencers.', BG_PURPLE, PURPLE)

# Clay Operator
story.append(Paragraph('Clay Operator (Sahil)', styles['SectionHead2']))
story.append(Paragraph('<b>Manages leads + TAM. Runs Clay. Pushes results back.</b>', styles['Body']))
story.append(Paragraph('• Sources new leads, expands TAM, works with data team<br/>• Checks Neon: which contacts are eligible? (fresh + cooldown-cleared)<br/>• Pulls eligible contacts WITH existing email outputs<br/>• Pushes ALL contacts to Clay via MCP (no CSV)<br/>• Sets up Clay table per recipe\'s clay_instructions<br/>• Clay processes: verify → recipe match → generate if needed<br/>• Webhook pushes results back to Neon automatically<br/>• Hands clean batch to campaign operator<br/>• Archives Clay table', styles['Body']))
add_info_box('Does NOT make recipe decisions or touch sequencers.', BG_ORANGE, ORANGE)

# Campaign Operator
story.append(Paragraph('Campaign Operator (Hassan)', styles['SectionHead2']))
story.append(Paragraph('<b>Makes campaigns live. Monitors delivery. Handles infra.</b>', styles['Body']))
story.append(Paragraph('• Receives ready batch from Clay operator<br/>• Uploads to sequencer<br/>• Registers campaign in Neon (campaigns table)<br/>• Makes campaign live<br/>• Monitors reply rates, domain health<br/>• Bad infra? Same emails from Neon, fresh domains', styles['Body']))
add_info_box('Does NOT manage leads, TAM, or Clay.', BG_RED, RED)

add_hr()

# ==================== PART 3: COMPLETE FLOW ====================
add_part_header('PART 3: THE COMPLETE FLOW — End to End', DARK)

flow_steps = [
    ('Step 1', 'Strategist Creates Recipe', 'Opens Claude Code → pulls client context → creates recipe with all approaches + selector + Clay instructions → tests on 50 leads → saves to Neon.', 'Strategist', PURPLE),
    ('Step 2', 'Clay Operator Pulls Eligible Contacts', 'Queries Neon: fresh contacts (never contacted) + cooldown-cleared (30+ days). Pulls WITH existing email outputs from email_outputs table.', 'Clay Operator', ORANGE),
    ('Step 3', 'Push ALL to Clay via MCP', 'ALL eligible contacts pushed to Clay. No CSV. Lead data + pre-filled enrichment + existing outputs + current recipe version all travel as columns.', 'Clay Operator', ORANGE),
    ('Step 4', 'Clay Processes (Decision Matrix)', 'Re-verify every email. Check recipe match. Four outcomes: PASS_THRU (verified + match), REGENERATE (verified + no match/new), HOLD (not verified + match), DEAD (not verified + no match).', 'Clay (automated)', ORANGE),
    ('Step 5', 'Webhook to Neon', 'Results pushed back automatically. REGENERATE: new email_output rows. ALL contacts: fresh verification + enrichment updates. HOLD/DEAD: verification status updated.', 'Automated', BLUE),
    ('Step 6', 'Hand to Campaign Operator', 'Clay operator hands clean batch (PASS_THRU + REGENERATE only). HOLD/DEAD excluded. Campaign operator does NOT query DB separately.', 'Clay Op → Campaign Op', RED),
    ('Step 7', 'Upload to Sequencer', 'Campaign operator uploads to sequencer. Registers campaign in Neon (campaigns table: maps to client + segment). recipe_version as custom field.', 'Campaign Operator', RED),
    ('Step 8', 'Sequencer API Syncs Back', 'Automated sync every 4 hrs. Uses campaigns table to map data. Updates: SENT → sent_at + cooldown. REPLIED → reply data. BOUNCED → email invalid.', 'Automated', TEAL),
]

for step_num, title, desc, who, color in flow_steps:
    data = [[
        Paragraph(f'<b>{step_num}</b>', ParagraphStyle('sn', parent=styles['Body'], textColor=color, fontSize=9)),
        Paragraph(f'<b>{title}</b><br/>{desc}<br/><i>{who}</i>', styles['Body'])
    ]]
    t = Table(data, colWidths=[doc.width*0.12, doc.width*0.88])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)

story.append(PageBreak())

# ==================== PART 4: CLAY INTEGRATION ====================
add_part_header('PART 4: CLAY INTEGRATION', ORANGE)

story.append(Paragraph('What Gets Pushed TO Clay (via MCP)', styles['SectionHead2']))

add_table(
    ['Data', 'Source', 'Purpose'],
    [
        ['contact_id, email, name, company, job_title', 'contacts table', 'Lead data + identification'],
        ['company_domain, company_website, industry', 'contacts table', 'Enrichment inputs + approach selector'],
        ['AOV, LCP, TTI, monthly_visits, employee_count', 'contacts table', 'Pre-filled enrichment (Clay skips if filled)'],
        ['email_verified, email_verified_at, is_catchall, mx_provider', 'contacts table', 'Current verification status'],
        ['existing_subject_line, existing_email_1/2/3', 'email_outputs table', 'For reuse check (NULL if new contact)'],
        ['last_recipe_version', 'email_outputs table', 'For recipe match check'],
        ['current_recipe_version', 'recipes table', 'Compare against last_recipe_version'],
        ['client_id, segment_name', 'client_contacts + segments', 'Tracking + approach selector'],
    ],
    [doc.width*0.32, doc.width*0.20, doc.width*0.48]
)

story.append(Paragraph('Clay Decision Matrix — 4 Cases', styles['SectionHead2']))
story.append(Paragraph('Every contact gets re-verified. Every contact\'s last recipe version is compared to the current active version.', styles['Body']))

matrix_data = [
    [Paragraph('', styles['TableHeader']),
     Paragraph('<b>Recipe MATCHES</b>', styles['TableHeader']),
     Paragraph('<b>Recipe DOESN\'T MATCH</b>', styles['TableHeader'])],
    [Paragraph('<b>Email VERIFIED</b>', ParagraphStyle('mc', parent=styles['TableCell'], textColor=GREEN)),
     Paragraph('<b>PASS-THROUGH</b><br/>Use existing emails. No pipeline runs. Zero Clay credits on generation.', styles['TableCell']),
     Paragraph('<b>REGENERATE</b><br/>Run full pipeline: enrich → scrape → select → research → write → style check. New email_output row.', styles['TableCell'])],
    [Paragraph('<b>Email NOT VERIFIED</b>', ParagraphStyle('mc2', parent=styles['TableCell'], textColor=RED)),
     Paragraph('<b>HOLD</b><br/>Recipe is current but email went bad. Excluded from batch. Contacts table updated.', styles['TableCell']),
     Paragraph('<b>DEAD (for now)</b><br/>Bad email + stale recipe. Don\'t waste credits. Contact parked.', styles['TableCell'])],
]

t = Table(matrix_data, colWidths=[doc.width*0.22, doc.width*0.39, doc.width*0.39])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('BACKGROUND', (1,1), (1,1), BG_GREEN),
    ('BACKGROUND', (2,1), (2,1), BG_BLUE),
    ('BACKGROUND', (1,2), (1,2), BG_YELLOW),
    ('BACKGROUND', (2,2), (2,2), BG_RED),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t)
add_spacer(10)

story.append(Paragraph('What Comes BACK From Clay (via Webhook)', styles['SectionHead2']))
story.append(Paragraph('<b>To email_outputs (INSERT — REGENERATE only):</b> contact_id, recipe_version, subject_line, email_1/2/3, company_summary, research_report, spam_flags, status="generated"', styles['Body']))
story.append(Paragraph('<b>To contacts (UPDATE — ALL contacts):</b> email_verified (fresh), email_verified_at, AOV/LCP/TTI/monthly_visits (COALESCE — only if was NULL)', styles['Body']))
story.append(Paragraph('<b>PASS_THRU contacts:</b> No new email_output. Only verification updated. Existing output still current.', styles['Body']))

story.append(PageBreak())

# ==================== PART 5: CLAY TEMPLATE ====================
add_part_header('PART 5: CLAY TEMPLATE STRUCTURE', ORANGE)

story.append(Paragraph('Re-Verification Template (from actual Clay export)', styles['SectionHead2']))
story.append(Paragraph('The Clay re-verification template currently used by the Clay operator:', styles['Body']))

add_table(
    ['Column Group', 'Columns', 'Purpose'],
    [
        ['Import', 'First Name, Last Name, Job Title, Company Name, Company Domain, LinkedIn URL, Email, Email Verified, Email Verified At, Is Catchall, Mx Provider, Has Email Security Gateway', 'Lead data from Neon'],
        ['Verification Waterfall', 'Reveify Email, normal reverify, catchall reverify, Reoon Again', 'Multi-step email verification (normal → catchall → Reoon)'],
        ['Decision Logic', 'Verified Normal Email, Catchall reverifier, TLDR, Verified Catchalls', 'Determines which emails pass verification'],
        ['Output', 'Reverified Emails, Final Email, Updated Email Validity, Email Verified Date', 'Final verified email + status'],
        ['Push-back', 'Update Email Validity', 'HTTP API callback — pushes verification result back to Neon'],
    ],
    [doc.width*0.18, doc.width*0.52, doc.width*0.30]
)

story.append(Paragraph('Full Pipeline Template (extends verification template)', styles['SectionHead2']))
story.append(Paragraph('For email generation, additional columns follow the verification waterfall:', styles['Body']))

add_table(
    ['Column #', 'Column', 'Type', 'Runs When'],
    [
        ['After verification', 'Recipe Match Check', 'Formula', 'Always — compares last_recipe_version to current'],
        ['After match check', 'Action Decision', 'Formula', 'Always — outputs PASS_THRU / REGENERATE / HOLD / DEAD'],
        ['If REGENERATE', 'StoreLeads → AOV', 'Enrichment', 'Only if AOV is empty'],
        ['If REGENERATE', 'PageSpeed → LCP, TTI', 'Enrichment', 'Only if LCP is empty'],
        ['If REGENERATE', 'Website Scrape', 'Claygent', 'Always for REGENERATE'],
        ['If REGENERATE', 'Approach Selector', 'Formula', 'Picks which approach based on data'],
        ['If REGENERATE', 'Researcher', 'Claygent', 'Only if recipe requires it'],
        ['If REGENERATE', 'Copywriter', 'GPT-4o-mini', 'Generates email_1, email_2, subject_line'],
        ['If REGENERATE', 'Style Checker', 'GPT-4o-mini', 'Cleans spam words, humanizes'],
        ['Final', 'final_email_1', 'Formula', 'IF(PASS_THRU → existing, else → generated)'],
        ['Final', 'final_subject_line', 'Formula', 'IF(PASS_THRU → existing, else → generated)'],
        ['Final', 'recipe_version', 'Static', 'Current active version number'],
        ['Final', 'lead_action', 'Formula', 'PASS_THRU / REGENERATE / HOLD / DEAD'],
        ['Final', 'Webhook to Neon', 'HTTP API', 'Pushes all results back to Neon'],
    ],
    [doc.width*0.14, doc.width*0.22, doc.width*0.14, doc.width*0.50]
)

add_hr()

# ==================== PART 6: SEQUENCER + COOLDOWN ====================
add_part_header('PART 6: SEQUENCER INTEGRATION + COOLDOWN', TEAL)

story.append(Paragraph('API Sync — Automated Feedback Loop', styles['SectionHead2']))
story.append(Paragraph('One sync script handles sends, replies, and bounces. Runs every 4 hours.', styles['Body']))

story.append(Paragraph('<b>1.</b> Query Neon: all active campaigns (gets client_id, segment_id, sequencer info)<br/><b>2.</b> For each campaign, call sequencer API: pull lead statuses<br/><b>3.</b> Match by email + client_id (via campaigns table) → find exact contact<br/><b>4.</b> Update Neon:', styles['Body']))

add_table(
    ['Sequencer Status', 'email_outputs Update', 'client_contacts Update', 'contacts Update'],
    [
        ['SENT', 'status = "sent", sent_at = actual timestamp', 'last_contacted_at = sent_at, cooldown_until = sent_at + 30 days, contacted_count += 1', '—'],
        ['REPLIED', 'status = "replied", reply_type, reply_at, reply_message', 'lead_status = "replied"', '—'],
        ['BOUNCED', 'status = "bounced"', 'lead_status = "bounced"', 'email_verified = "false"'],
    ],
    [doc.width*0.13, doc.width*0.27, doc.width*0.35, doc.width*0.25]
)

story.append(Paragraph('Cooldown Lifecycle — API-Driven', styles['SectionHead2']))

add_table(
    ['Day', 'Event', 'DB State'],
    [
        ['Day 1', 'Contact added to Neon', 'lead_status = verified, cooldown = NULL → Eligible'],
        ['Day 5', 'Goes through Clay, emails generated', 'email_output created, status = generated'],
        ['Day 6', 'Campaign operator uploads to sequencer', 'Campaign registered in Neon. No status change yet.'],
        ['Day 8', 'Sequencer actually sends (API sync picks up)', 'sent_at set, cooldown_until = Day 38 → In cooldown'],
        ['Day 8-38', 'In cooldown', 'Excluded from all batches for this client'],
        ['Day 38+', 'Cooldown cleared', 'cooldown_until < NOW() → Eligible again'],
    ],
    [doc.width*0.12, doc.width*0.38, doc.width*0.50]
)

add_info_box('<b>Why API-driven:</b> Sequencer drips 2,000 leads over 10-15 days. Each lead gets its ACTUAL send date for cooldown, not the upload date. Lead #1 sent March 28, lead #1,800 sent April 10 — each gets accurate 30-day cooldown.', BG_TEAL, TEAL)

story.append(PageBreak())

# ==================== PART 7: TAG-BASED SEGMENTATION ====================
add_part_header('PART 7: TAG-BASED SEGMENTATION', DARK)

story.append(Paragraph('Tags are a TEXT[] array on the contacts table. They are the primary mechanism for segmentation.', styles['Body']))

add_table(
    ['Tag Type', 'Examples', 'Purpose'],
    [
        ['Client-segment', '"hector-retail", "owner-restaurant"', 'Links contact to client + segment'],
        ['Attribute', '"csuite", "30plus-employees", "high-aov"', 'Lead characteristics for filtering'],
        ['Campaign', '"march-batch-1", "reapproach-april"', 'Batch tracking (optional)'],
    ],
    [doc.width*0.18, doc.width*0.42, doc.width*0.40]
)

story.append(Paragraph('<b>How tags relate to segments:</b> segment_name "retail" under client "Hector" corresponds to the tag "hector-retail" on contacts. The tag IS the segment assignment.', styles['Body']))
story.append(Paragraph('<b>Do we need recipe version tags?</b> No. Recipe version tracking lives on email_outputs (recipe_version column). Tags are for segmentation, not recipe tracking.', styles['Body']))
story.append(Paragraph('<b>Why tags, not just segment_id on junction:</b> Tags are more flexible. New segmentation = new tag, no schema change. Multiple tags per contact. Merge without duplicates on update.', styles['Body']))

add_hr()

# ==================== PART 8: RECIPE + CLAY INSTRUCTIONS ====================
add_part_header('PART 8: RECIPE MANAGEMENT + CLAY INSTRUCTIONS FLOW', PURPLE)

story.append(Paragraph('How Clay Instructions Flow', styles['SectionHead2']))

story.append(Paragraph('<b>1.</b> Strategist writes clay_instructions as part of recipe creation<br/><b>2.</b> Saved to Neon recipes table (full text: template name, column-by-column setup, prompts, formulas)<br/><b>3.</b> Clay operator queries: "Show me instructions for Hector Retail"<br/><b>4.</b> Gets step-by-step: which template to clone, which columns to set up, which prompts to paste<br/><b>5.</b> When recipe versions up → Clay operator checks: "What changed?"<br/><b>6.</b> If only approach text changed → operator updates prompt columns in Clay template<br/><b>7.</b> If enrichment sources changed → operator adds/removes enrichment columns<br/><b>8.</b> Template structure stays mostly the same across versions', styles['Body']))

add_info_box('The clay_instructions field is the contract between strategist and Clay operator. It\'s a plain-text document with exact column setup, formulas, and prompts. The Clay operator follows it step by step.', BG_PURPLE, PURPLE)

story.append(Paragraph('Recipe Version Flow', styles['SectionHead2']))
story.append(Paragraph('• Create recipe → v1, status = testing, parent = null<br/>• Test and approve → status = active<br/>• Edit recipe → NEW row (v2), parent = old recipe_id, old → inactive<br/>• Kill recipe → status = inactive<br/>• <b>Only ONE active recipe per client-segment at any time</b>', styles['Body']))

add_hr()

# ==================== PART 9: SCENARIOS ====================
add_part_header('PART 9: CAMPAIGN SCENARIOS', DARK)

scenarios = [
    ('A: New Client, First Campaign', '~5% of days', 'All contacts new → all REGENERATE. Full pipeline. Clay operator hands batch to campaign operator.', GREEN),
    ('B: Same Recipe, More Leads', '~60% of days', 'Mix of fresh + cooldown-cleared. All go to Clay. Fresh = REGENERATE. Cooldown-cleared with current recipe = PASS_THRU (re-verified, existing emails reused).', BLUE),
    ('C: Recipe Changed', '~20% of days', 'Version bumped. Recipe match fails for all. All = REGENERATE. New email_output rows. Old preserved for comparison.', ORANGE),
    ('D: Bad Infrastructure', '~10% of days', 'Same emails from Neon, fresh sending domains. No Clay needed. Zero regeneration.', RED),
    ('E: Re-approach (Cooldown Cleared)', 'Monthly', 'Contacts 30+ days, no reply. Through Clay. Recipe unchanged = PASS_THRU. Recipe changed = REGENERATE. New campaign.', TEAL),
    ('F: A/B Test Versions', 'As needed', 'Split contacts: half v2, half v3. Compare reply rates by recipe_version after 2 weeks.', PURPLE),
]

for title, freq, desc, color in scenarios:
    data = [[
        Paragraph(f'<b>{title}</b> ({freq})', ParagraphStyle('sc', parent=styles['Body'], textColor=color, fontSize=9.5)),
        Paragraph(desc, styles['Body'])
    ]]
    t = Table(data, colWidths=[doc.width*0.35, doc.width*0.65])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)

add_hr()

# ==================== PART 10: MIGRATION ====================
add_part_header('PART 10: MIGRATION FROM SUPABASE', DARK_BLUE)

story.append(Paragraph('What Carries Over (Same Patterns)', styles['SectionHead2']))

add_table(
    ['Pattern', 'Status'],
    [
        ['Shared contacts, no duplicates', 'KEEP — one row per person'],
        ['client_contacts junction', 'KEEP — now carries lifecycle data (cooldown, status)'],
        ['COALESCE dedup on upsert', 'KEEP — never lose enriched data'],
        ['Domain normalization on write', 'KEEP — strip https://, www., paths'],
        ['Tags TEXT[] for segmentation', 'KEEP — flexible, no schema changes needed'],
        ['extra_data JSONB catch-all', 'KEEP — non-standard Clay fields'],
        ['employee_count as TEXT', 'KEEP — Clay sends ranges'],
        ['email_verified as TEXT', 'KEEP — richer values from Clay'],
        ['is_personal_email computed', 'KEEP — auto-detect Gmail/Yahoo'],
    ],
    [doc.width*0.45, doc.width*0.55]
)

story.append(Paragraph('What Changes', styles['SectionHead2']))

add_table(
    ['Supabase → Neon', 'Why'],
    [
        ['PostgREST API → Clay MCP + webhook', 'Direct integration, no REST layer'],
        ['push-to-clay edge function → MCP push', 'MCP handles the push'],
        ['No segments table → Add segments (registry)', 'Recipe linkage'],
        ['No recipes table → Add recipes (versioned)', 'Core of the system'],
        ['No email_outputs → Add email_outputs', 'Track emails + lifecycle + replies'],
        ['No campaigns → Add campaigns', 'Bridge for sequencer API sync'],
        ['client_contacts (simple) → + lifecycle fields', 'Cooldown, status per-client'],
    ],
    [doc.width*0.45, doc.width*0.55]
)

add_hr()

# ==================== PART 11: BUILD ORDER ====================
add_part_header('PART 11: BUILD ORDER — 6 PHASES', DARK)

phases = [
    ('P1', 'Neon Schema', 'Create all 7 tables. Replicate upsert_contact logic with COALESCE. Indexes on email, linkedin_username, company_domain. Test with sample data.', 'Neon access', 'Everything', GREEN),
    ('P2', 'Recipe Management + Testing', 'CRUD for recipes via Claude Code. Test 50 leads (GPT-4o-mini). Show 10 in chat. Save to Neon.', 'P1 + OpenAI API + SerpAPI', 'Recipe workflow', PURPLE),
    ('P3', 'Clay Integration', 'MCP push to Clay. Webhook return. Decision matrix (PASS_THRU/REGENERATE/HOLD). Auto push-back to Neon.', 'P1 + Clay MCP + webhook', 'Full pipeline', ORANGE),
    ('P4', 'Campaigns + Sequencer Sync', 'Campaign registration. API sync: sends, replies, bounces. Cooldown tracking.', 'P3 + sequencer API', 'Feedback loop', YELLOW),
    ('P5', 'Performance + Dashboard', 'Recipe version performance. Cross-client views. Bottom performers.', 'P4', 'Data-driven decisions', PURPLE),
    ('P6', 'Slack Alerts + Monitoring', 'Daily: leads remaining, 0% reply alerts, proactive management.', 'P5 + Slack webhook', 'Proactive ops', RED),
]

for num, title, desc, needs, unblocks, color in phases:
    data = [[
        Paragraph(f'<b>{num}</b>', ParagraphStyle('pn', parent=styles['Body'], textColor=color, fontSize=11, alignment=TA_CENTER)),
        Paragraph(f'<b>{title}</b><br/>{desc}<br/><i>Needs: {needs} | Unblocks: {unblocks}</i>', styles['Body'])
    ]]
    t = Table(data, colWidths=[doc.width*0.08, doc.width*0.92])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,0), 0),
    ]))
    story.append(t)

add_hr()

# ==================== DATA FLOW SUMMARY ====================
add_part_header('DATA FLOW SUMMARY — Every Arrow in the System', DARK)

flows = [
    ('Strategist → Neon', 'Recipe content (all approaches + selector + Clay instructions), version, status', PURPLE),
    ('Neon → Clay (via MCP)', 'Contact data + pre-filled enrichment + existing email outputs + current recipe version. ALL eligible contacts.', ORANGE),
    ('Clay → Neon (via Webhook)', 'New email_output rows (REGENERATE only). Updated verification + enrichment (ALL contacts). COALESCE on enrichment.', ORANGE),
    ('Clay → Campaign Operator', 'Clean batch: verified contacts with final emails (PASS_THRU + REGENERATE). HOLD/DEAD excluded. Direct handoff.', RED),
    ('Campaign Op → Sequencer', 'CSV with contact info + emails + recipe_version as custom field.', RED),
    ('Campaign Op → Neon', 'Campaign registration (campaigns table: maps sequencer campaign to client + segment).', RED),
    ('Sequencer → Neon (API Sync)', 'Send confirmations → sent_at + cooldown. Reply data → reply_type, reply_at. Bounce data → email_verified = false.', TEAL),
    ('Neon → Strategist (Claude Code)', 'Performance data: recipe version × reply rate. Lead lifecycle. Cross-client views.', PURPLE),
]

for label, desc, color in flows:
    data = [[
        Paragraph(f'<b>{label}</b>', ParagraphStyle('fl', parent=styles['Body'], textColor=color, fontSize=9)),
        Paragraph(desc, styles['Body'])
    ]]
    t = Table(data, colWidths=[doc.width*0.28, doc.width*0.72])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)

# Build
doc.build(story)
print(f"PDF generated: {output_path}")
