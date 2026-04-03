"""
Generate the Recipe Structure Design PDF.
Run: python3 scripts/generate_recipe_structure_pdf.py
Output: docs/recipe-structure.pdf
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
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'recipe-structure.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.7*inch, rightMargin=0.7*inch)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Title'],
        fontSize=22, textColor=DARK, spaceAfter=6, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
        fontSize=11, textColor=GRAY, alignment=TA_CENTER, spaceAfter=20)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
        fontSize=16, textColor=BLUE, spaceBefore=16, spaceAfter=8)
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
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=20, bulletIndent=10)
    bullet2 = ParagraphStyle('Bullet2', parent=body, leftIndent=40, bulletIndent=30, fontSize=9)
    note_style = ParagraphStyle('Note', parent=body,
        fontSize=9, textColor=ACCENT, leftIndent=10)
    callout = ParagraphStyle('Callout', parent=body,
        fontSize=9.5, textColor=DARK, backColor=LIGHT_BLUE,
        leftIndent=10, rightIndent=10, borderPadding=8, spaceAfter=10)

    story = []

    # ── Title ──
    story.append(Paragraph("Recipe Structure Design", title_style))
    story.append(Paragraph("How recipes connect to Clay tables, email generation, and the DB", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE))
    story.append(Spacer(1, 12))

    # ── What is a Recipe? ──
    story.append(Paragraph("What is a Recipe?", h1))
    story.append(Paragraph(
        "A recipe is the complete playbook for generating emails for a specific client + segment. "
        "It contains everything the Clay operator and the AI copywriter need to produce personalized "
        "cold emails. One recipe = one segment's campaign strategy.", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A recipe is <b>NOT</b> a single email template. It's a strategic document that can contain "
        "multiple approaches (angles), each with its own eligibility criteria, data requirements, and "
        "email patterns. The system selects the right approach for each lead automatically.", callout))

    # ── The 5 Pieces ──
    story.append(Paragraph("The 5 Pieces of a Recipe", h1))
    story.append(Paragraph(
        "Every recipe stored in the <font face='Courier'>recipes</font> table has these 5 components. "
        "They map to the DB columns shown below.", body))

    pieces = [
        ['#', 'Piece', 'DB Column', 'What It Contains'],
        ['1', 'Approach Content', 'approach_content', 'The full playbook: all approaches, email patterns,\ncopywriter instructions, constraints, examples'],
        ['2', 'Value Prop', 'value_prop', 'Case studies, social proof library, offer structure,\nproduct explanation — shared across all approaches'],
        ['3', 'Lead List Context', 'lead_list_context', 'Who we are targeting: ICP criteria, persona,\nsales trigger, company-level and person-level filters'],
        ['4', 'Data Variables', 'data_variables_required', 'Which enrichment fields the recipe needs:\nalways-needed vs conditional per approach'],
        ['5', 'Clay Instructions', 'clay_instructions', 'Step-by-step for the Clay operator:\nwhich columns to create, formulas, enrichment sources'],
    ]
    story.append(_make_table(pieces, col_widths=[25, 110, 130, 210]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Additional DB columns:", h3))
    meta = [
        ['Column', 'Type', 'Purpose'],
        ['recipe_id', 'serial PK', 'Auto-generated ID'],
        ['client_id', 'UUID FK', 'Which client this recipe belongs to'],
        ['segment_id', 'int FK', 'Which segment (one active recipe per segment)'],
        ['version', 'int', 'Bumps on ANY change — never reuse version numbers'],
        ['status', 'text', 'active / inactive / testing'],
        ['parent_recipe_id', 'int FK', 'Links to previous version (version chain)'],
        ['enrichment_sources', 'text[]', 'PageSpeed, StoreLeads, BuiltWith, etc.'],
        ['clay_template_name', 'text', 'Name for the Clay table template'],
        ['notes', 'text', 'Why this version was created, what changed'],
    ]
    story.append(_make_table(meta))

    story.append(PageBreak())

    # ── Piece 1: Approach Content ──
    story.append(Paragraph("Piece 1: Approach Content (approach_content)", h1))
    story.append(Paragraph(
        "This is the core of the recipe. It contains ALL approaches for the segment, plus the "
        "selector logic that picks the right one per lead. Stored as a single text field in the DB.", body))

    story.append(Paragraph("Structure of approach_content", h2))
    story.append(Paragraph(
        "The approach_content field contains a structured markdown document with these sections:", body))

    ac_struct = (
        '# Recipe: {Client} — {Segment}<br/><br/>'
        '## APPROACH SELECTOR (priority cascade)<br/>'
        '...<br/><br/>'
        '---<br/><br/>'
        '## APPROACH 1: {Name}<br/>'
        '### STRATEGY<br/>'
        '### CORE PRINCIPLES<br/>'
        '### VERBATAGE<br/>'
        '### VARIABLES REQUIRED<br/>'
        '### RESEARCH REQUIRED<br/>'
        '### PATTERN (Email 1/2/3 structure)<br/>'
        '### OUTPUT EXAMPLES<br/>'
        '### CRITICAL CONSTRAINTS<br/><br/>'
        '---<br/><br/>'
        '## APPROACH 2: {Name}<br/>'
        '(same structure)<br/><br/>'
        '---<br/><br/>'
        '## APPROACH 3: {Name}<br/>'
        '(same structure)'
    )
    story.append(Paragraph(ac_struct, code_style))

    story.append(Paragraph("Anatomy of a Single Approach", h2))

    sections = [
        ['Section', 'Purpose', 'Example (Owner.com Approach 1)'],
        ['STRATEGY', '2-3 sentences: when and why this approach works',
         'Show restaurant owners how much they lose\nto delivery commissions using their own data'],
        ['CORE PRINCIPLES', '5-7 bullet points: messaging philosophy',
         'Lead with their numbers, not ours.\nCommission savings is the hook.'],
        ['VERBATAGE', 'Approved language and tone markers',
         '"ran some numbers", "you are probably paying",\n"zero-commission" (not "no commission")'],
        ['VARIABLES\nREQUIRED', 'Which data fields this approach needs.\nSplit: always-needed vs conditional',
         'Always: first_name, company, job_title\nConditional: delivery_platform, review_count'],
        ['RESEARCH\nREQUIRED', 'YES/NO + Boolean queries if YES',
         'NO — this approach is purely data-driven'],
        ['PATTERN', 'Email 1/2/3 structure.\nEach paragraph: GOAL + SIGNAL + CONSTRAINT',
         'P1: The Math Opener (their commission $)\nP2: The Mechanism (how Owner.com works)\nP3: CTA (book a demo)'],
        ['OUTPUT\nEXAMPLES', '3 complete sample emails showing the pattern applied',
         'Full emails for Pizza Owner, Asian Fusion GM,\nMexican Restaurant Operator'],
        ['CRITICAL\nCONSTRAINTS', 'Non-negotiable rules for the copywriter',
         'CTA starts with "Worth", no "!", K/M formatting,\nno percent symbol'],
    ]
    story.append(_make_table(sections, col_widths=[80, 170, 220]))

    story.append(PageBreak())

    # ── The Pattern: GOAL / SIGNAL / CONSTRAINT ──
    story.append(Paragraph("The Pattern: GOAL / SIGNAL / CONSTRAINT", h2))
    story.append(Paragraph(
        "Each email paragraph is defined by three elements. This is what makes approach-driven "
        "emails different from templates — the copywriter AI reads the <b>intent</b>, not a fill-in-the-blank.", body))

    gsc = [
        ['Element', 'What It Is', 'Example'],
        ['GOAL', 'What this paragraph should achieve.\nThe intent, not the words.',
         'Make the prospect realize how much\ncommission money they are losing'],
        ['SIGNAL', 'What data/inputs the copywriter pulls from.\nWhich variables, which context.',
         'Pull from delivery_platform, review_count,\nestimated_monthly_commission'],
        ['CONSTRAINT', 'Rules that apply to this paragraph.\nWhat the copywriter must/must not do.',
         'Use uncertainty language ("roughly", "about").\nNever state exact dollar promises.'],
    ]
    story.append(_make_table(gsc, col_widths=[80, 180, 210]))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This three-part structure means the AI copywriter adapts to each lead's data while staying "
        "on-strategy. Two leads with different data will get different emails, but both follow the same "
        "approach pattern.", callout))

    # ── Variant Count ──
    story.append(Paragraph("Variant Count Per Recipe", h2))
    story.append(Paragraph(
        "The recipe determines how many variants to generate per email. This is specified in the "
        "<font face='Courier'>clay_instructions</font> field. The Clay operator creates the corresponding "
        "number of AI columns.", body))

    variant_data = [
        ['Recipe Config', 'Clay Columns Created', 'DB Columns Used'],
        ['1 variant per email\n(minimum)', '3 AI columns:\nEmail 1/2/3 Variant A', 'email_X_variant_a = populated\nemail_X_variant_b = NULL\nemail_X_variant_c = NULL'],
        ['2 variants per email', '6 AI columns:\nEmail 1/2/3 Variant A + B', 'email_X_variant_a = populated\nemail_X_variant_b = populated\nemail_X_variant_c = NULL'],
        ['3 variants per email\n(maximum)', '9 AI columns:\nEmail 1/2/3 Variant A/B/C', 'email_X_variant_a = populated\nemail_X_variant_b = populated\nemail_X_variant_c = populated'],
    ]
    story.append(_make_table(variant_data, col_widths=[130, 170, 170]))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "HTTP Column 3 always references all 9 email columns. Non-existent Clay columns resolve "
        "to empty strings → stored as NULL in the DB. No SQL changes needed when variant count changes.", note_style))

    story.append(PageBreak())

    # ── Piece 2: Value Prop ──
    story.append(Paragraph("Piece 2: Value Prop (value_prop)", h1))
    story.append(Paragraph(
        "The shared value proposition used by ALL approaches in this recipe. The copywriter references "
        "this as <font face='Courier'>{{valueprop}}</font> in email generation. Contains:", body))

    vp_parts = [
        "What the product/service does (plain language explanation)",
        "Case studies and proof points (name, result, persona)",
        "Social proof library (organized by industry/cuisine/vertical)",
        "Offer structure (what is sold, pricing, guarantee, CTA)",
        "Value by role (different messaging for Owner vs GM vs VP)",
    ]
    for v in vp_parts:
        story.append(Paragraph(f"&bull; {v}", bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This comes from the client onboarding data (<font face='Courier'>clients.client_usp_differentiators</font>, "
        "<font face='Courier'>clients.pain_points</font>, etc.) plus campaign-specific proof points.", body))

    # ── Piece 3: Lead List Context ──
    story.append(Spacer(1, 8))
    story.append(Paragraph("Piece 3: Lead List Context (lead_list_context)", h1))
    story.append(Paragraph(
        "Defines WHO we are targeting. The copywriter uses this to understand the reader's world. "
        "Also used by the approach selector to determine eligibility.", body))

    llc_parts = [
        ['Section', 'Content'],
        ['Company-Level Criteria', 'Industry, size, geography, tech stack, platform usage'],
        ['Person-Level Criteria', 'Job titles, seniority, decision-making authority'],
        ['Sales Trigger', 'What makes NOW the right time to reach out'],
        ['Segment-Specific Notes', 'What makes this segment different from others'],
    ]
    story.append(_make_table(llc_parts, col_widths=[160, 310]))

    # ── Piece 4: Data Variables ──
    story.append(Spacer(1, 8))
    story.append(Paragraph("Piece 4: Data Variables (data_variables_required)", h1))
    story.append(Paragraph(
        "A text array listing which enrichment fields the recipe needs. Split into two categories:", body))

    story.append(Paragraph("<b>Always Needed</b> — every lead must have these:", body))
    always = ["first_name", "company_name", "job_title", "company_website", "email"]
    for a in always:
        story.append(Paragraph(f"&bull; <font face='Courier'>{a}</font>", bullet))

    story.append(Paragraph("<b>Conditional</b> — depends on which approach is selected:", body))
    story.append(Paragraph(
        "Each approach lists its own conditional variables. The approach selector runs AFTER "
        "data is available, so the system knows which variables exist for each lead.", bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Stored as a PostgreSQL text array: <font face='Courier'>ARRAY['lcp','tti','aov','review_count']</font>. "
        "This lets the system warn if required enrichment is missing before a batch runs.", note_style))

    story.append(PageBreak())

    # ── Piece 5: Clay Instructions ──
    story.append(Paragraph("Piece 5: Clay Instructions (clay_instructions)", h1))
    story.append(Paragraph(
        "Step-by-step instructions for the Clay operator (Kuldeep). This is the bridge between "
        "the strategist's recipe and the actual Clay table setup.", body))

    story.append(Paragraph("What clay_instructions should contain:", h3))
    ci_parts = [
        "How many email variants to create (1, 2, or 3 per email)",
        "Which enrichment columns to add (PageSpeed, StoreLeads, etc.)",
        "Clay formula definitions (calculated variables like estimated_monthly_commission)",
        "Approach selector formula (the IF cascade that picks the right approach per lead)",
        "AI column prompts — what instructions to give each Clay AI column",
        "Which approaches need research columns (and the Boolean queries to use)",
        "Any special formula columns needed (case study lookup, data formatting)",
    ]
    for ci in ci_parts:
        story.append(Paragraph(f"&bull; {ci}", bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The Clay operator follows these instructions literally. They don't need to understand "
        "the strategy — just set up the columns as described.", callout))

    # ── Approach Selector ──
    story.append(Paragraph("The Approach Selector (Priority Cascade)", h1))
    story.append(Paragraph(
        "When a recipe has multiple approaches, the selector picks the best one per lead. "
        "It's a priority cascade — the first eligible approach wins.", body))

    story.append(Paragraph("How it works:", h3))
    sel_steps = [
        "Each approach has an <b>eligibility formula</b> based on which data variables are present",
        "Approaches are ordered by priority (strongest first, fallback last)",
        "The selector is a nested IF: <font face='Courier'>IF(app1_eligible, app1, IF(app2_eligible, app2, app3))</font>",
        "The selected approach name is stored in <font face='Courier'>email_outputs.selected_approach</font>",
        "This gets pushed back to Neon via HTTP Column 3 for performance tracking",
    ]
    for s in sel_steps:
        story.append(Paragraph(f"&bull; {s}", bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Example: Owner.com (3 approaches)", h3))
    sel_data = [
        ['Priority', 'Approach', 'Eligibility', 'When It Fires'],
        ['1', 'Here\'s the Math', 'delivery_platform exists\nAND review_count > 50', 'We have delivery data to\ncalculate their commission loss'],
        ['2', 'Insider Remark', 'Always eligible\n(research quality at runtime)', 'No delivery data, but we can\nfind a specific company observable'],
        ['3', 'Customer Empathy', 'Always eligible\n(universal fallback)', 'No special data needed.\nFrames from customer perspective'],
    ]
    story.append(_make_table(sel_data, col_widths=[50, 110, 140, 170]))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The selector lives in <b>two places</b>: (1) inside approach_content as documentation, "
        "and (2) as a Clay formula column that the Clay operator implements from clay_instructions.", note_style))

    story.append(PageBreak())

    # ── How Recipe Connects to Clay Template ──
    story.append(Paragraph("How the Recipe Connects to the Clay Table", h1))
    story.append(Paragraph(
        "The recipe and the Clay template are two sides of the same coin. Here's the mapping:", body))

    mapping = [
        ['Recipe Piece', 'Clay Table Section', 'Who Sets It Up'],
        ['approach_content\n→ PATTERN sections', 'Section G: Email Generation\n(AI column prompts)', 'Clay operator copies prompts\nfrom clay_instructions'],
        ['approach_content\n→ SELECTOR', 'Section D: Decision Logic\n(approach selector formula)', 'Clay operator implements\nthe IF cascade formula'],
        ['value_prop', 'Referenced in AI prompts\nas {{valueprop}}', 'Pasted into Clay AI\ncolumn instructions'],
        ['data_variables_required', 'Section E: Enrichment\n(which enrichment columns to add)', 'Clay operator adds the\nrequired enrichment columns'],
        ['enrichment_sources', 'Section E: Enrichment\n(which providers to use)', 'Clay operator configures\nenrichment provider columns'],
        ['clay_instructions', 'ALL SECTIONS\n(the complete setup guide)', 'Clay operator follows\nstep by step'],
    ]
    story.append(_make_table(mapping, col_widths=[130, 170, 170]))

    # ── Recipe Versioning ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("Recipe Versioning", h1))
    story.append(Paragraph(
        "Any change to a recipe — even a small CTA tweak — creates a new version. "
        "This is how we track which version generated which emails.", body))

    story.append(Paragraph("Rules:", h3))
    ver_rules = [
        "One active recipe per client-segment at a time",
        "Any change = new row with incremented version number",
        "Old version's status set to 'inactive' before new one is activated",
        "parent_recipe_id links new version to the previous one (version chain)",
        "notes field records what changed and why",
        "email_outputs.recipe_version records which version generated each email",
        "When recipe version changes, Clay's decision logic detects the mismatch and regenerates",
    ]
    for r in ver_rules:
        story.append(Paragraph(f"&bull; {r}", bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Version lifecycle:", h3))
    lifecycle = (
        'v1 (status: active)  → Strategist creates recipe<br/>'
        'v1 (status: inactive) → Strategist edits CTA<br/>'
        'v2 (status: active)  → New version with updated CTA<br/>'
        '  → email_outputs with recipe_version=1 still exist (historical)<br/>'
        '  → next batch: decision logic detects v2 != v1 → regenerates<br/>'
        '  → new email_outputs rows with recipe_version=2'
    )
    story.append(Paragraph(lifecycle, code_style))

    story.append(PageBreak())

    # ── Creating a New Recipe (Workflow) ──
    story.append(Paragraph("Creating a New Recipe (Strategist Workflow)", h1))
    story.append(Paragraph(
        "This is the step-by-step process the strategist follows when creating a recipe via "
        "<font face='Courier'>/create-recipe</font>:", body))

    steps = [
        ("<b>Select client</b> — pull client context from DB (ICP, USPs, pain points, CTA, social proof)", None),
        ("<b>Select segment</b> — check for existing active recipe. If one exists, this will create a new version.", None),
        ("<b>Define approaches</b> — for each approach:", [
            "Name and strategy (2-3 sentences)",
            "Core principles (5-7 bullets)",
            "Verbatage (approved language markers)",
            "Variables required (always-needed + conditional)",
            "Research required (YES/NO + Boolean queries)",
            "Email pattern (GOAL/SIGNAL/CONSTRAINT per paragraph)",
            "Output examples (3 sample emails)",
            "Critical constraints (non-negotiable rules)",
        ]),
        ("<b>Set approach priority</b> — which approach fires first, second, fallback", None),
        ("<b>Define value prop</b> — case studies, social proof, offer structure (or pull from client data)", None),
        ("<b>Define lead list context</b> — who are we targeting and why now", None),
        ("<b>List data variables</b> — what enrichment fields are needed", None),
        ("<b>Write Clay instructions</b> — step-by-step for the Clay operator: columns, formulas, prompts, variant count", None),
        ("<b>Preview</b> — show the complete recipe for review", None),
        ("<b>Save</b> — deactivate old version (if any), INSERT new version as active", None),
    ]
    for i, (step, sub) in enumerate(steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet))
        if sub:
            for s in sub:
                story.append(Paragraph(f"&ndash; {s}", bullet2))

    # ── Example: SpeedSize Recipe ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("Example: What a SpeedSize Recipe Might Look Like", h2))

    example = [
        ['Field', 'Value'],
        ['client', 'SpeedSize'],
        ['segment', '1M+ Qualified'],
        ['approach_content', '2-3 approaches based on LCP/TTI performance data,\nAOV-based ROI calculations, competitor speed analysis'],
        ['value_prop', 'AI compression, preserved visual quality, AWS-sponsored POC,\n14-day free trial, case studies per vertical'],
        ['lead_list_context', 'E-commerce sites with 1M+ monthly visits,\nslow LCP/TTI scores, high-value product imagery'],
        ['data_variables_required', 'ARRAY[\'lcp\', \'tti\', \'aov\', \'monthly_visits\',\n\'company_website\', \'industry\']'],
        ['enrichment_sources', 'ARRAY[\'pagespeed\', \'storeleads\']'],
        ['clay_instructions', '1. Add PageSpeed enrichment for LCP/TTI\n2. Add StoreLeads for AOV\n3. Create selector: IF(lcp>2.5, approach_1, approach_2)\n4. Create 2 variant AI columns per email\n5. Use attached prompts for AI generation'],
        ['variant count', '2 variants per email (A/B testing)'],
    ]
    story.append(_make_table(example, col_widths=[130, 340]))

    # Build
    doc.build(story)
    print(f"Generated: {output_path}")
    return output_path


def _make_table(data, col_widths=None):
    if not col_widths:
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
