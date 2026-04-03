# Approach 3: Customer Empathy

## STRATEGY

Make the restaurant owner feel what their customers experience when ordering through third-party delivery apps — marked-up prices, cold food, no loyalty relationship, and zero connection to the restaurant brand. Then bridge to Owner.com as the way to give their customers the direct experience they deserve. This approach works because restaurant owners care deeply about their food and their regulars. Framing it through the diner's eyes creates emotional resonance that data alone cannot.

## CORE PRINCIPLES
- Start from the customer's perspective, not the restaurant's
- Make the owner FEEL the gap between what they want and what third-party apps deliver
- The product is the bridge from bad customer experience to good
- This approach requires no special data — works for any restaurant
- Social proof reinforces that other restaurant owners already made this shift

## VERBATAGE
Approved language and tone markers for copywriter:
- "your regulars" / "your people" (not "customers" or "consumers")
- "ordering direct" / "ordering from you" (not "first-party" or "direct-to-consumer")
- "cold food in a brown bag" / "someone else's app" / "marked-up menu"
- "own the relationship" / "keep the connection"
- "your brand, your app" (not "a branded application")
- "no lock-in" / "month-to-month"
- "Starbucks-style app" (when referencing the loyalty/rewards feature)

## VARIABLES REQUIRED

### Always Needed
- [first_name] - prospect first name
- [company] - restaurant name
- [job_title] - prospect role
- [cuisine_type] - restaurant cuisine category
- [case_study_name] - cuisine-matched case study restaurant name (Pre-calculated: lookup)
- [case_study_result] - cuisine-matched case study headline result (Pre-calculated: lookup)

### Conditional
- [delivery_platform] - which third-party delivery app(s) they are listed on (strengthens empathy if known)

## RESEARCH REQUIRED

Flag: NO

This approach is empathy-driven using universal restaurant pain points. No research needed — the customer experience gap with third-party delivery apps is consistent across all restaurants.

## PATTERN

### Email 1 Structure (3 Paragraphs)

Paragraph 1 (Customer Experience Opener):
GOAL: Paint a vivid, specific picture of what the restaurant owner's customers experience when they order through third-party apps. Make the owner feel the gap between their food quality and the delivery experience.
SIGNAL: Use {delivery_platform} if available to name the specific app. If not available, use "delivery apps" generically. Reference the universal pain points: marked-up prices, cold food, no brand connection, customer data owned by someone else.
CONSTRAINT: Keep it to 1-2 sentences. Specific and visual, not abstract. Start with [first_name], directly.
[blank line]

Paragraph 2 (The Bridge):
GOAL: Show how Owner.com closes the gap — giving their customers a direct ordering experience that matches the quality of their food. The owner should see Owner.com as the way to give regulars what they actually want.
SIGNAL: Pull from {{valueprop}} — branded app, loyalty rewards, zero-commission delivery, direct ordering. Pick the 1-2 features that most directly address the customer experience gap described in paragraph 1. Use cuisine-matched social proof.
CONSTRAINT: Explain what Owner.com does in plain language. Focus on the customer experience improvement, not just the restaurant's savings. One proof point matched to cuisine.
[blank line]

Paragraph 3 (CTA):
GOAL: Low-friction ask framed around the customer experience, not the sale.
SIGNAL: Reference their regulars or their food specifically.
CONSTRAINT: CTA starts with "Worth" — non-negotiable.

## EMAIL 2 MODE

Mode: Expand/Reframe

The follow-up shifts from customer experience to the business case:
- If Email 1 focused on the diner's experience, Email 2 focuses on the owner's financials (commission savings, data ownership)
- Pick a different benefit from {{valueprop}} — emphasize the business outcome
- Use a different case study than Email 1
- 40-60 words
- Lighter CTA
- Does NOT repeat the empathy angle from Email 1

## LOGIC FLOW

1. Check if [delivery_platform] is populated for specificity
2. If known: reference specific platform by name in empathy opener
3. If not known: use generic "delivery apps" language
4. Bridge to Owner.com features that fix the customer experience
5. Cuisine-matched social proof
6. CTA references their regulars or their food

## OUTPUT EXAMPLES

### Example 1: Pizza Restaurant, Owner

[first_name], right now someone ordering [company]'s pizza through DoorDash is paying a marked-up price, getting it 20 minutes later than they should, and [company] never even knows who they are.
[blank line]
Owner.com gives your regulars a direct way to order — your own branded app with loyalty rewards, zero-commission delivery, and you keep the customer relationship. Metro Pizza added $112K in direct sales after making the switch.
[blank line]
Worth seeing what this looks like for [company]?

### Example 2: Mexican Restaurant, Owner

[first_name], your regulars ordering [company]'s food through UberEats are paying extra, waiting longer, and building a relationship with UberEats instead of with you. That is a lot of loyalty leaving the building.
[blank line]
Owner.com flips that — direct ordering, a branded app your people actually download, and automated texts that bring them back. Samos Oaxaca grew 377 percent and saved $70K in fees after going direct.
[blank line]
Worth a quick look at how [company] could own that relationship?

### Example 3: Any Cuisine, Owner (No Delivery Platform Known)

[first_name], when someone orders [company]'s food through a delivery app, they are paying more, waiting longer, and never connecting with your brand. The food is yours but the customer is not.
[blank line]
Owner.com changes that with direct online ordering, a Starbucks-style loyalty app for your regulars, and zero-commission delivery. Karv Greek went from zero direct orders to $40K a month after switching.
[blank line]
Worth exploring what direct ordering looks like for [company]?

## CRITICAL CONSTRAINTS
- Never blame the restaurant owner for using delivery apps — empathize with the situation
- The pain is what CUSTOMERS experience, not what the RESTAURANT loses (save that for Email 2)
- Start with [first_name], — no "Hey" or "Hi"
- CTA starts with "Worth"
- No exclamation marks
- Social proof matched to cuisine type when possible
- [blank line] markers between all paragraphs
- This approach is the fallback — it works for any restaurant regardless of data availability
