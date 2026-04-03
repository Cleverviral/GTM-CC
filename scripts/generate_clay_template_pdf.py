"""
Generate the Clay Template Specification PDF.
Run: python3 scripts/generate_clay_template_pdf.py
Output: docs/clay-template-spec.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
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
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'clay-template-spec.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.7*inch, rightMargin=0.7*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Title'],
        fontSize=22, textColor=DARK, spaceAfter=6, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
        fontSize=11, textColor=GRAY, alignment=TA_CENTER, spaceAfter=20)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
        fontSize=16, textColor=BLUE, spaceBefore=16, spaceAfter=8,
        borderWidth=0, borderPadding=0)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
        fontSize=13, textColor=DARK, spaceBefore=12, spaceAfter=6)
    h3 = ParagraphStyle('H3', parent=styles['Heading3'],
        fontSize=11, textColor=BLUE, spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle('Body', parent=styles['Normal'],
        fontSize=9.5, textColor=DARK, spaceAfter=6, leading=13)
    code_style = ParagraphStyle('Code', parent=styles['Normal'],
        fontSize=8, fontName='Courier', textColor=DARK, backColor=LIGHT_GRAY,
        spaceAfter=6, leading=11, leftIndent=10, rightIndent=10,
        borderWidth=0.5, borderColor=HexColor('#dddddd'), borderPadding=6)
    bullet = ParagraphStyle('Bullet', parent=body,
        leftIndent=20, bulletIndent=10)
    note_style = ParagraphStyle('Note', parent=body,
        fontSize=9, textColor=ACCENT, leftIndent=10, borderWidth=0)

    story = []

    # ── Title ──
    story.append(Paragraph("Clay Template Specification", title_style))
    story.append(Paragraph("GTM-CC Standardized Clay Table Layout — v1.0", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE))
    story.append(Spacer(1, 12))

    # ── How It Works ──
    story.append(Paragraph("How It Works", h1))
    story.append(Paragraph("Every Clay table follows this structure regardless of client or scenario:", body))
    for step in [
        "<b>1.</b> We push leads from Neon → Clay via webhook (Section A: 41 fields per lead)",
        "<b>2.</b> Clay processes them: verification → enrichment → email generation (Sections B–G)",
        "<b>3.</b> Clay pushes results back to Neon via 3 HTTP columns (Sections C, F, H)",
    ]:
        story.append(Paragraph(step, bullet))
    story.append(Spacer(1, 6))

    # ── Variant Flexibility ──
    story.append(Paragraph("Variant Flexibility", h2))
    story.append(Paragraph(
        "The DB always has 9 email columns (email_1/2/3_variant_a/b/c) + 2 subject lines. "
        "Not every recipe uses all variants. The recipe's <b>clay_instructions</b> tells the Clay operator "
        "which AI columns to create. Unused variants stay NULL in the DB.", body))
    story.append(Paragraph(
        "<b>Recipe v1</b> (1 variant/email): Clay table has 3 AI columns → email_X_variant_a populated, b/c = NULL", bullet))
    story.append(Paragraph(
        "<b>Recipe v2</b> (3 variants/email): Clay table has 9 AI columns → all email_X_variant_a/b/c populated", bullet))
    story.append(Paragraph(
        "HTTP Column 3 always references all 9 columns. Non-existent Clay columns resolve to empty → stored as NULL.", bullet))

    story.append(PageBreak())

    # ── Section A ──
    story.append(Paragraph("Section A: Import Data (Webhook Push from Neon)", h1))
    story.append(Paragraph(
        "Auto-created when the first lead is pushed. The <font face='Courier'>/push-to-clay</font> command sends this exact JSON per lead.", body))

    # Identity table
    story.append(Paragraph("Identity Fields (7)", h3))
    identity_data = [
        ['#', 'Field', 'Source', 'Notes'],
        ['1', 'lead_id', 'leads.lead_id', 'Primary key — used by all 3 HTTP columns'],
        ['2', 'email', 'leads.email', "The lead's email"],
        ['3', 'first_name', 'leads.first_name', ''],
        ['4', 'last_name', 'leads.last_name', ''],
        ['5', 'full_name', 'leads.full_name', ''],
        ['6', 'job_title', 'leads.job_title', ''],
        ['7', 'linkedin_profile_url', 'leads.linkedin_profile_url', ''],
    ]
    story.append(_make_table(identity_data))

    # Company table
    story.append(Paragraph("Company Fields (5)", h3))
    company_data = [
        ['#', 'Field', 'Source', 'Notes'],
        ['8', 'company_name', 'leads.company_name', ''],
        ['9', 'company_domain', 'leads.company_domain', 'Used for enrichment lookups'],
        ['10', 'company_website', 'leads.company_website', 'Used for scraping'],
        ['11', 'industry', 'leads.industry', ''],
        ['12', 'employee_count', 'leads.employee_count', 'Range string from Clay'],
    ]
    story.append(_make_table(company_data))

    # Client + Segment
    story.append(Paragraph("Client + Segment (5)", h3))
    cs_data = [
        ['#', 'Field', 'Source', 'Notes'],
        ['13', 'client_id', 'clients.client_id', 'UUID — needed for email_outputs INSERT'],
        ['14', 'client_name', 'clients.client_name', 'Human reference in Clay'],
        ['15', 'segment_id', 'segments.segment_id', 'INT — needed for email_outputs INSERT'],
        ['16', 'segment_name', 'segments.segment_name', 'Human reference'],
        ['17', 'segment_tag', 'segments.segment_tag', 'Human reference'],
    ]
    story.append(_make_table(cs_data))

    # Verification
    story.append(Paragraph("Verification Fields (5)", h3))
    ver_data = [
        ['#', 'Field', 'Source', 'Notes'],
        ['18', 'email_verified', 'leads.email_verified', 'Current status'],
        ['19', 'email_verified_at', 'leads.email_verified_at', 'When last verified'],
        ['20', 'is_catchall', 'leads.is_catchall', ''],
        ['21', 'mx_provider', 'leads.mx_provider', ''],
        ['22', 'has_email_security_gateway', 'leads.has_email_...', ''],
    ]
    story.append(_make_table(ver_data))

    # Enrichment
    story.append(Paragraph("Enrichment Fields (4)", h3))
    enr_data = [
        ['#', 'Field', 'Source', 'Notes'],
        ['23', 'monthly_visits', 'leads.monthly_visits', ''],
        ['24', 'lcp', 'leads.lcp', 'Largest Contentful Paint'],
        ['25', 'tti', 'leads.tti', 'Time to Interactive'],
        ['26', 'aov', 'leads.aov', 'Average Order Value'],
    ]
    story.append(_make_table(enr_data))

    # Recipe
    story.append(Paragraph("Recipe Context (3)", h3))
    rec_data = [
        ['#', 'Field', 'Source', 'Notes'],
        ['27', 'recipe_id', 'recipes.recipe_id', 'Active recipe for this segment'],
        ['28', 'current_recipe_version', 'recipes.version', 'Current version number'],
        ['29', 'batch_id', 'Generated', '{client}_{segment}_{YYYYMMDD}_{seq}'],
    ]
    story.append(_make_table(rec_data))

    # Existing outputs
    story.append(Paragraph("Existing Email Outputs (12)", h3))
    story.append(Paragraph(
        "Only populated if the lead already has outputs in the DB. Lets Clay skip regeneration when recipe version is unchanged.", body))
    out_data = [
        ['#', 'Field', 'Source'],
        ['30', 'last_recipe_version', 'email_outputs.recipe_version'],
        ['31', 'existing_subject_line_1', 'email_outputs.subject_line_1'],
        ['32', 'existing_subject_line_2', 'email_outputs.subject_line_2'],
        ['33–35', 'existing_email_1_variant_a/b/c', 'email_outputs.email_1_variant_*'],
        ['36–38', 'existing_email_2_variant_a/b/c', 'email_outputs.email_2_variant_*'],
        ['39–41', 'existing_email_3_variant_a/b/c', 'email_outputs.email_3_variant_*'],
    ]
    story.append(_make_table(out_data, col_widths=[50, 200, 220]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Total import fields: 41</b>", body))

    story.append(PageBreak())

    # ── Section B: Verification Waterfall ──
    story.append(Paragraph("Section B: Verification Waterfall (Clay Template)", h1))
    story.append(Paragraph(
        "These columns are part of the Clay table template. The Clay operator sets them up once per table.", body))

    ver_wf = [
        ['#', 'Column', 'Type', 'What It Does'],
        ['1', 'Reverify Email', 'Action', 'Primary re-verification'],
        ['2', 'Normal Reverify', 'Action', 'Secondary check'],
        ['3', 'Catchall Reverify', 'Action', 'Catchall-specific check'],
        ['4', 'Reoon Again', 'Action', 'Reoon verification pass'],
        ['5', 'Verified Normal Email', 'Formula', 'Consolidates normal results'],
        ['6', 'Catchall Reverifier', 'Formula', 'Consolidates catchall results'],
        ['7', 'TLDR', 'Formula', 'Summary of verification chain'],
        ['8', 'Verified Catchalls', 'Formula', 'Final catchall determination'],
        ['9', 'Reverified Emails', 'Formula', 'Combined reverified results'],
        ['10', 'Final Email', 'Formula', 'The final verified email'],
        ['11', 'Updated Email Validity', 'Formula', 'valid / invalid / risky'],
        ['12', 'Email Verified Date', 'Formula', 'Timestamp of verification'],
    ]
    story.append(_make_table(ver_wf))

    # ── Section C: HTTP Column 1 ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section C: HTTP Column 1 — Verification Push-Back", h1))
    story.append(Paragraph("<b>Target:</b> UPDATE leads table", body))
    story.append(Paragraph("<b>Triggers:</b> After verification waterfall completes", body))
    story.append(Spacer(1, 4))

    sql1 = (
        'UPDATE leads SET<br/>'
        '  email_verified = COALESCE(NULLIF($1, \'\'), email_verified),<br/>'
        '  email_verified_at = CASE WHEN NULLIF($1, \'\') IS NOT NULL<br/>'
        '    THEN NOW() ELSE email_verified_at END,<br/>'
        '  is_catchall = COALESCE(NULLIF($2, \'\'), is_catchall),<br/>'
        '  mx_provider = COALESCE(NULLIF($3, \'\'), mx_provider),<br/>'
        '  has_email_security_gateway = COALESCE(NULLIF($4, \'\'),<br/>'
        '    has_email_security_gateway)<br/>'
        'WHERE lead_id = $5'
    )
    story.append(Paragraph(sql1, code_style))

    story.append(Paragraph("Params: {{Updated Email Validity}}, {{Is Catchall}}, {{Mx Provider}}, "
                           "{{Has Email Security Gateway}}, {{Lead Id}}", body))
    story.append(Paragraph(
        "<b>Pattern:</b> COALESCE(NULLIF($1, ''), existing_value) — only updates if Clay sends a non-empty value. "
        "Empty strings from Clay are ignored, preserving existing DB data.", note_style))

    story.append(PageBreak())

    # ── Section D: Decision Logic ──
    story.append(Paragraph("Section D: Decision Logic (Clay Formula Columns)", h1))

    dec_data = [
        ['Column', 'Logic'],
        ['Needs Enrichment', 'IF(AND(LCP = "", TTI = ""), "yes", "no")'],
        ['Needs Email Generation', 'IF(OR(Current Recipe Version != Last Recipe Version,\nExisting Subject Line_1 = ""), "generate", "skip")'],
        ['Action', 'Combines above: generate / enrich_only / verify_only / skip'],
    ]
    story.append(_make_table(dec_data, col_widths=[160, 310]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Key:</b> If current_recipe_version == last_recipe_version AND existing emails exist → skip generation (reuse from DB). "
        "This is how we save Clay credits.", note_style))

    # ── Section E: Enrichment ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section E: Data Enrichment (Clay Enrichment Columns)", h1))
    story.append(Paragraph("Only runs for leads where Needs Enrichment = \"yes\". Specific columns depend on recipe's "
                           "data_variables_required and enrichment_sources.", body))

    enr_cols = [
        ['Column', 'Source', 'Gets'],
        ['PageSpeed Results', 'Google PageSpeed API', 'LCP, TTI, FCP, CLS'],
        ['LCP Result', 'Formula (extract)', 'Largest Contentful Paint'],
        ['TTI Result', 'Formula (extract)', 'Time to Interactive'],
        ['Company Data', 'StoreLeads / BuiltWith', 'Tech stack, platform, revenue'],
        ['AOV Result', 'StoreLeads', 'Average Order Value'],
        ['Employee Count', 'Clay / LinkedIn', 'Employee count range'],
        ['Industry Result', 'Clay / LinkedIn', 'Industry classification'],
    ]
    story.append(_make_table(enr_cols))

    # ── Section F: HTTP Column 2 ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section F: HTTP Column 2 — Enrichment Push-Back", h1))
    story.append(Paragraph("<b>Target:</b> UPDATE leads table", body))

    sql2 = (
        'UPDATE leads SET<br/>'
        '  lcp = COALESCE(NULLIF($1, \'\')::double precision, lcp),<br/>'
        '  tti = COALESCE(NULLIF($2, \'\')::double precision, tti),<br/>'
        '  aov = COALESCE(NULLIF($3, \'\')::double precision, aov),<br/>'
        '  monthly_visits = COALESCE(NULLIF($4, \'\')::int, monthly_visits),<br/>'
        '  employee_count = COALESCE(NULLIF($5, \'\'), employee_count),<br/>'
        '  industry = COALESCE(NULLIF($6, \'\'), industry)<br/>'
        'WHERE lead_id = $7'
    )
    story.append(Paragraph(sql2, code_style))
    story.append(Paragraph("Params: {{LCP Result}}, {{TTI Result}}, {{AOV Result}}, "
                           "{{Monthly Visits}}, {{Employee Count}}, {{Industry Result}}, {{Lead Id}}", body))

    story.append(PageBreak())

    # ── Section G: Email Generation ──
    story.append(Paragraph("Section G: Email Generation (Clay AI Columns)", h1))
    story.append(Paragraph(
        "Only runs for leads where Needs Email Generation = \"generate\". "
        "The number of variant columns created depends on the recipe.", body))

    email_cols = [
        ['#', 'Column', 'Notes'],
        ['1', 'Company Summary', '50–100 word summary from website scrape'],
        ['2', 'Selected Approach', 'Which approach from the recipe'],
        ['3', 'Subject Line 1', 'First subject line'],
        ['4', 'Subject Line 2', 'Second subject line'],
        ['5', 'Email 1 Variant A', 'Always created'],
        ['6', 'Email 1 Variant B', 'Only if recipe specifies multiple variants'],
        ['7', 'Email 1 Variant C', 'Only if recipe specifies 3 variants'],
        ['8–10', 'Email 2 Variant A/B/C', 'Follow-up email (same variant logic)'],
        ['11–13', 'Email 3 Variant A/B/C', 'Break-up email (same variant logic)'],
    ]
    story.append(_make_table(email_cols))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Recipe controls variant count:</b> The recipe's clay_instructions specify how many variant columns "
        "to create. Variant A is always present. Variants B and C are optional. HTTP Column 3 always "
        "references all 9 email columns — non-existent Clay columns resolve to NULL in the DB.", note_style))

    # ── Section H: HTTP Column 3 ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section H: HTTP Column 3 — Email Output Push-Back", h1))
    story.append(Paragraph("<b>Target:</b> INSERT INTO email_outputs table", body))
    story.append(Paragraph("<b>Triggers:</b> After email generation completes", body))
    story.append(Spacer(1, 4))

    sql3 = (
        'INSERT INTO email_outputs (<br/>'
        '  lead_id, client_id, segment_id, recipe_id, recipe_version,<br/>'
        '  selected_approach, company_summary,<br/>'
        '  subject_line_1, subject_line_2,<br/>'
        '  email_1_variant_a, email_1_variant_b, email_1_variant_c,<br/>'
        '  email_2_variant_a, email_2_variant_b, email_2_variant_c,<br/>'
        '  email_3_variant_a, email_3_variant_b, email_3_variant_c,<br/>'
        '  batch_id<br/>'
        ') VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19)'
    )
    story.append(Paragraph(sql3, code_style))
    story.append(Paragraph(
        "<b>Critical:</b> client_id and segment_id must be pushed as import data (Section A) "
        "so they're available as Clay variables here.", note_style))

    story.append(PageBreak())

    # ── Scenarios ──
    story.append(Paragraph("Scenarios", h1))

    scenarios = [
        ("Scenario 1: Full Pipeline", "New leads, new recipe",
         "Push all 41 fields. Existing emails empty. Clay runs B→C→D→E→F→G→H. "
         "Everything verified, enriched, generated, pushed back."),
        ("Scenario 2: Re-verification Only", "Email validity check",
         "Push Section A fields. Clay runs B→C only. HTTP Col 2 & 3 disabled. "
         "Email validity updated in Neon."),
        ("Scenario 3: Enrichment Only", "PageSpeed / company data",
         "Push Section A fields. Clay runs B→C→E→F. HTTP Col 3 disabled. "
         "Verification + enrichment updated. No emails generated."),
        ("Scenario 4: Recipe Changed", "Regeneration needed",
         "Push all fields. current_recipe_version > last_recipe_version. "
         "Decision logic detects mismatch → runs D→G→H. New emails generated as new rows."),
        ("Scenario 5: Reuse", "No Clay needed",
         "current_recipe_version == last_recipe_version AND existing emails exist. "
         "Don't push to Clay. Pull emails directly from Neon → CSV. Zero Clay credits."),
    ]

    for title, subtitle, desc in scenarios:
        story.append(Paragraph(f"<b>{title}</b> — {subtitle}", h2))
        story.append(Paragraph(desc, body))
        story.append(Spacer(1, 4))

    # ── Variant Count by Recipe Version ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("How Variant Counts Change Across Recipe Versions", h1))

    vc_data = [
        ['', 'Recipe v1\n(1 variant)', 'Recipe v2\n(3 variants)', 'Recipe v3\n(2 variants)'],
        ['email_1_variant_a', 'Populated', 'Populated', 'Populated'],
        ['email_1_variant_b', 'NULL', 'Populated', 'Populated'],
        ['email_1_variant_c', 'NULL', 'Populated', 'NULL'],
        ['email_2_variant_a', 'Populated', 'Populated', 'Populated'],
        ['email_2_variant_b', 'NULL', 'Populated', 'Populated'],
        ['email_2_variant_c', 'NULL', 'Populated', 'NULL'],
        ['email_3_variant_a', 'Populated', 'Populated', 'Populated'],
        ['email_3_variant_b', 'NULL', 'Populated', 'Populated'],
        ['email_3_variant_c', 'NULL', 'Populated', 'NULL'],
    ]
    story.append(_make_table(vc_data, col_widths=[130, 110, 110, 110]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Each recipe version creates a NEW row in email_outputs. Old rows are never modified. "
        "The system always pulls the latest version per lead for CSV export.", body))

    story.append(PageBreak())

    # ── Operator Checklist ──
    story.append(Paragraph("Clay Operator Checklist", h1))
    story.append(Paragraph("When setting up a new Clay table:", body))

    steps = [
        "Create blank table (not from template — webhook auto-creates columns)",
        "Set up webhook → get URL → give to /push-to-clay command",
        "Push 1 test lead → verify all 41 columns appear correctly",
        "Add verification waterfall (Section B) — use the standard template",
        "Add HTTP Column 1 (Section C) — verification push-back",
        "Add decision logic (Section D) — needs_enrichment / needs_generation formulas",
        "Add enrichment columns (Section E) — per recipe's enrichment_sources",
        "Add HTTP Column 2 (Section F) — enrichment push-back",
        "Add email generation columns (Section G) — per recipe's clay_instructions",
        "Add HTTP Column 3 (Section H) — email output push-back",
        "Test with 3 leads → verify all 3 HTTP columns fire correctly",
        "Push remaining leads → run table",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(f"<b>{i}.</b> {step}", bullet))

    story.append(Spacer(1, 12))
    story.append(Paragraph("HTTP Column Configuration (All 3)", h2))
    http_config = (
        'URL: https://{neon-host}/sql<br/>'
        'Method: POST<br/>'
        'Headers:<br/>'
        '  Content-Type: application/json<br/>'
        '  Neon-Connection-String: {connection-string-from-Mayank}<br/>'
        'Body: (see SQL queries in Sections C, F, H)'
    )
    story.append(Paragraph(http_config, code_style))
    story.append(Paragraph(
        "Get the Neon host and connection string from Mayank. Never share in Slack or email.", note_style))

    # ── Batch ID Format ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("Batch ID Format", h2))
    story.append(Paragraph("<font face='Courier'>{client_tag}_{segment_tag}_{YYYYMMDD}_{seq}</font>", body))
    story.append(Paragraph("Examples: speedsize_1m-plus_20260403_001, hector_retail_20260403_001", body))
    story.append(Paragraph("Seq increments if multiple batches run on the same day for the same client/segment.", body))

    # Build
    doc.build(story)
    print(f"Generated: {output_path}")
    return output_path


def _make_table(data, col_widths=None):
    """Create a styled table."""
    if not col_widths:
        # Auto-calculate based on number of columns
        page_width = letter[0] - 1.4 * inch
        col_widths = [page_width / len(data[0])] * len(data[0])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


if __name__ == '__main__':
    build()
