# Waterfall Simulation — Owner.com Campaign

Testing the full pipeline with two sample leads: one hitting the Math approach (data-rich path) and one hitting Insider Remark (research-dependent path).

---

## LEAD 1: Marco at Sal's Coal Fired Pizza (Math Path)

### Lead Data
```
firstName: Marco
company: Sal's Coal Fired Pizza
jobTitle: Owner
cuisine_type: Pizza
companyWebsite: salscoalfired.com
delivery_platform: DoorDash
review_count: 2400
```

### STEP 1: Approach Selector (Priority Cascade Formula)

Data checks:
- approach_1_eligible (Math): delivery_platform = "DoorDash" (not empty) AND review_count = 2400 (> 50) → TRUE
- approach_2_eligible (Insider Remark): TRUE (always at selector stage)
- approach_3_eligible (Customer Empathy): TRUE (always)

Cascade: approach_1 = TRUE → selected.

Output: {{SelectedApproach}} = approach_1_heres_the_math.md

### STEP 2: Research Required (Formula)

Reads SelectedApproach → "Flag: NO"
Email 2 Mode = "Expand/Reframe" (not "3 Ideas")

Output: NO

Researcher does NOT run. Skip to Copywriter.

### STEP 3: Calculated Variables (Clay Formulas)

```
estimated_monthly_delivery_orders = 2400 x 0.15 = 360
estimated_monthly_commission = 360 x 28 x 0.30 = $3,024
estimated_monthly_delivery_orders_formatted = "360"
estimated_monthly_commission_formatted = "$3K"
case_study_name = "Metro Pizza" (cuisine_type contains "pizza")
case_study_result = "+$112K sales, 11K app installs"
```

### STEP 4: Copywriter Agent (Use AI)

Inputs:
- {{SelectedApproach}} = Here's the Math approach
- {{valueprop}} = Owner.com value prop
- {{LeadListContext}} = "Independent restaurants on delivery apps, paying 30-40 percent commissions"
- {{researchReport}} = empty (research did not run)
- {{firstName}} = Marco
- {{company}} = Sal's Coal Fired Pizza
- All calculated variables above

Mode: MODE B (no research) — but Company Products/Services section also empty since researcher did not run for Math approach

Data Handling: All conditional variables populated. No missing data adaptation needed.

#### Email 1 Output:

```
---EMAIL 1---
Marco, I looked at Sal's Coal Fired Pizza's DoorDash presence. Based on your review volume, you are likely doing around 360 delivery orders a month — which means roughly $3K going to DoorDash in commissions.
[blank line]
Owner.com replaces that with zero-commission delivery and a branded app your regulars actually use. Metro Pizza kept an extra $112K and got 11K app installs after moving orders direct.
[blank line]
Worth a quick look at what that math looks like for Sal's?
---END EMAIL 1---
```

Word count: ~71 words. PASS.

#### Email 2 Output:

Email 2 Mode: Expand/Reframe
- Different angle: shift from commission savings to customer data ownership and loyalty
- Different case study

```
---EMAIL 2---
Marco, one more thought on this.
[blank line]
Every order through DoorDash means DoorDash owns that customer — not you. Owner.com gives you a Starbucks-style loyalty app so your regulars order direct and come back on their own. Township Line Pizza added $300K in yearly direct sales after switching.
[blank line]
Worth a look?
---END EMAIL 2---
```

Word count: ~53 words. Within 40-60 range. PASS.

### STEP 5: Spam Word Checker (Formula)

Scans Email 1 against ~100-word spam list.

Assume flagged: "free" — NOT FOUND. "guarantee" — NOT FOUND. "exclusive" — NOT FOUND.
No common spam words detected in this email.

Output: {{flaggedWords}} = "" (empty)

### STEP 6: Style, Tone & Spam Checker (Use AI)

Inputs:
- {{email1Draft}} = Email 1 from copywriter
- {{flaggedWords}} = "" (empty — no spam words found)
- {{valueprop}} = Owner.com value prop
- {{SelectedApproach}} = Here's the Math approach (includes Verbatage section)

#### Job 1 (Spam words): No flagged words. Skip.

#### Job 2 (Humanize):
Check for AI patterns. "Based on your review volume, you are likely doing around 360" — slightly formal. Tweak: "Your review volume suggests about 360" → more natural.
"which means roughly $3K going to DoorDash in commissions" — good, "roughly" adds uncertainty.

#### Job 3 (Casual tone):
"replaces that with zero-commission delivery" — clean and direct. PASS.
"your regulars actually use" — conversational. PASS.

#### Job 4 (Break linear flow):
Flow check: data observation → problem (commission) → solution (Owner.com) → proof → CTA. Somewhat linear but acceptable for a math-heavy email. The proof is integrated into the solution paragraph, not a separate step. PASS.

