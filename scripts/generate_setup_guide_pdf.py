"""
Generate the Team Setup Guide PDF.
Run: python3 scripts/generate_setup_guide_pdf.py
Output: docs/gtm-cc-setup-guide.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, ListFlowable, ListItem
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
BG_STEP = HexColor('#f0f4ff')


def build():
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'gtm-cc-setup-guide.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.8*inch, rightMargin=0.8*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Title'],
        fontSize=24, textColor=DARK, spaceAfter=4, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
        fontSize=12, textColor=GRAY, alignment=TA_CENTER, spaceAfter=20)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
        fontSize=18, textColor=BLUE, spaceBefore=20, spaceAfter=10,
        borderWidth=0, borderPadding=0)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
        fontSize=14, textColor=DARK, spaceBefore=14, spaceAfter=8)
    body = ParagraphStyle('Body', parent=styles['Normal'],
        fontSize=10.5, textColor=DARK, spaceAfter=8, leading=15)
    body_bold = ParagraphStyle('BodyBold', parent=body,
        fontName='Helvetica-Bold')
    code_style = ParagraphStyle('Code', parent=styles['Normal'],
        fontSize=9, fontName='Courier', textColor=DARK, backColor=LIGHT_GRAY,
        spaceAfter=8, leading=12, leftIndent=12, rightIndent=12,
        borderWidth=0.5, borderColor=HexColor('#dddddd'), borderPadding=8)
    bullet_style = ParagraphStyle('Bullet', parent=body,
        leftIndent=24, bulletIndent=12, spaceAfter=4)
    step_title = ParagraphStyle('StepTitle', parent=styles['Heading2'],
        fontSize=14, textColor=WHITE, spaceBefore=0, spaceAfter=0)
    note_style = ParagraphStyle('Note', parent=body,
        fontSize=9.5, textColor=ACCENT, leftIndent=12, borderWidth=0)
    faq_q = ParagraphStyle('FaqQ', parent=body,
        fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=2)
    faq_a = ParagraphStyle('FaqA', parent=body,
        leftIndent=12, spaceAfter=6)

    story = []

    # ── Title ──
    story.append(Spacer(1, 40))
    story.append(Paragraph("GTM-CC Setup Guide", title_style))
    story.append(Paragraph("Get your team running in under 10 minutes", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE))
    story.append(Spacer(1, 20))

    # ── What is GTM-CC ──
    story.append(Paragraph("What is GTM-CC?", h1))
    story.append(Paragraph(
        "GTM-CC is a database-powered campaign system that connects to your Cursor/Claude Code editor. "
        "Instead of managing dozens of spreadsheets and Clay tables manually, you talk to Claude in plain English "
        "and it handles all the database queries, Clay pushes, and CSV exports for you.", body))
    story.append(Paragraph(
        "You don't need to know SQL or coding. Just open the project, pick your role, and use slash commands.", body))

    # ── What you need ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("What You Need", h1))

    needs_data = [
        ['What', 'Where to Get It', 'Time'],
        ['Cursor (code editor)', 'cursor.com — free download', '2 min'],
        ['GitHub account', 'github.com — free signup', '1 min'],
        ['.env file (database credentials)', 'Google Drive (link from Mayank)', '30 sec'],
    ]
    t = Table(needs_data, colWidths=[180, 220, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "That's it. No Node.js, no Python installs, no terminal commands beyond git clone.", note_style))

    story.append(PageBreak())

    # ── SETUP STEPS ──
    story.append(Paragraph("Setup Steps", h1))

    # Step 1
    story.append(_step_header("Step 1: Install Cursor"))
    story.append(Paragraph(
        "Go to <b>cursor.com</b> and download the installer for your computer (Mac or Windows).", body))
    story.append(Paragraph(
        "Install it like any other app. If you've used VS Code before, Cursor looks exactly the same.", body))
    story.append(Spacer(1, 6))

    # Step 2
    story.append(_step_header("Step 2: Clone the Repository"))
    story.append(Paragraph(
        "Open Cursor. Open the built-in terminal:", body))
    story.append(Paragraph(
        "<b>Mac:</b> press <font face='Courier'>Cmd + `</font> (backtick key, above Tab)", bullet_style))
    story.append(Paragraph(
        "<b>Windows:</b> press <font face='Courier'>Ctrl + `</font> (backtick key, above Tab)", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Then paste this command and hit Enter:", body))
    story.append(Paragraph(
        "git clone https://github.com/cleverviral-mayank/GTM-CC.git", code_style))
    story.append(Paragraph(
        "This downloads the project to your computer.", body))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Now open the folder in Cursor:", body))
    story.append(Paragraph(
        "<b>File → Open Folder →</b> find and select the <font face='Courier'>GTM-CC</font> folder you just downloaded.", body))
    story.append(Spacer(1, 6))

    # Step 3
    story.append(_step_header("Step 3: Download the .env File"))
    story.append(Paragraph(
        "Mayank will share a Google Drive link with a file called <font face='Courier'>.env</font>.", body))
    story.append(Paragraph(
        "<b>1.</b> Download the <font face='Courier'>.env</font> file from Google Drive", bullet_style))
    story.append(Paragraph(
        "<b>2.</b> Move/copy it into the <font face='Courier'>GTM-CC</font> folder on your computer "
        "(the same folder you opened in Step 2)", bullet_style))
    story.append(Paragraph(
        "<b>3.</b> That's it — Cursor will automatically find it", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The .env file contains the database connection. Without it, nothing works. "
        "Never share this file outside the team or post it anywhere.", note_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Note for Mac:</b> Files starting with a dot (like .env) are hidden by default in Finder. "
        "Press <font face='Courier'>Cmd + Shift + .</font> (period) in Finder to show hidden files. "
        "Or just drag the downloaded file into the GTM-CC folder in Cursor's sidebar.", body))
    story.append(Paragraph(
        "<b>Note for Windows:</b> In File Explorer, go to View → Show → Hidden items (check it). "
        "Then you'll see the .env file.", body))
    story.append(Spacer(1, 6))

    # Step 4
    story.append(_step_header("Step 4: Add the Claude Code Plugin in Cursor"))
    story.append(Paragraph(
        "You need to add the <b>Claude Code</b> plugin to Cursor. This is what lets you talk to Claude inside Cursor.", body))
    story.append(Paragraph(
        "<b>1.</b> Open Cursor's Extensions panel: click the Extensions icon in the left sidebar "
        "(or press <font face='Courier'>Cmd+Shift+X</font> on Mac / <font face='Courier'>Ctrl+Shift+X</font> on Windows)", bullet_style))
    story.append(Paragraph(
        "<b>2.</b> Search for <b>\"Claude Code\"</b> and install the plugin", bullet_style))
    story.append(Paragraph(
        "<b>3.</b> Once installed, Mayank will help you log into the shared Claude account "
        "(this is a one-time setup)", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "After the plugin is installed and logged in, open the Claude Code panel from the sidebar. "
        "Type <font face='Courier'>/whoami</font> and press Enter. Claude will ask you to pick your role:", body))

    role_data = [
        ['#', 'Role', 'What You Can Do'],
        ['1', 'Copy Strategist', 'Everything — create recipes, manage clients, full access'],
        ['2', 'Clay Operator', 'Pull leads, push to Clay, manage enrichment, export'],
        ['3', 'Campaign Operator', 'Check outputs, export CSV (read-only)'],
    ]
    rt = Table(role_data, colWidths=[25, 120, 315])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(rt)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Type your role number. Claude will show you your available commands.", body))

    story.append(PageBreak())

    # Step 5
    story.append(_step_header("Step 5: You're Ready — Use Slash Commands"))
    story.append(Paragraph(
        "That's the entire setup. Now just use slash commands to do your work:", body))
    story.append(Spacer(1, 6))

    # Commands by role
    story.append(Paragraph("Clay Operator Commands", h2))
    clay_cmds = [
        ['Command', 'What It Does'],
        ['/pull-leads', 'Pull leads for a client + segment (guided flow)'],
        ['/push-to-clay', 'Push leads to a Clay table via webhook'],
        ['/generate-http-query', 'Generate the HTTP body for Clay push-back columns'],
        ['/check-outputs', 'View email output stats'],
        ['/export-csv', 'Export leads + emails as CSV'],
    ]
    story.append(_make_cmd_table(clay_cmds))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Campaign Operator Commands", h2))
    campaign_cmds = [
        ['Command', 'What It Does'],
        ['/check-outputs', 'View email output stats for a client + segment'],
        ['/export-csv', 'Export leads + emails as CSV for sequencer upload'],
    ]
    story.append(_make_cmd_table(campaign_cmds))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Campaign Operator is fully read-only. You cannot accidentally modify any data.", note_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Copy Strategist Commands (all of the above, plus:)", h2))
    strat_cmds = [
        ['Command', 'What It Does'],
        ['/create-recipe', 'Create a new email recipe (guided flow)'],
        ['/test-recipe', 'Test a recipe on sample leads'],
    ]
    story.append(_make_cmd_table(strat_cmds))
    story.append(Paragraph(
        "The Copy Strategist can also run custom database queries in plain English.", body))

    story.append(PageBreak())

    # ── Day-to-Day Usage ──
    story.append(Paragraph("Day-to-Day Usage", h1))
    story.append(Paragraph(
        "You don't need to memorize commands. Just describe what you want in plain English. "
        "Claude will guide you step-by-step.", body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Example conversations:", h2))

    examples = [
        ("Clay Operator", [
            '"Pull leads for SpeedSize, the 1M+ segment"',
            '"Push these leads to Clay" → paste webhook URL when asked',
            '"Generate the HTTP query for enrichment push-back — I need CDN Detected and LCP P75"',
            '"Export verified leads as CSV"',
        ]),
        ("Campaign Operator", [
            '"Export a batch for SpeedSize 1M+ segment"',
            '"Check email outputs for SpeedSize"',
            '"Search for john@example.com in the outputs"',
        ]),
        ("Copy Strategist", [
            '"Create a new recipe for SpeedSize 1M+ segment"',
            '"Show me all active clients and their segments"',
            '"How many leads have email outputs for SpeedSize?"',
        ]),
    ]

    for role, convos in examples:
        story.append(Paragraph(f"<b>{role}:</b>", body_bold))
        for convo in convos:
            story.append(Paragraph(f"→ {convo}", bullet_style))
        story.append(Spacer(1, 4))

    # ── Keeping Updated ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("Keeping Updated", h1))
    story.append(Paragraph(
        "When the system gets updated (new commands, schema changes), you need to sync:", body))
    story.append(Paragraph(
        "Open the terminal in Cursor and run:", body))
    story.append(Paragraph("git pull", code_style))
    story.append(Paragraph(
        "That's it. Your commands and rules will be updated automatically. "
        "The .env file is never overwritten by git pull — your credentials stay safe.", body))

    # ── FAQ ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("FAQ", h1))

    faqs = [
        ("Do I need to know SQL or coding?",
         "No. Claude handles all database queries. You just describe what you want in plain English."),
        ("Can I accidentally break the database?",
         "No. Destructive operations (DELETE, DROP) are blocked for all roles. "
         "Campaign Operator is completely read-only. Clay Operator can only update lead enrichment fields. "
         "Claude always asks for confirmation before any write operation."),
        ("Where do exported CSVs go?",
         "In the exports/ folder inside the project. You can see it in Cursor's file sidebar on the left."),
        ("What if I get an error?",
         "Screenshot it and send to the Copy Strategist. Don't try to fix database issues yourself."),
        ("The .env file is missing / I can't see it",
         "Files starting with a dot are hidden by default. Mac: Cmd+Shift+. in Finder. "
         "Windows: View → Show → Hidden items. Or just look in Cursor's sidebar — it shows all files."),
        ("I synced from GitHub and my changes disappeared",
         "Run 'git pull' in the terminal. If you had local changes, ask the Copy Strategist for help."),
        ("Can I use this from multiple computers?",
         "Yes. Clone the repo and download the .env file on each computer. They share the same database."),
    ]

    for q, a in faqs:
        story.append(Paragraph(f"Q: {q}", faq_q))
        story.append(Paragraph(a, faq_a))

    # ── Troubleshooting ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("Troubleshooting", h1))

    trouble = [
        ['"Database error" or "connection refused"',
         'Your .env file is missing or has the wrong connection string. '
         'Re-download it from Google Drive.'],
        ['"BLOCKED: DELETE statements not allowed"',
         'Safety rules prevented a dangerous operation. This is working as intended.'],
        ['Claude doesn\'t know my role',
         'Type /whoami at the start of each new conversation to set your role.'],
        ['Commands not showing up',
         'Run "git pull" in the terminal to sync the latest commands.'],
    ]

    trouble_data = [['Problem', 'Fix']] + trouble
    tt = Table(trouble_data, colWidths=[200, 260])
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tt)

    # Build
    doc.build(story)
    print(f"Generated: {output_path}")
    return output_path


def _step_header(text):
    """Create a styled step header with blue background."""
    data = [[Paragraph(f"<b>{text}</b>",
             ParagraphStyle('StepH', fontName='Helvetica-Bold',
                            fontSize=13, textColor=WHITE, leading=18))]]
    t = Table(data, colWidths=[460])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t


def _make_cmd_table(data):
    """Create a command reference table."""
    t = Table(data, colWidths=[150, 310])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


if __name__ == '__main__':
    build()
