# Approach 2: Insider Remark

## STRATEGY

Position as someone who tracks the restaurant industry closely. Use a specific, publicly verifiable achievement or initiative by the prospect's restaurant (new location, menu launch, catering expansion, award, press mention) to open a peer-level conversation about the digital ordering opportunity that achievement creates. The insider remark signals "I follow your world" — not "I am selling you something."

## CORE PRINCIPLES
- The observable must be specific and verifiable — not "you are growing" but "saw your second location in Midtown"
- Insider remark reacts to THEIR achievement positively (not problem-pointing)
- Hook question connects logically to the observable
- Value bridge explains Owner.com in plain language
- This approach only works when research returns a strong finding

## VERBATAGE
Approved language and tone markers for copywriter:
- "noticed" / "saw" / "loved" (opener verbs)
- "that [X] though" / "[X] hits different" / "smart move" (insider remark patterns)
- "direct ordering" / "own the relationship" / "zero-commission"
- "regulars" (not "customers" or "consumers")
- "your spot" / "your place" (casual restaurant reference)
- Cuisine-specific: match their food category naturally
- "month-to-month" / "no lock-in"

## VARIABLES REQUIRED

### Always Needed
- [first_name] - prospect first name
- [company] - restaurant name
- [job_title] - prospect role
- [cuisine_type] - restaurant cuisine category
- [case_study_name] - cuisine-matched case study restaurant name (Pre-calculated: lookup)
- [case_study_result] - cuisine-matched case study headline result (Pre-calculated: lookup)

### Conditional
- [delivery_platform] - which third-party delivery app(s) they are listed on

## RESEARCH REQUIRED

Flag: YES

### Boolean Query Strategy

Core Question: What recent public signals show this restaurant is growing or investing in their business?

Need Trigger: Growth (new locations, menus, catering, awards) creates the need for better digital ordering infrastructure.

#### Boolean Queries
1. "[company] new location OR opening OR expansion 2025 2026"
2. "[company] menu launch OR new menu OR seasonal 2025 2026"
3. "[company] catering OR events OR pop-up OR award OR best of"
4. "site:[company_website] about OR story OR news"

#### Research Structure
1. Company Products/Services (always — from website scrape): what food, locations, current ordering setup
2. Key Finding: specific initiative, expansion, or achievement — factual and verifiable
3. Context: why this matters for their business and connects to digital infrastructure need
4. Insider Remark Material: what a peer would react to — facts, not phrasing
5. Supporting Evidence: additional relevant details

#### What Researcher Should Look For
- New location or expansion (need for scalable ordering)
- Menu innovation or seasonal launch (active investment)
- Awards or press recognition (pride point to reference)

## PATTERN

### Email 1 Structure (3 Paragraphs)

Paragraph 1 (Opener — Three-Part Connected Thought):
[first_name], [noticed/saw/loved] [their_observable] ([insider_remark]). How're you [action_verb] [challenge_created_by_observable]?
[blank line]

Paragraph 2 (Value Bridge):
GOAL: Connect the challenge from the hook question to what Owner.com does. The reader should understand how direct ordering and a branded app solve the problem the observable created.
SIGNAL: Pull from {{valueprop}} — pick the benefit most relevant to their growth signal (if expanding locations, emphasize scalable ordering; if launching new menu, emphasize marketing automation). Use cuisine-matched social proof.
CONSTRAINT: Explain what Owner.com does in plain language. One proof point, matched to cuisine type.
[blank line]

Paragraph 3 (CTA):
GOAL: Low-friction ask that references the specific initiative from paragraph 1.
SIGNAL: Tie back to their observable or growth signal.
CONSTRAINT: CTA starts with "Worth" — non-negotiable.

### MODE B Fallback (When Research is Inconclusive)

If research returns no specific observable, adapt Paragraph 1:
[first_name], running an independent [cuisine_type] spot right now is a different game than it was two years ago (the delivery app squeeze is real). How're you thinking about keeping more of each order?

This uses {LeadListContext} and {cuisine_type} to construct a relevant opener about the general industry challenge instead of a company-specific achievement.

### Observable Construction
- Must be specific: "opened a second location in Midtown" not "you are growing"
- Must be verifiable from research
- Must create a logical connection to needing digital infrastructure

### Insider Remark Construction
- 3-6 words, positive tone
- React to THEIR achievement
- "that second spot though" / "smart expansion" / "love the new menu"

### Hook Question Construction
- Flows from the observable
- Asks about the challenge or opportunity the observable creates
- Not generic — specific to their situation

## EMAIL 2 MODE

Mode: 3 Specific Ideas

The follow-up email gives three concrete ways Owner.com applies to THIS restaurant:
- Brief 1-sentence callback to Email 1
- 3 specific applications drawn from {{valueprop}} capabilities + research findings (e.g., "branded app for your regulars at the new location", "automated texts when you launch seasonal specials", "zero-commission delivery so expansion margins stay healthy")
- Each idea specific to their restaurant context
- 60-80 words
- Research Required is always YES when this mode is selected

## LOGIC FLOW

1. Researcher scrapes website and runs Boolean queries
2. If strong observable found: MODE A — full three-part opener
3. If research inconclusive: MODE B — industry-level opener using LeadListContext
4. Value bridge connects observable to Owner.com mechanism
5. CTA references their specific situation
6. Email 2 gives 3 specific ideas using research + valueprop

## OUTPUT EXAMPLES

### Example 1: Pizza Restaurant Expanding, Owner

[first_name], saw [company] just opened a second location on Main Street (that expansion though). How're you handling online ordering across both spots without doubling your delivery app fees?
[blank line]
Owner.com gives each location its own direct ordering and a shared branded app your regulars already know. Metro Pizza added $112K in sales and saved $29K in fees after ditching third-party apps.
[blank line]
Worth exploring how this works across your two locations?

### Example 2: Mexican Restaurant with New Menu, Owner

[first_name], loved [company]'s new brunch menu launch (smart pivot). How're you getting the word out to your existing customer base without blasting social and hoping?
[blank line]
Owner.com runs automated email and text campaigns to your actual customers when you launch something new — no manual work. Talkin Tacos drives $120K a month in direct orders through their branded app and automated marketing.
[blank line]
Worth seeing how this works for [company]'s brunch rollout?

### Example 3: Asian Restaurant with Press Feature, Owner

[first_name], noticed [company] made the city's best ramen list this year (well deserved). How're you converting that buzz into repeat direct orders instead of one-time DoorDash pickups?
[blank line]
Owner.com builds you a branded app with loyalty rewards so the press-driven traffic becomes regulars who order direct. Aburaya Fried Chicken saved $100K in delivery fees and added $25K a month going direct.
[blank line]
Worth a quick look at capturing that momentum for [company]?

## CRITICAL CONSTRAINTS
- Never fabricate an observable — if research fails, use MODE B
- Insider remark must be positive (not problem-pointing)
- Start with [first_name], — no "Hey" or "Hi"
- CTA starts with "Worth"
- No exclamation marks
- Social proof matched to cuisine type when possible
- [blank line] markers between all paragraphs