#### Output: {{email1Final}}

```
Marco, I looked at Sal's Coal Fired Pizza on DoorDash. Your review volume suggests about 360 delivery orders a month — roughly $3K going to DoorDash in commissions.
[blank line]
Owner.com replaces that with zero-commission delivery and a branded app your regulars actually use. Metro Pizza kept an extra $112K and got 11K app installs after moving orders direct.
[blank line]
Worth a quick look at what that math looks like for Sal's?
```

Changes: "Based on your review volume, you are likely doing around" → "Your review volume suggests about" (less formal, more natural). Removed "presence" from first sentence (cleaner).

### STEP 7: Subject Line Picker (Formula)

Templates from approach: 1. "Delivery Fees" 2. "[cuisine_type] Orders"
Formula randomly selects template #1.

Output: {{subjectLine}} = "Delivery Fees"

Validation:
- 2 words. PASS.
- Title Case. PASS.
- No punctuation. PASS.
- No first name token. PASS.
- Passes Colleague Test — sounds like an internal topic. PASS.
- Zero cost. PASS.

### LEAD 1 FINAL OUTPUTS

| Output | Value |
|---|---|
| Approach Used | Here's the Math (priority cascade: delivery data available) |
| Email 1 | Style-checked, ~68 words |
| Email 2 | Expand/Reframe, ~53 words |
| Subject Line | "Delivery Fees" |

---

## LEAD 2: Sofia at Casa de Sabor (Insider Remark Path)

### Lead Data
```
firstName: Sofia
company: Casa de Sabor
jobTitle: Owner
cuisine_type: Mexican
companyWebsite: casadesabor.com
delivery_platform: (empty — not enriched)
review_count: (empty)
```

### STEP 1: Approach Selector (Priority Cascade Formula)

Data checks:
- approach_1_eligible (Math): delivery_platform = EMPTY → FALSE
- approach_2_eligible (Insider Remark): TRUE
- approach_3_eligible (Customer Empathy): TRUE

Cascade: approach_1 fails → approach_2 = TRUE → selected.

Output: {{SelectedApproach}} = approach_2_insider_remark.md

### STEP 2: Research Required (Formula)

Reads SelectedApproach → "Flag: YES"
Email 2 Mode = "3 Specific Ideas" → confirms YES

Output: YES

Researcher Agent runs.

### STEP 3: Researcher Agent (Claygent Simulation)

#### STEP 0: Website Scrape (always runs)

Visits casadesabor.com. Finds:
- Mexican restaurant specializing in Oaxacan cuisine
- Menu includes mole negro, tlayudas, mezcal cocktails
- Single location in Austin, TX
- Currently uses Toast POS
- No branded app visible
- Online ordering through Toast website widget

#### STEP 1: Query Substitution

From approach Boolean queries:
1. "Casa de Sabor new location OR opening OR expansion 2025 2026"
2. "Casa de Sabor menu launch OR new menu OR seasonal 2025 2026"
3. "Casa de Sabor catering OR events OR pop-up OR award OR best of"
4. "site:casadesabor.com about OR story OR news"

#### STEP 2: Web Searches (4-6 searches)

Simulated findings:
- Search 1: Found — Casa de Sabor was featured in Austin Monthly's "Best New Restaurants 2025" list
- Search 2: Found — they launched a weekend brunch menu with Oaxacan-inspired brunch items in Q4 2025
- Search 3: Found — they are now catering corporate events through their website
- Search 4: About page confirms single location, owner-operated, opened 2024

#### STEP 3: Research Report

Output: {{researchReport}}

```
## Research Report: Casa de Sabor

### Company Products/Services
Casa de Sabor is a Oaxacan Mexican restaurant in Austin, TX. Menu features mole negro, tlayudas, mezcal cocktails, and house-made tortillas. Single location, owner-operated. Uses Toast POS for online ordering through their website. No branded mobile app. Targets Austin food enthusiasts interested in regional Mexican cuisine.
Source: casadesabor.com

### Key Finding
Casa de Sabor was named to Austin Monthly's "Best New Restaurants 2025" list and launched a weekend brunch menu with Oaxacan-inspired items (chilaquiles with mole, horchata French toast) in Q4 2025.
Source: austinmonthly.com, casadesabor.com/brunch

### Context
Press recognition and a brunch launch signal a restaurant investing in growth and expanding its customer base. The brunch menu targets a new daypart and audience. This creates a need for marketing infrastructure to reach new customers and bring them back — especially the press-driven traffic that may only visit once.

### Insider Remark Material
Named "Best New Restaurants 2025" in a competitive Austin market. Brunch launch with Oaxacan twist is distinctive — not just standard brunch fare. Owner-operated single location making smart moves to grow. The mole-topped chilaquiles and horchata French toast are specific, memorable menu items.

### Supporting Evidence
Now offering corporate catering through their website. Single location means every new customer channel (brunch, catering, direct ordering) matters more.

### Priority Evidence Found
- New location or expansion: NOT FOUND — single location
- Menu innovation or seasonal launch: FOUND — weekend brunch menu, Q4 2025
- Awards or press recognition: FOUND — Austin Monthly Best New Restaurants 2025
```

