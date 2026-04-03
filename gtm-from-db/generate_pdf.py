"""Generate a clean, professional PDF from the complete system scope."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib import colors
import re

# ── Colors ──
DARK = HexColor('#1a1a2e')
BLUE = HexColor('#2563eb')
GREEN = HexColor('#16a34a')
PURPLE = HexColor('#7c3aed')
ORANGE = HexColor('#ea580c')
RED = HexColor('#dc2626')
TEAL = HexColor('#0891b2')
GRAY = HexColor('#6b7280')
LIGHT_GRAY = HexColor('#f3f4f6')
WHITE = HexColor('#ffffff')
BLACK = HexColor('#111827')
BORDER = HexColor('#e5e7eb')

# ── Document setup ──
doc = SimpleDocTemplate(
    "/Users/mayankmittal/Desktop/GTM-CC/gtm-from-db/complete-system-scope.pdf",
    pagesize=A4,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.6*inch, bottomMargin=0.6*inch,
)

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle('DocTitle', parent=styles['Title'], fontSize=22, textColor=BLACK, spaceAfter=4, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontSize=11, textColor=GRAY, spaceAfter=20))
styles.add(ParagraphStyle('PartTitle', parent=styles['Heading1'], fontSize=16, textColor=BLUE, spaceBefore=24, spaceAfter=8, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('SectionHead', parent=styles['Heading2'], fontSize=13, textColor=BLACK, spaceBefore=16, spaceAfter=6, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('SubHead', parent=styles['Heading3'], fontSize=11, textColor=PURPLE, spaceBefore=12, spaceAfter=4, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, textColor=BLACK, spaceAfter=6, leading=13))
styles.add(ParagraphStyle('BodyBold', parent=styles['Normal'], fontSize=9, textColor=BLACK, spaceAfter=6, leading=13, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CodeBlock', parent=styles['Normal'], fontSize=8, textColor=HexColor('#374151'), fontName='Courier', spaceAfter=8, leading=11, leftIndent=12, backColor=LIGHT_GRAY))
styles.add(ParagraphStyle('Note', parent=styles['Normal'], fontSize=8, textColor=GREEN, spaceAfter=6, leading=11, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('Label', parent=styles['Normal'], fontSize=8, textColor=GRAY, spaceAfter=2))

story = []

# ── Helper functions ──
def add_title(text):
    story.append(Paragraph(text, styles['DocTitle']))

def add_subtitle(text):
    story.append(Paragraph(text, styles['DocSubtitle']))

def add_part(text):
    story.append(Paragraph(text, styles['PartTitle']))

def add_section(text):
    story.append(Paragraph(text, styles['SectionHead']))

def add_subsection(text):
    story.append(Paragraph(text, styles['SubHead']))

def add_body(text):
    # Convert **bold** to <b>bold</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    story.append(Paragraph(text, styles['Body']))

def add_bold(text):
    story.append(Paragraph(text, styles['BodyBold']))

def add_code(text):
    lines = text.strip().split('\n')
    for line in lines:
        line = line.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
        story.append(Paragraph(line, styles['CodeBlock']))
    story.append(Spacer(1, 4))

def add_note(text):
    story.append(Paragraph(text, styles['Note']))

def add_spacer(h=8):
    story.append(Spacer(1, h))

def add_hr():
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=12, spaceBefore=12))

def add_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if col_widths is None:
        col_widths = [doc.width / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), DARK),
        ('TEXTCOLOR', (0, 1), (-1, -1), BLACK),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    add_spacer(8)


# ════════════════════════════════════════
# COVER
# ════════════════════════════════════════
add_spacer(100)
add_title("GTM-CC: Complete System Scope")
add_subtitle("One Neon DB. Three Roles. 30 Clients. Every Scenario.")
add_spacer(20)
add_body("CleverViral — DB-Powered Campaign System Architecture")
add_body("Version: March 2026")
add_spacer(40)

add_table(
    ['Component', 'Details'],
    [
        ['Database', 'Neon (single DB for everything)'],
        ['Roles', 'Strategist, Campaign Operator, Clay Operator'],
        ['Scale', '30 clients, 90 segments, 250K-500K leads'],
        ['Email Pipeline', 'Clay (enrichment + GPT-4o-mini pipeline)'],
        ['Feedback Loop', 'Sequencer API sync to Neon DB'],
        ['Cost', '~$20-70/mo for Neon (Clay cost unchanged)'],
    ],
    col_widths=[2*inch, 4.5*inch]
)

story.append(PageBreak())

# ════════════════════════════════════════
# PART 1: DATABASE
# ════════════════════════════════════════
add_part("PART 1: THE DATABASE (Neon)")
add_body("Everything runs on ONE Neon database. Five tables.")
add_hr()

# Table 1: clients
add_section("Table 1: clients")
add_body("<b>Source:</b> Tally onboarding form webhook")
add_body("<b>Updated by:</b> Strategist (manual approval), Tally webhook (auto)")
add_body("<b>Read by:</b> Strategist (recipe creation context), Dashboard (all roles)")
add_spacer(4)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['client_id', 'serial PK', 'Auto-generated'],
        ['client_name', 'text', 'e.g., "Hector"'],
        ['client_website', 'text', 'e.g., "hector.com"'],
        ['client_status', 'text', 'in_onboarding / active / paused / churned'],
        ['primary_poc_name', 'text', 'Main client contact'],
        ['primary_poc_email', 'text', ''],
        ['target_icp_details', 'text', 'ICP description across segments'],
        ['client_usp_differentiators', 'text', 'USPs and differentiators'],
        ['all_client_sales_resources', 'text', 'Case studies, FAQs, resources'],
        ['all_social_proof_brand_names', 'text', 'Logo wall brands'],
        ['client_call_to_action', 'text', 'What the client wants prospects to do'],
        ['complimentary_sales_value', 'text', 'Free offer / lead magnet'],
        ['dnc_list_url', 'text', 'Do Not Contact list'],
        ['client_crm', 'text', 'hubspot / pipedrive / salesforce / etc'],
        ['notification_channels', 'text', 'slack / email / both'],
        ['ar_client_choice', 'text', 'yes / no / tell_me_more'],
        ['ar_mode', 'text', 'all_manual / first_auto / all_auto'],
        ['approved', 'boolean', 'Must be true before downstream use'],
        ['created_at', 'timestamptz', ''],
    ],
    col_widths=[2.2*inch, 1.2*inch, 3.1*inch]
)
add_hr()

# Table 2: segments
add_section("Table 2: segments")
add_body("<b>Source:</b> Strategist creates when defining ICP segments")
add_body("<b>UNIQUE constraint:</b> (client_id, segment_name) -- no duplicate segments per client.")
add_spacer(4)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['segment_id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK', 'Which client'],
        ['segment_name', 'text', 'e.g., "Retail", "Agency", "Enterprise"'],
        ['target_industry', 'text', 'e.g., "Retail ecommerce"'],
        ['target_persona', 'text', 'e.g., "VP Marketing, Director of Growth"'],
        ['target_pain_points', 'text', 'Key pain points for this segment'],
        ['icp_criteria', 'text', 'How to identify leads for this segment'],
        ['status', 'text', 'active / paused / archived'],
        ['created_at', 'timestamptz', ''],
    ],
    col_widths=[2.2*inch, 1.2*inch, 3.1*inch]
)
add_hr()

# Table 3: leads
add_section("Table 3: leads")
add_body("<b>Source:</b> Data team (Apollo, SimilarWeb, etc.) to Clay for verification to Neon")
add_body("<b>UNIQUE constraint:</b> (client_id, segment_id, email) -- same person can exist for different clients/segments.")
add_spacer(4)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['lead_id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK', 'Which client this lead belongs to'],
        ['segment_id', 'int FK', 'Which segment'],
        ['segment_name', 'text', 'Denormalized for easy queries'],
        ['email', 'text', 'Prospect email (unique per client)'],
        ['first_name', 'text', ''],
        ['last_name', 'text', ''],
        ['full_name', 'text', ''],
        ['job_title', 'text', ''],
        ['linkedin_profile_url', 'text', ''],
        ['company_name', 'text', ''],
        ['company_domain', 'text', ''],
        ['company_website', 'text', ''],
        ['industry', 'text', ''],
        ['monthly_visits', 'int', 'From SimilarWeb or Clay'],
        ['employee_count', 'int', 'From Apollo or Clay'],
        ['email_verified', 'boolean', ''],
        ['email_verified_at', 'timestamptz', 'Last verification date'],
        ['mx_provider', 'text', 'Gmail, Outlook, etc.'],
        ['city', 'text', ''],
        ['country', 'text', ''],
        ['LCP', 'float', 'Largest Contentful Paint (PageSpeed)'],
        ['TTI', 'float', 'Time to Interactive (PageSpeed)'],
        ['AOV', 'float', 'Average Order Value (StoreLeads)'],
        ['extra_data', 'jsonb', 'Any additional enrichment fields'],
        ['lead_status', 'text', 'raw / verified / contacted / replied / dnc'],
        ['contacted_count', 'int', 'How many times contacted'],
        ['last_contacted_at', 'timestamptz', 'When last email was sent'],
        ['cooldown_until', 'timestamptz', 'last_contacted + 30 days'],
        ['created_at', 'timestamptz', ''],
    ],
    col_widths=[2.2*inch, 1.2*inch, 3.1*inch]
)

add_note("Cross-client: john@acme.com can have Row 1 (client=Hector, segment=Retail) and Row 2 (client=Owner.com, segment=Restaurant). Separate rows, no conflict. DNC is per-client.")

story.append(PageBreak())

# Table 4: recipes
add_section("Table 4: recipes")
add_body("<b>Source:</b> Strategist creates via Claude Code + email-approach-generator skill")
add_body("<b>Read by:</b> Clay operator (instructions), Campaign operator (reuse check), Strategist (performance review)")
add_spacer(4)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['recipe_id', 'serial PK', 'Auto-generated'],
        ['client_id', 'int FK', 'Which client'],
        ['segment_id', 'int FK', 'Which segment'],
        ['segment_name', 'text', 'Denormalized'],
        ['recipe_name', 'text', '"ROI Calculator", "Insider Remark"'],
        ['version', 'int', 'Starts at 1, bumps on ANY change'],
        ['status', 'text', 'active / inactive / testing'],
        ['parent_recipe_id', 'int FK', 'Links to previous version (null for v1)'],
        ['approach_content', 'text', 'Full email approach markdown'],
        ['value_prop', 'text', 'Value prop text this recipe uses'],
        ['lead_list_context', 'text', 'Lead list context text'],
        ['data_variables_required', 'text[]', "e.g., ARRAY['aov', 'review_count']"],
        ['enrichment_sources', 'text[]', "e.g., ARRAY['StoreLeads for AOV']"],
        ['research_required', 'boolean', 'Whether Claygent researcher runs'],
        ['clay_template_name', 'text', 'Which Clay template to clone'],
        ['clay_instructions', 'text', 'Step-by-step for the Clay operator'],
        ['notes', 'text', 'Why created, what changed'],
        ['created_at', 'timestamptz', ''],
    ],
    col_widths=[2.2*inch, 1.2*inch, 3.1*inch]
)

add_bold("Version flow:")
add_body("Create recipe: version 1, parent = null, status = testing")
add_body("Test and approve: status = active")
add_body("Edit recipe: NEW row with version 2, parent = old recipe_id, old row status = inactive")
add_body("Kill recipe: status = inactive")
add_hr()

# Table 5: email_outputs
add_section("Table 5: email_outputs")
add_body("<b>Source:</b> Clay push-back (after running recipe) + Sequencer API sync (reply data)")
add_spacer(4)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ['output_id', 'serial PK', 'Auto-generated'],
        ['lead_id', 'int FK', 'Which lead'],
        ['client_id', 'int FK', 'Which client'],
        ['segment_id', 'int FK', 'Which segment'],
        ['recipe_id', 'int FK', 'Which recipe generated this'],
        ['recipe_name', 'text', 'Denormalized (for CSV custom field)'],
        ['recipe_version', 'int', 'Which version of the recipe'],
        ['subject_line', 'text', ''],
        ['email_1', 'text', ''],
        ['email_2', 'text', ''],
        ['email_3', 'text', ''],
        ['company_summary', 'text', 'Website scrape output'],
        ['research_report', 'text', 'Researcher output (if ran)'],
        ['spam_flags', 'text', 'Flagged spam words'],
        ['batch_id', 'text', 'Groups leads processed together'],
        ['status', 'text', 'generated / sent / replied / bounced'],
        ['campaign_name', 'text', 'Sequencer campaign name'],
        ['sequencer_type', 'text', 'smartlead / instantly / emailbison'],
        ['sent_at', 'timestamptz', 'When uploaded to sequencer'],
        ['reply_type', 'text', 'positive / negative / ooo / bounce / null'],
        ['reply_at', 'timestamptz', 'When reply received'],
        ['reply_message', 'text', 'First reply text'],
        ['created_at', 'timestamptz', 'When email was generated'],
    ],
    col_widths=[2.2*inch, 1.2*inch, 3.1*inch]
)

add_note("Reuse check: Does this lead have a row WHERE recipe_name + recipe_version matches a CURRENT active recipe? If yes = REUSE (pull existing emails). If no = GENERATE (send to Clay).")

story.append(PageBreak())

# ════════════════════════════════════════
# PART 2: CLAY
# ════════════════════════════════════════
add_part("PART 2: WHAT HAPPENS ON CLAY")
add_body("Clay is a <b>disposable processing layer</b>. Use it, get results, push back to Neon, archive the table.")
add_hr()

add_section("Columns Imported TO Clay (Neon to Clay)")
add_table(
    ['Column', 'Source', 'Purpose'],
    [
        ['lead_id', 'Neon leads', 'To match results back on push-back'],
        ['email', 'Neon leads', 'Lead identification + re-verification'],
        ['first_name, last_name', 'Neon leads', 'Used in email copy'],
        ['company_name, company_domain', 'Neon leads', 'Email copy + enrichment input'],
        ['company_website', 'Neon leads', 'Website scrape + PageSpeed input'],
        ['job_title, industry', 'Neon leads', 'Email copy + approach selector'],
        ['monthly_visits, employee_count', 'Neon leads', 'Pre-filled if already enriched'],
        ['email_verified_at', 'Neon leads', 'Clay checks if re-verification needed'],
        ['AOV, LCP, TTI', 'Neon leads', 'Pre-filled if enriched (saves Clay credits)'],
        ['client_id, segment_name', 'Neon leads', 'For approach selector'],
    ],
    col_widths=[2*inch, 1.3*inch, 3.2*inch]
)

add_section("Clay Recipe Columns (What Clay Does)")
add_table(
    ['#', 'Column', 'Type', 'What It Does'],
    [
        ['1-17', 'Import columns', 'Import', 'All lead data from CSV'],
        ['18', 'Email Re-verify', 'Enrichment', 'Re-verifies email. Always runs.'],
        ['19', 'StoreLeads AOV', 'Enrichment', 'Gets AOV. Only if empty.'],
        ['20', 'PageSpeed LCP/TTI', 'Enrichment', 'Gets LCP + TTI. Only if empty.'],
        ['21', 'SimilarWeb', 'Enrichment', 'Gets monthly visits. Only if empty.'],
        ['22', 'Website Scrape', 'Claygent', 'Scrapes website, 50-100 word summary'],
        ['23', 'Approach Selector', 'Formula', 'Picks recipe per lead by data availability'],
        ['24', 'Selected Recipe', 'Formula', 'Pulls approach_content from selector'],
        ['25', 'Researcher', 'Claygent', 'Web research. Conditional per recipe.'],
        ['26', 'Copywriter', 'GPT-4o-mini', 'Writes email_1, email_2, email_3, subject_line'],
        ['27', 'Style Checker', 'GPT-4o-mini', 'Fixes spam, humanizes, breaks linear flow'],
        ['28', 'Recipe Name', 'Formula', 'Which recipe this lead got'],
        ['29', 'Recipe Version', 'Formula', 'Version number for tracking'],
    ],
    col_widths=[0.4*inch, 1.5*inch, 1.1*inch, 3.5*inch]
)

add_section("Push Back FROM Clay (Clay to Neon)")
add_bold("Update 1: email_outputs table (INSERT new rows)")
add_body("lead_id, recipe_name, recipe_version, subject_line, email_1, email_2, email_3, company_summary, research_report, spam_flags, batch_id, status='generated'")
add_spacer(4)
add_bold("Update 2: leads table (UPDATE existing rows)")
add_body("email_verified, email_verified_at, AOV, LCP, TTI, monthly_visits -- only fields that were NULL and are now enriched.")
add_spacer(4)
add_note("Enrichment data goes to leads table (permanent). Email content goes to email_outputs table (versioned per recipe).")

story.append(PageBreak())

# ════════════════════════════════════════
# PART 3: TYPICAL DAY
# ════════════════════════════════════════
add_part("PART 3: A TYPICAL DAY -- EVERY SCENARIO")
add_body("30 clients. Each has 1-4 segments. Each segment has 1-5 active recipes.")
add_hr()

# Strategist
add_section("STRATEGIST'S DAY (Mayank)")

add_subsection("Morning: Weekly Planning (Monday, 30 min)")
add_body('Opens Claude Code (GTM-CC project). Says "Show me all clients\' status." Claude Code queries Neon and returns a dashboard view of all 30 clients: segments, active recipes, pending leads, required actions.')
add_spacer()

add_subsection("Task 1: Create New Recipe")
add_body("1. Pull client context from Neon (USPs, case studies, pain points)")
add_body("2. Run email-approach-generator skill in Claude Code")
add_body("3. Create recipe: declare data variables needed + enrichment sources")
add_body("4. Write Clay operator instructions (step-by-step)")
add_body("5. Test on 50 sample leads (GPT-4o-mini), review 10 in chat")
add_body("6. Iterate, approve, save to Neon recipes table")
add_body("<b>Time: ~15 minutes</b>")
add_spacer()

add_subsection("Task 2: Update Existing Recipe")
add_body("1. Review performance by recipe (query email_outputs)")
add_body("2. Identify underperformers")
add_body("3. Edit approach_content, test on 10 leads, save as new version")
add_body("4. Old version marked inactive, new version active")
add_body("<b>Time: ~10 minutes</b>")
add_spacer()

add_subsection("Task 3: Review Performance Across All Clients")
add_body('Query: "Bottom 5 recipes by reply rate this month." Decide what to keep, kill, or rework.')
add_body("<b>Time: ~10 minutes</b>")
add_hr()

# Campaign Operator
add_section("CAMPAIGN OPERATOR'S DAY (Hassan)")

add_subsection("Morning: Check Slack Alerts (8:00 AM, 5 min)")
add_body("Slack bot shows: URGENT (less than 2 days of leads), PREPARE (less than 5 days), ON TRACK, INFRA ALERTS (0% reply rate).")
add_spacer()

add_subsection("Scenario A: Same Recipe, More Leads (60% of days)")
add_body("1. Query Neon: eligible leads, split REUSE vs GENERATE")
add_body("2. Export REUSE leads CSV from Neon (instant)")
add_body("3. Hand GENERATE leads to Clay operator")
add_body("4. Wait for Clay push-back, combine CSVs")
add_body("5. Upload to sequencer, update email_outputs status")
add_body("<b>Time: 15 min</b>")
add_spacer()

add_subsection("Scenario B: Recipe Changed (20% of days)")
add_body("1. Strategy updated a recipe -- version bumped")
add_body("2. Leads with old version flagged for regeneration")
add_body("3. Send to Clay with updated recipe instructions")
add_body("4. Push back, combine with any reuse leads, upload")
add_body("<b>Time: 15 min + Clay wait</b>")
add_spacer()

add_subsection("Scenario C: Bad Infrastructure (10% of days)")
add_body("0% reply rate = bad sending domains. Same emails, new infra.")
add_body("Pull existing emails from Neon (instant). New campaign, new domains. <b>Zero Clay cost.</b>")
add_spacer()

add_subsection("Scenario D: New Client, First Campaign (5% of days)")
add_body("ALL leads are new. ALL go to Clay. Full recipe run. ~30-45 min processing for 2,000 leads.")
add_spacer()

add_subsection("Scenario E: Re-approach After 30-Day Cooldown")
add_body("Leads contacted 30+ days ago, no reply. REGENERATE through Clay (research finds new signals, copy is fresh). New email_output rows, old ones preserved.")
add_spacer()

add_subsection("Scenario F: Add to Existing Campaign")
add_body("NOT adding to the same sequencer campaign. Each batch = new campaign. Same flow as Scenario A or B.")
add_hr()

# Clay Operator
add_section("CLAY OPERATOR'S DAY")

add_subsection("Morning: Check Assignments (8:30 AM)")
add_body("Dashboard shows pending Clay runs across all clients. Total: 3-5 assignments, 2,000-5,000 leads per day.")
add_spacer()

add_subsection("For Each Assignment")
add_body("1. Read recipe instructions from Neon (clay_instructions field)")
add_body("2. Clone Clay template (or create from scratch for new clients)")
add_body("3. Import leads CSV")
add_body("4. Run the table (~20-40 min per 800-2,000 leads)")
add_body("5. Spot-check 5-10 rows for errors")
add_body("6. Export CSV, run push-back script to Neon")
add_body("7. Confirm in Neon, archive Clay table")
add_body("<b>Time per assignment: ~40-60 min</b>")
add_spacer()

add_subsection("When Recipe Changed")
add_body("Update approach text in Clay template per instructions. +5 min. Everything else stays the same.")
add_spacer()

add_subsection("New Client (No Template)")
add_body("Create Clay table from scratch following clay_instructions. ~30-45 min first time. Save as template for future.")

story.append(PageBreak())

# ════════════════════════════════════════
# PART 4: EDGE CASES
# ════════════════════════════════════════
add_part("PART 4: EDGE CASES AND SCENARIOS")
add_hr()

scenarios = [
    ("Same Lead, Different Clients", "john@acme.com has separate rows per client. Different recipes, different emails, no conflict. DNC is per-client."),
    ("Lead Gets Different Recipe on Re-approach", "March: ROI Calculator. April (after cooldown): approach selector picks Page Speed Angle (new LCP data available). Both email_output rows preserved. Can compare which worked."),
    ("A/B Test a New Recipe", "Split 500 leads: 250 get Brand Authority only, 250 get ROI Calculator only. After 2 weeks, query performance by recipe_name. Winner scales."),
    ("Data Team Adds TAM Mid-Month", "New leads appear as GENERATE in next batch. No disruption to existing campaigns."),
    ("Client Churns", "client_status = 'churned'. All recipes inactive. Data preserved for potential reactivation."),
    ("Clay Fails Mid-Processing", "Export completed rows, push to Neon. Re-import failed rows to new Clay table. Net result: all processed, two passes."),
    ("Wrong CSV Uploaded", "No DB corruption -- error is sequencer-side only. Pause wrong campaign, upload correct CSV. Prevention: filename convention client-segment-date.csv."),
]

for title, desc in scenarios:
    add_subsection(title)
    add_body(desc)
    add_spacer(4)

story.append(PageBreak())

# ════════════════════════════════════════
# PART 5: SUMMARY
# ════════════════════════════════════════
add_part("PART 5: SUMMARY")
add_hr()

add_section("Daily Time Per Role")
add_table(
    ['Role', 'Daily Tasks', 'Time/Day', 'Tools'],
    [
        ['Strategist', 'Review performance, update/create recipes, test samples', '1-2 hours', 'Claude Code + Neon'],
        ['Campaign Op', 'Slack alerts, reuse checks, CSV export, sequencer upload', '2-3 hours', 'Dashboard + Neon + Sequencers'],
        ['Clay Op', 'Read instructions, run Clay tables, push results back', '3-4 hours', 'Clay + Neon + push-back script'],
    ],
    col_widths=[1.2*inch, 2.5*inch, 1*inch, 1.8*inch]
)

add_section("Neon DB Size at 30 Clients")
add_table(
    ['Table', 'Rows', 'Growth Rate'],
    [
        ['clients', '30', 'Slow (new clients)'],
        ['segments', '~90', 'Slow'],
        ['leads', '250K-500K', '~20K-30K/month'],
        ['recipes', '~200-400', '~20-30/month'],
        ['email_outputs', '500K-1M+', '~80K-100K/month'],
    ],
    col_widths=[2*inch, 2*inch, 2.5*inch]
)

add_section("Monthly Cost")
add_table(
    ['Item', 'Monthly Cost'],
    [
        ['Neon DB', '$19-69/mo (Pro plan)'],
        ['Clay', 'Per usage (no change from today)'],
        ['GPT-4o-mini (via Clay)', '~$0.005/lead x 80K = ~$400'],
        ['Sequencer API sync', 'Minimal (cron job)'],
        ['Slack notifications', 'Free (webhook)'],
        ['Total new cost', '$20-70/mo for Neon'],
    ],
    col_widths=[3*inch, 3.5*inch]
)

# ── Build PDF ──
doc.build(story)
print("PDF generated successfully!")
