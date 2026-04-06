"""
Generate the GTM-CC Architecture & System Scope PDF.
Run: python3 scripts/generate_architecture_pdf.py
Output: docs/gtm-cc-architecture.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# ── Colors ──
DARK = HexColor('#1a1a2e')
BLUE = HexColor('#0f3460')
ACCENT = HexColor('#e94560')
LIGHT_BLUE = HexColor('#eef2f7')
WHITE = HexColor('#ffffff')
GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#f5f5f5')
GREEN = HexColor('#27ae60')
ORANGE = HexColor('#e67e22')


def build():
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'gtm-cc-architecture.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.7*inch, rightMargin=0.7*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Title'],
        fontSize=26, textColor=DARK, spaceAfter=4, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
        fontSize=12, textColor=GRAY, alignment=TA_CENTER, spaceAfter=20)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
        fontSize=18, textColor=BLUE, spaceBefore=20, spaceAfter=10)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
        fontSize=14, textColor=DARK, spaceBefore=14, spaceAfter=8)
    h3 = ParagraphStyle('H3', parent=styles['Heading3'],
        fontSize=11, textColor=BLUE, spaceBefore=10, spaceAfter=6)
    body = ParagraphStyle('Body', parent=styles['Normal'],
        fontSize=10, textColor=DARK, spaceAfter=6, leading=14)
    body_bold = ParagraphStyle('BodyBold', parent=body, fontName='Helvetica-Bold')
    code_style = ParagraphStyle('Code', parent=styles['Normal'],
        fontSize=8.5, fontName='Courier', textColor=DARK, backColor=LIGHT_GRAY,
        spaceAfter=8, leading=11, leftIndent=12, rightIndent=12,
        borderWidth=0.5, borderColor=HexColor('#dddddd'), borderPadding=6)
    bullet_style = ParagraphStyle('Bullet', parent=body,
        leftIndent=24, bulletIndent=12, spaceAfter=4)
    note_style = ParagraphStyle('Note', parent=body,
        fontSize=9, textColor=ACCENT, leftIndent=12)
    scenario_title = ParagraphStyle('ScenarioTitle', parent=body,
        fontName='Helvetica-Bold', fontSize=11, textColor=BLUE, spaceBefore=10, spaceAfter=4)

    story = []

    # ═══════════════════════════════════════════════════
    # COVER
    # ═══════════════════════════════════════════════════
    story.append(Spacer(1, 80))
    story.append(Paragraph("GTM-CC", title_style))
    story.append(Paragraph("Complete System Architecture", ParagraphStyle('Sub1', parent=subtitle_style, fontSize=16, textColor=BLUE)))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="60%", thickness=2, color=BLUE))
    story.append(Spacer(1, 10))
    story.append(Paragraph("One Neon DB &bull; Three Roles &bull; 30 Clients &bull; Every Scenario", subtitle_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("v4.0 &mdash; April 2026", ParagraphStyle('Ver', parent=subtitle_style, fontSize=10, textColor=GRAY)))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════
    story.append(Paragraph("Contents", h1))
    toc_items = [
        ("Part 1", "The Database (Neon) — 5 Tables"),
        ("Part 2", "What Happens on Clay"),
        ("Part 3", "A Typical Day — Every Scenario"),
        ("Part 4", "Edge Cases"),
        ("Part 5", "Summary & Cost"),
    ]
    for num, desc in toc_items:
        story.append(Paragraph(f"<b>{num}:</b> {desc}", body))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # PART 1: THE DATABASE
    # ═══════════════════════════════════════════════════
    story.append(Paragraph("Part 1: The Database (Neon)", h1))
    story.append(Paragraph(
        "Everything runs on <b>one Neon PostgreSQL database</b>. Five tables. "
        "All access goes through <font face='Courier'>scripts/db.py</font> — no raw SQL from operators.", body))
    story.append(Spacer(1, 8))

    # ── Table 1: clients ──
    story.append(Paragraph("Table 1: clients", h2))
    story.append(Paragraph(
        "<b>Source:</b> Tally onboarding form webhook &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Updated by:</b> Copy Strategist &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Read by:</b> All roles", body))

    clients_data = [
        ['Column', 'Type', 'Description'],
        ['client_id', 'UUID PK', 'From Tally onboarding'],
        ['client_name', 'text', 'e.g., "Hector"'],
        ['client_website', 'text', 'e.g., "hector.com"'],
        ['client_status', 'text', 'in_onboarding / active / paused / churned'],
        ['target_icp_details', 'text', 'ICP description across segments'],
        ['target_persona', 'text', 'Target decision-maker persona'],
        ['pain_points', 'text', 'Key pain points'],
        ['client_usp_differentiators', 'text', 'USPs and differentiators'],
        ['approved', 'boolean', 'Must be true before downstream use'],
        ['primary_poc_name', 'text', 'Main client contact'],
        ['primary_poc_email', 'text', ''],
        ['all_client_sales_resources', 'text', 'Case studies, FAQs, resources'],
        ['all_social_proof_brand_names', 'text', 'Logo wall brands'],
        ['client_call_to_action', 'text', 'What client wants prospects to do'],
        ['complimentary_sales_value', 'text', 'Free offer / lead magnet'],
        ['casestudy_or_leadmagnet_links', 'text', 'Links for autoresponder'],
        ['dnc_list_url', 'text', 'Do Not Contact list'],
        ['client_crm', 'text', 'hubspot / pipedrive / salesforce'],
        ['ar_mode', 'text', 'all_manual / first_auto / all_auto'],
        ['sequencer_client_campaign_name', 'text', 'Auto-generated from client_name'],
    ]
    story.append(_make_schema_table(clients_data))
    story.append(Spacer(1, 8))

    # ── Table 2: segments ──
    story.append(Paragraph("Table 2: segments", h2))
    story.append(Paragraph(
        "<b>Source:</b> Copy Strategist creates &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Key:</b> value_prop lives HERE (not on clients or recipes)", body))

    segments_data = [
        ['Column', 'Type', 'Description'],
        ['segment_id', 'serial PK', 'Stored in leads.segment_ids[]'],
        ['client_id', 'UUID FK', 'Which client'],
        ['segment_name', 'text', 'e.g., "Retail", "Agency", "Enterprise"'],
        ['segment_tag', 'text', 'Human-readable label'],
        ['description', 'text', ''],
        ['value_prop', 'text', 'Value proposition for this segment'],
        ['leadlist_context', 'text', 'Targeting criteria for this segment'],
        ['status', 'text', 'active / paused / archived'],
    ]
    story.append(_make_schema_table(segments_data))
    story.append(Paragraph(
        "UNIQUE constraint: (client_id, segment_name) — no duplicate segments per client.", note_style))
    story.append(Spacer(1, 8))

    # ── Table 3: leads ──
    story.append(PageBreak())
    story.append(Paragraph("Table 3: leads", h2))
    story.append(Paragraph(
        "<b>Source:</b> Data team + Clay enrichment &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Dedup key:</b> email (case-insensitive)", body))

    leads_data = [
        ['Column', 'Type', 'Description'],
        ['lead_id', 'serial PK', ''],
        ['email', 'text UNIQUE', 'Primary dedup key'],
        ['first_name / last_name / full_name', 'text', 'Identity'],
        ['job_title', 'text', ''],
        ['linkedin_profile_url', 'text', ''],
        ['company_name / company_domain', 'text', 'Company info'],
        ['company_website', 'text', ''],
        ['industry', 'text', ''],
        ['monthly_visits', 'int', 'From SimilarWeb or Clay'],
        ['employee_count', 'text', 'Clay sends ranges'],
        ['email_verified', 'text', ''],
        ['email_verified_at', 'timestamptz', 'Last verification date'],
        ['is_catchall', 'text', ''],
        ['mx_provider', 'text', 'Gmail, Outlook, etc.'],
        ['has_email_security_gateway', 'text', ''],
        ['lcp', 'float', 'Largest Contentful Paint'],
        ['tti', 'float', 'Time to Interactive'],
        ['aov', 'float', 'Average Order Value'],
        ['segment_ids', 'int[]', 'Array of segment IDs (multi-segment)'],
        ['info_tags', 'text[]', 'Free-form context tags'],
        ['extra_data', 'jsonb', 'Flexible catch-all for Clay enrichment'],
    ]
    story.append(_make_schema_table(leads_data))
    story.append(Paragraph(
        "Same lead email can belong to multiple segments via segment_ids array. "
        "Use /inspect-extra-data to see what's in extra_data.", note_style))
    story.append(Spacer(1, 8))

    # ── Table 4: recipes ──
    story.append(Paragraph("Table 4: recipes", h2))
    story.append(Paragraph(
        "<b>Source:</b> Copy Strategist via Claude Code &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Versioning:</b> ANY change = new version row", body))

    recipes_data = [
        ['Column', 'Type', 'Description'],
        ['recipe_id', 'serial PK', ''],
        ['client_id', 'UUID FK', 'Which client'],
        ['segment_id', 'int FK', 'Which segment'],
        ['version', 'int', 'Starts at 1, bumps on ANY change'],
        ['status', 'text', 'active / inactive / testing'],
        ['approach_content', 'text', 'Full playbook (reference, NOT pushed to Clay)'],
        ['data_variables_required', 'text[]', "e.g., ARRAY['aov','review_count']"],
        ['clay_template_name', 'text', 'Which saved Clay template to use'],
        ['clay_instructions', 'text', 'Step-by-step for the Clay operator'],
        ['notes', 'text', 'What changed in this version'],
    ]
    story.append(_make_schema_table(recipes_data))
    story.append(Paragraph(
        "Only ONE active recipe per client-segment. Old version set to 'inactive' before new version activates.", note_style))
    story.append(Spacer(1, 8))

    # ── Table 5: email_outputs ──
    story.append(PageBreak())
    story.append(Paragraph("Table 5: email_outputs", h2))
    story.append(Paragraph(
        "<b>Source:</b> Clay push-back (HTTP Col 3) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Key feature:</b> Enables email reuse across batches", body))

    outputs_data = [
        ['Column', 'Type', 'Description'],
        ['output_id', 'serial PK', ''],
        ['lead_id', 'int FK', 'Which lead'],
        ['client_id', 'UUID FK', 'Denormalized for queries'],
        ['segment_id', 'int FK', ''],
        ['recipe_id', 'int FK', 'Which recipe generated this'],
        ['recipe_version', 'int', 'Which version of the recipe'],
        ['selected_approach', 'text', 'Which approach ran'],
        ['email_1_variant_a / _b', 'text', 'Primary email 1 + A/B variant'],
        ['email_2_variant_a / _b', 'text', 'Primary email 2 + A/B variant'],
        ['email_3_variant_a / _b', 'text', 'Primary email 3 + A/B variant'],
        ['company_summary', 'text', 'Website scrape output'],
        ['batch_id', 'text', 'Groups leads processed together'],
    ]
    story.append(_make_schema_table(outputs_data))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Reuse check query:", h3))
    story.append(Paragraph(
        "SELECT * FROM email_outputs eo JOIN recipes r ON eo.recipe_id = r.recipe_id "
        "WHERE eo.lead_id = {lead_id} AND r.status = 'active' AND eo.recipe_version = r.version", code_style))
    story.append(Paragraph("If a row exists = REUSE (pull existing emails). If not = GENERATE (send to Clay).", body))

    # ═══════════════════════════════════════════════════
    # PART 2: WHAT HAPPENS ON CLAY
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Part 2: What Happens on Clay", h1))
    story.append(Paragraph(
        "Clay is a <b>disposable processing layer</b>. Use it, get results, push back to Neon, archive the table.", body))

    # ── 38-Field Webhook Payload ──
    story.append(Paragraph("Webhook Push: Neon to Clay (38 Fields)", h2))
    story.append(Paragraph(
        "When pushing leads to Clay via /push-to-clay, ALL 38 fields are included:", body))

    payload_data = [
        ['Group', 'Fields', 'Count'],
        ['Identity', 'lead_id, email, first_name, last_name, full_name, job_title, linkedin_profile_url', '7'],
        ['Company', 'company_name, company_domain, company_website, industry, employee_count', '5'],
        ['Enrichment', 'monthly_visits, lcp, tti, aov', '4'],
        ['Verification', 'email_verified, email_verified_at, is_catchall, mx_provider, has_email_security_gateway', '5'],
        ['Client', 'client_id, client_name', '2'],
        ['Segment', 'segment_id, segment_name, segment_tag, leadlist_context, value_prop', '5'],
        ['Batch/Recipe', 'batch_id, recipe_id, recipe_version', '3'],
        ['Existing Outputs', 'email_1-3_variant_a, email_1-3_variant_b, selected_approach', '7'],
    ]
    story.append(_make_data_table(payload_data))
    story.append(Paragraph("Pre-filled enrichment fields mean Clay SKIPS enrichment for those leads (saves credits).", note_style))
    story.append(Spacer(1, 8))

    # ── Clay Table Columns ──
    story.append(Paragraph("Typical Clay Table Structure", h2))
    clay_cols = [
        ['#', 'Column', 'Type', 'Purpose'],
        ['1-17', 'Import columns', 'Import', 'Lead data from webhook push'],
        ['18', 'Email Re-verify', 'Enrichment', 'Re-verifies email (always runs)'],
        ['19', 'StoreLeads AOV', 'Enrichment', 'Gets AOV (only if empty)'],
        ['20', 'PageSpeed LCP/TTI', 'Enrichment', 'Gets LCP + TTI (only if empty)'],
        ['21', 'SimilarWeb Visits', 'Enrichment', 'Gets monthly visits (only if empty)'],
        ['22', 'Website Scrape', 'Claygent', 'Scrapes company website (50-100 word summary)'],
        ['23', 'Approach Selector', 'Formula', 'Picks recipe per lead based on data availability'],
        ['24', 'Selected Recipe Text', 'Formula', 'Pulls approach_content based on selector'],
        ['25', 'Researcher', 'Claygent', 'Web research for signals (only when required)'],
        ['26', 'Copywriter', 'Use AI', 'Writes email_1/2/3_variant_a/b (GPT-4o-mini)'],
        ['27', 'Style Checker', 'Use AI', 'Fixes spam words, humanizes (GPT-4o-mini)'],
        ['28', 'Recipe Name', 'Formula', 'Tracking field'],
        ['29', 'Recipe Version', 'Formula', 'Tracking field'],
    ]
    t = Table(clay_cols, colWidths=[30, 120, 65, 240])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # ── Push-back ──
    story.append(Paragraph("HTTP Push-back: Clay to Neon (3 HTTP Columns)", h2))

    story.append(Paragraph("<b>HTTP Col 1 — Verification</b> (UPDATE leads)", h3))
    story.append(Paragraph(
        "Fields: email_verified, email_verified_at, is_catchall, mx_provider, has_email_security_gateway", body))

    story.append(Paragraph("<b>HTTP Col 2 — Enrichment</b> (UPDATE leads)", h3))
    story.append(Paragraph(
        "Fields: lcp, tti, aov, monthly_visits + extra_data JSONB merge (any custom fields)", body))

    story.append(Paragraph("<b>HTTP Col 3 — Email Outputs</b> (INSERT email_outputs)", h3))
    story.append(Paragraph(
        "Fields: lead_id, client_id, segment_id, recipe_id, recipe_version, selected_approach, "
        "email_1/2/3_variant_a (9 params total)", body))
    story.append(Paragraph(
        "Use /generate-http-query in Claude Code to generate the exact HTTP body for any push-back column.", note_style))

    # ═══════════════════════════════════════════════════
    # PART 3: A TYPICAL DAY
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Part 3: A Typical Day — Every Scenario", h1))

    # ── Copy Strategist ──
    story.append(Paragraph("Copy Strategist's Day", h2))

    story.append(Paragraph("Morning: Weekly Planning (Monday, 30 min)", scenario_title))
    story.append(Paragraph(
        "Opens Claude Code. \"Show me all clients' status.\" Gets a dashboard of all clients, segments, "
        "active recipes, pending leads, and action items. Identifies which clients need new recipes, "
        "which are running low on TAM, which recipes to review.", body))

    story.append(Paragraph("Task 1: Create New Recipe", scenario_title))
    story.append(Paragraph(
        "Uses /create-recipe. Pulls client context from DB, selects segment, "
        "writes approach content with Claude, defines data variables, writes Clay instructions, "
        "tests on 50 sample leads, reviews output, saves to DB. ~15 minutes.", body))

    story.append(Paragraph("Task 2: Update Underperforming Recipe", scenario_title))
    story.append(Paragraph(
        "Queries performance by recipe. Finds underperformer (0.8% reply rate). "
        "Edits the approach content. Tests on 10 leads. Saves as new version (v2). "
        "Old version auto-deactivated. ~10 minutes.", body))

    story.append(Paragraph("Task 3: Cross-Client Review", scenario_title))
    story.append(Paragraph(
        "\"Show me bottom 5 recipes by reply rate across all clients.\" Makes kill/rework/keep decisions. "
        "Manages all 30 clients from one Claude Code session.", body))
    story.append(Spacer(1, 8))

    # ── Campaign Operator ──
    story.append(Paragraph("Campaign Operator's Day", h2))

    story.append(Paragraph("Morning: Check Slack Alerts", scenario_title))
    story.append(Paragraph(
        "Daily Slack bot shows: URGENT (< 2 days of leads), PREPARE (< 5 days), ON TRACK, "
        "and INFRA ALERTS (0% reply rate campaigns).", body))

    scenarios = [
        ("Scenario A: Same Recipe, Need Leads (60% of days)",
         "Query DB for reuse-eligible leads. Split: REUSE (pull existing emails from DB, instant) + "
         "GENERATE (send to Clay operator). Combine, upload to sequencer. 15 min."),
        ("Scenario B: Recipe Changed (20% of days)",
         "Recipe v2 exists. Leads with old version need regeneration. Leads with other recipes still reusable. "
         "Only send the delta to Clay. 15 min + Clay wait."),
        ("Scenario C: Bad Infrastructure (10% of days)",
         "0% reply = domain issue. Pull same emails from DB (no regeneration). "
         "Upload to new sequencer campaign with fresh domains. 10 min. Zero Clay credits."),
        ("Scenario D: New Client First Campaign (5% of days)",
         "All leads are new. All go through Clay. Full pipeline. 20 min + Clay processing."),
        ("Scenario E: Re-approach After 30-Day Cooldown",
         "Leads contacted 30+ days ago, no reply. Regenerate through Clay (fresh research, new signals). "
         "New email_output rows created, old ones preserved."),
        ("Scenario F: Add Leads to Live Campaign",
         "Pull new leads, same recipe. New sequencer campaign (never add to running campaigns). "
         "Same recipe tracking for performance comparison."),
    ]
    for title, desc in scenarios:
        story.append(Paragraph(title, scenario_title))
        story.append(Paragraph(desc, body))
    story.append(Spacer(1, 8))

    # ── Clay Operator ──
    story.append(PageBreak())
    story.append(Paragraph("Clay Operator's Day", h2))

    story.append(Paragraph("Morning: Check Assignments", scenario_title))
    story.append(Paragraph(
        "Views pending Clay runs from campaign operator. Typical: 3-5 assignments, 3,900 total leads.", body))

    story.append(Paragraph("For Each Assignment (Step by Step)", scenario_title))
    steps = [
        "Read recipe instructions from DB (SELECT clay_instructions FROM recipes)",
        "Clone saved Clay template (or create new if first run for this client)",
        "Import leads (pre-filled enrichment fields = Clay skips those, saves credits)",
        "Run the table (20-40 min for 800 leads)",
        "Spot-check 5-10 rows for quality",
        "Push results back to Neon via HTTP columns (verification + enrichment + email outputs)",
        "Confirm in DB, archive Clay table, notify campaign operator",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(f"<b>{i}.</b> {step}", bullet_style))

    story.append(Paragraph(
        "Time per assignment: ~10 min setup + 20-40 min processing + 10 min push-back = ~40-60 min", note_style))

    # ═══════════════════════════════════════════════════
    # PART 4: EDGE CASES
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Part 4: Edge Cases", h1))

    edge_cases = [
        ("Same Lead, Different Clients",
         "john@acme.com can exist for both Hector (Retail) and Owner.com (Restaurant). "
         "Separate lead rows, separate email_outputs. DNC is per-client — if John says \"not interested\" "
         "to Hector, his Owner.com lead is unaffected."),
        ("Lead Gets Different Recipe on Re-approach",
         "March: approach selector picks ROI Calculator (AOV data available). "
         "April: 30-day cooldown passed, new recipe Page Speed Angle now available (LCP enriched). "
         "Selector picks Page Speed. Two email_output rows, both preserved. Enables per-recipe performance tracking."),
        ("A/B Test a New Recipe",
         "Pull 500 leads. Split: 250 get only Recipe A active in selector, 250 get only Recipe B. "
         "Or let the selector distribute naturally. After 2 weeks, query performance by recipe_name."),
        ("Data Team Adds New TAM Mid-Month",
         "New leads appear with no email_outputs. Next batch prep automatically picks them up as GENERATE leads. "
         "No disruption to existing campaigns."),
        ("Client Churns",
         "Set client_status = 'churned'. All recipes go inactive. All leads stay in DB (historical). "
         "If client reactivates, all data is still there, recipes can be reactivated."),
        ("Clay Table Fails Mid-Processing",
         "Export completed rows (e.g., 600 of 800). Push those to Neon. "
         "Re-import remaining 200 to new Clay table. Rerun. Net result: all processed, two passes."),
        ("Campaign Operator Uploads Wrong CSV",
         "No DB corruption — error is only on sequencer side. Pause wrong campaign immediately. "
         "CSV filenames include client + segment for prevention."),
    ]
    for title, desc in edge_cases:
        story.append(Paragraph(title, scenario_title))
        story.append(Paragraph(desc, body))
    story.append(Spacer(1, 4))

    # ═══════════════════════════════════════════════════
    # PART 5: SUMMARY
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Part 5: Summary", h1))

    # ── Role Summary ──
    story.append(Paragraph("What Each Role Does Daily", h2))
    role_summary = [
        ['Role', 'Daily Tasks', 'Time/Day', 'Tools'],
        ['Copy\nStrategist', 'Review performance, update recipes,\ncreate new recipes, test on samples', '1-2 hrs\n(across all\nclients)', 'Claude Code\n+ Neon DB'],
        ['Campaign\nOperator', 'Check Slack alerts, run reuse checks,\nexport CSVs, upload to sequencer', '2-3 hrs', 'Dashboard\n+ Neon\n+ Sequencers'],
        ['Clay\nOperator', 'Read recipe instructions, set up Clay\ntables, run tables, push results back', '3-4 hrs\n(3-5 Clay\nruns/day)', 'Clay + Neon\n+ push-back'],
    ]
    t = Table(role_summary, colWidths=[65, 195, 65, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # ── DB Scale ──
    story.append(Paragraph("DB Scale at 30 Clients", h2))
    scale_data = [
        ['Table', 'Rows', 'Growth Rate'],
        ['clients', '30', 'Slow (new clients)'],
        ['segments', '~90 (3 per client avg)', 'Slow'],
        ['leads', '250K-500K', '~20-30K/month (new TAM)'],
        ['recipes', '~200-400 (with versions)', '~20-30/month'],
        ['email_outputs', '500K-1M+', '~80-100K/month'],
    ]
    story.append(_make_data_table(scale_data))
    story.append(Spacer(1, 10))

    # ── Cost ──
    story.append(Paragraph("Monthly Cost", h2))
    cost_data = [
        ['Item', 'Monthly Cost'],
        ['Neon DB (Pro plan)', '$19-69/mo'],
        ['Clay', 'Per usage (existing cost, no change)'],
        ['GPT-4o-mini (via Clay Use AI)', '~$0.005/lead x 80K = ~$400'],
        ['SerpAPI (via Clay Claygent)', 'Included in Clay cost'],
        ['Sequencer API sync', 'Minimal (cron job)'],
        ['Slack notifications', 'Free (webhook)'],
        ['Total new cost', '$20-70/mo for Neon (Clay stays same)'],
    ]
    t = Table(cost_data, colWidths=[230, 225])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)

    # ── Commands Reference ──
    story.append(Spacer(1, 14))
    story.append(Paragraph("Available Commands (Claude Code)", h2))
    cmd_data = [
        ['Command', 'Role', 'What It Does'],
        ['/whoami', 'All', 'Set your role for the session'],
        ['/pull-leads', 'Strategist, Clay', 'Pull leads for a client + segment'],
        ['/add-leads', 'Strategist, Clay', 'Import leads from CSV (auto-column-mapping + dedup)'],
        ['/push-to-clay', 'Strategist, Clay', 'Push leads to Clay via webhook (38 fields)'],
        ['/generate-http-query', 'Strategist, Clay', 'Generate HTTP push-back body for Clay columns'],
        ['/inspect-extra-data', 'All', 'Show extra_data JSONB keys with fill rates'],
        ['/create-recipe', 'Strategist only', 'Create a new email recipe (guided)'],
        ['/test-recipe', 'Strategist only', 'Test a recipe on sample leads'],
        ['/check-outputs', 'All', 'View email output stats'],
        ['/export-csv', 'All', 'Export leads + emails as CSV for sequencer'],
    ]
    t = Table(cmd_data, colWidths=[120, 100, 235])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)

    # Build
    doc.build(story)
    print(f"Generated: {output_path}")
    return output_path


def _make_schema_table(data):
    """Create a schema table with standard styling."""
    t = Table(data, colWidths=[145, 70, 240])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def _make_data_table(data):
    """Create a generic data table."""
    t = Table(data, colWidths=[140, 235, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


if __name__ == '__main__':
    build()