### STEP 4: Copywriter Agent (Use AI)

Inputs:
- {{SelectedApproach}} = Insider Remark approach
- {{valueprop}} = Owner.com value prop
- {{LeadListContext}} = "Independent restaurants on delivery apps"
- {{researchReport}} = report above
- {{firstName}} = Sofia
- {{company}} = Casa de Sabor
- {{cuisine_type}} = Mexican
- {{case_study_name}} = Talkin Tacos
- {{case_study_result}} = "$120K/mo direct sales, +$435K savings"

Mode: MODE A (research has usable findings)

Company Products/Services: Oaxacan Mexican, single location, Toast POS, no branded app.

Data Handling: delivery_platform is empty — copywriter will not reference a specific delivery app. Will adapt.

#### Email 1 Output:

```
---EMAIL 1---
Sofia, noticed Casa de Sabor made Austin Monthly's best new restaurants list (well deserved in that market). How're you turning that press buzz into repeat direct orders instead of one-time visitors?
[blank line]
Owner.com gives you a branded app with loyalty rewards and automated texts that bring people back — especially when you launch something new like that brunch menu. Talkin Tacos drives $120K a month in direct orders through their app.
[blank line]
Worth seeing how this works for Casa de Sabor?
---END EMAIL 1---
```

Word count: ~76 words. PASS.

Validation:
- Observable: "made Austin Monthly's best new restaurants list" — specific, verifiable
- Insider remark: "well deserved in that market" — positive, reacts to achievement, 5 words
- Hook: "turning that press buzz into repeat direct orders" — connects logically
- Value bridge: explains what Owner.com does (branded app, loyalty, automated texts)
- References brunch menu from research (Supporting Evidence)
- Social proof: Talkin Tacos — cuisine-matched (Mexican)
- CTA starts with "Worth"

#### Email 2 Output:

Email 2 Mode: 3 Specific Ideas
- 1-sentence callback to Email 1
- 3 specific applications using research + valueprop

```
---EMAIL 2---
Sofia, following up on the direct ordering idea.
[blank line]
Three ways this could work for Casa de Sabor specifically:
1. Automated texts to your brunch customers every Friday with the weekend specials
2. A loyalty app where regulars earn points toward your mezcal flights
3. Zero-commission delivery for your catering orders so margins stay healthy
[blank line]
Worth a quick call to walk through these?
---END EMAIL 2---
```

Word count: ~63 words. Within 60-80 range. PASS.

Validation:
- Callback to Email 1: "following up on the direct ordering idea" — brief, not repeating
- Idea 1: brunch + automated texts (from research finding + valueprop feature)
- Idea 2: loyalty app + mezcal flights (from Company Products/Services + valueprop feature)
- Idea 3: catering + zero-commission delivery (from Supporting Evidence + valueprop feature)
- Each idea specific to Casa de Sabor's context
- CTA casual

### STEP 5: Spam Word Checker (Formula)

Scans Email 1. No common spam words detected.
Output: {{flaggedWords}} = ""

### STEP 6: Style, Tone & Spam Checker (Use AI)

#### Job 1 (Spam words): None. Skip.

#### Job 2 (Humanize):
"Owner.com gives you a branded app with loyalty rewards and automated texts that bring people back" — slightly feature-listy. Tweak to flow more naturally.

#### Job 3 (Casual tone):
"especially when you launch something new like that brunch menu" — conversational, references their specific thing. PASS.

#### Job 4 (Break linear flow):
Press recognition → problem (one-time visitors) → solution (Owner.com) → proof → CTA. Standard flow but the brunch menu reference in paragraph 2 creates a callback that breaks pure linearity. Acceptable.

#### Output: {{email1Final}}

```
Sofia, noticed Casa de Sabor made Austin Monthly's best new restaurants list (well deserved in that market). How're you turning that press buzz into repeat direct orders instead of one-time visitors?
[blank line]
Owner.com sets you up with a branded app and loyalty rewards so those new faces become regulars — plus automated texts when you launch something new like that brunch menu. Talkin Tacos runs $120K a month in direct orders through their app.
[blank line]
Worth seeing how this works for Casa de Sabor?
```

Changes: "gives you a branded app with loyalty rewards and automated texts that bring people back" → "sets you up with a branded app and loyalty rewards so those new faces become regulars — plus automated texts when you launch something new" (more natural, less feature-listy, "those new faces become regulars" closes the thought loop with the press buzz opener).

### STEP 7: Subject Line Picker (Formula)

Templates: 1. "[cuisine_type] Ordering" 2. "Direct Orders"
Substitution: [cuisine_type] = "Mexican"
Formula randomly selects template #2.

Output: {{subjectLine}} = "Direct Orders"

Validation:
- 2 words. PASS.
- Title Case. PASS.
- No punctuation. PASS.
- Colleague Test. PASS.

### LEAD 2 FINAL OUTPUTS

| Output | Value |
|---|---|
| Approach Used | Insider Remark (cascade: Math failed — no delivery data) |
| Email 1 | Style-checked, ~76 words |
| Email 2 | 3 Specific Ideas, ~63 words |
| Subject Line | "Direct Orders" |

---

## BLINDSPOT CHECK

### Issues Identified During Simulation

1. REVIEW COUNT PROXY ACCURACY: The formula estimated_monthly_delivery_orders = review_count x 0.15 is rough. For Lead 1 with 2,400 reviews, it produces 360 monthly orders. This could be wildly off — some restaurants have thousands of old reviews but low current volume, and vice versa. The email uses "suggests about" language to hedge, but the underlying estimate may not be credible.
   - SEVERITY: HIGH
   - MITIGATION: Consider alternative proxies (active listing status, menu size on platform, response to reviews as freshness signal). Or simply use the percentage framing ("30-40 percent of every delivery order") without estimating volume.

2. MATH APPROACH SKIPS WEBSITE SCRAPE: When approach_1 (Math) is selected, Research Required = NO, so the Researcher does not run at all. This means the Company Products/Services section is never populated. The copywriter gets no product context about the prospect's restaurant.
   - SEVERITY: MEDIUM-HIGH
   - FIX: Either (a) always run the website scrape step as a separate Claygent column regardless of approach, or (b) change Math approach Research Required to YES but with a minimal research scope (website scrape only, no Boolean queries).

3. INSIDER REMARK MODE B vs CUSTOMER EMPATHY OVERLAP: When the cascade selects Insider Remark (approach 2) but research returns INCONCLUSIVE, the copywriter uses MODE B — which is basically an industry-level empathy opener. This is very similar to what Customer Empathy (approach 3) does. The lead might have been better served by just getting approach 3 in the first place.
   - SEVERITY: LOW
   - ACCEPT: This is a feature, not a bug. MODE B is a graceful degradation. The approaches are designed to cascade — if MODE B fires, it means the lead did not have enough data for Math or enough public info for Insider Remark. The output quality is still acceptable.

4. EMAIL 2 PARSING RISK: The copywriter outputs both emails using ---EMAIL 1--- / ---END EMAIL 1--- / ---EMAIL 2--- / ---END EMAIL 2--- delimiters. Clay needs to split these into separate columns using a formula. If the LLM slightly varies the delimiter format (extra space, missing dash), the formula breaks.
   - SEVERITY: MEDIUM
   - MITIGATION: Add a strict output format reminder at the end of the copywriter prompt. Consider using a more robust delimiter (e.g., triple equals or unique tokens). Test with 20+ rows to see if the LLM is consistent.

5. CASE STUDY CUISINE MATCHING IS BROAD: The case_study_name formula maps "pizza" → Metro Pizza and "Mexican" → Talkin Tacos. But what about "Mediterranean" mapping to "Karv Greek Kouzina" — that might feel off for a Lebanese restaurant. And the default fallback is "Doo-Dah Diner" which may not resonate with all non-categorized cuisines.
   - SEVERITY: LOW
   - MITIGATION: Expand the cuisine mapping formula with more categories, or add a "general" case study that works universally (e.g., one with pure percentage growth, no cuisine specificity).

6. STYLE CHECKER CHANGES ARE MINIMAL: In both leads, the style checker made very small tweaks — a word or two. This is expected for well-prompted copywriter output, but it raises the question: is the style checker adding enough value to justify the credit cost per row?
   - SEVERITY: LOW (observation, not a bug)
   - NOTE: The value of the style checker will become more apparent with weaker copywriter outputs or when spam words are actually flagged. The humanization and linear-flow-breaking jobs are subtle but cumulative.

---

## SIMULATION VERDICT

Both leads produced clean, natural-sounding emails through the full pipeline. The approach selector correctly routed each lead based on data availability. Key wins:

- Math approach: the commission calculation feels personal and specific
- Insider Remark approach: the press mention creates genuine peer credibility
- Email 2 modes work well: Expand/Reframe shifts the angle naturally, 3 Specific Ideas gives actionable follow-up
- Subject lines: 2-word Title Case passes the Colleague Test
- Style checker: subtle but useful tweaks to tone

The two high-priority blindspots to address: review count proxy accuracy (#1) and Math approach missing website scrape (#2).
