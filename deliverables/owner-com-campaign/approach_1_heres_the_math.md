# Approach 1: Here's the Math

## STRATEGY

Show restaurant owners exactly how much money they are losing to third-party delivery commissions using their own publicly observable data. The math makes it personal — this is not a generic pitch about saving money, it is a specific calculation based on THEIR delivery presence and estimated order volume. The credibility comes from using data they can verify.

## CORE PRINCIPLES
- Lead with their numbers, not ours
- Commission savings is the hook — it is money they are already spending
- Explain what Owner.com does in plain language (not just metrics)
- Acknowledge estimates with "roughly", "about", "likely"
- Use percentage ranges, never absolute promises
- Social proof matched to their cuisine type

## VERBATAGE
Approved language and tone markers for copywriter:
- "ran some numbers" / "looked at your delivery setup"
- "you are probably paying" / "that is roughly"
- "keep that instead" / "that money stays with you"
- "zero-commission" (not "no commission" or "commission-free")
- "direct ordering" (not "first-party ordering")
- "own your customer data" / "own the relationship"
- "month-to-month" (emphasize no lock-in)
- Cuisine-specific language: match the prospect's food category naturally

## VARIABLES REQUIRED

### Always Needed
- [first_name] - prospect first name
- [company] - restaurant name
- [job_title] - prospect role

### Conditional
- [delivery_platform] - which third-party delivery app(s) they are listed on (DoorDash, UberEats, Grubhub)
- [review_count_formatted] - total review count across delivery platforms, formatted K/M
- [estimated_monthly_delivery_orders_formatted] - estimated monthly delivery orders, formatted K/M (Pre-calculated: review count proxy formula)
- [estimated_monthly_commission_formatted] - estimated monthly commission paid to third-party platforms, formatted K/M (Pre-calculated: orders x average order value x commission rate)
- [cuisine_type] - restaurant cuisine category
- [case_study_name] - cuisine-matched case study restaurant name (Pre-calculated: lookup from cuisine_type)
- [case_study_result] - cuisine-matched case study result (Pre-calculated: lookup from cuisine_type)

## RESEARCH REQUIRED

Flag: NO

This approach is entirely data-driven using pre-enriched Clay variables. No Boolean query research needed. The math is built from publicly available delivery platform data and industry benchmarks.

## PATTERN

### Email 1 Structure (3 Paragraphs)

Paragraph 1 (The Math Opener):
[first_name], I looked at [company]'s [delivery_platform] presence. Based on your review volume, you are likely doing around [estimated_monthly_delivery_orders_formatted] delivery orders a month — which means roughly [estimated_monthly_commission_formatted] going to [delivery_platform] in commissions.
[blank line]

Paragraph 2 (The Mechanism):
GOAL: Explain what Owner.com actually does and how it eliminates that commission loss. The reader should understand the product mechanism, not just the savings claim.
SIGNAL: Pull from {{valueprop}} — zero-commission delivery, direct ordering, branded app. Pick the 1-2 features most relevant to a restaurant doing heavy delivery volume. Use cuisine-matched social proof from the Social Proof Library.
CONSTRAINT: Explain in plain language. No jargon. Include one social proof reference matched to their cuisine type. Format as P.S. if it fits naturally.
[blank line]

Paragraph 3 (CTA):
GOAL: Low-friction ask that references the specific savings opportunity.
SIGNAL: Tie back to the commission number from paragraph 1.
CONSTRAINT: CTA starts with "Worth" — non-negotiable.

## EMAIL 2 MODE

Mode: Expand/Reframe

The follow-up email takes a different angle on the same value proposition:
- Shift from commission savings to customer data ownership or repeat ordering
- Pick a different benefit from {{valueprop}} (branded app, loyalty program, automated marketing)
- Use a different case study than Email 1
- 40-60 words
- Lighter, more casual CTA than Email 1
- Does NOT repeat the math from Email 1

## LOGIC FLOW

1. Check if [delivery_platform] and [estimated_monthly_commission_formatted] are populated
2. If populated: full math narrative with dollar savings
3. If commission data missing but delivery platform known: use percentage framing ("30-40 percent of every order")
4. If no delivery data at all: copywriter adapts using general commission pain from {{valueprop}}
5. Select cuisine-matched case study for social proof
6. CTA references the savings opportunity

## OUTPUT EXAMPLES

### Example 1: Pizza Restaurant, Owner

[first_name], I looked at [company]'s DoorDash presence. Based on your review volume, you are likely doing around 1.2K delivery orders a month — which means roughly $8K going to DoorDash in commissions.
[blank line]
Owner.com replaces that with zero-commission delivery and a branded app your regulars actually use. Township Line Pizza kept an extra $60K last year just by moving orders direct.
[blank line]
Worth a quick look at what that math looks like for [company]?

### Example 2: Mexican Restaurant, Owner

[first_name], I looked at [company]'s UberEats and DoorDash listings. You are probably doing around 800 delivery orders a month — that is roughly $5.6K in commissions every month that could stay with you.
[blank line]
Owner.com gives you direct online ordering, a branded app with loyalty rewards, and zero-commission delivery. Talkin Tacos went from $4K to $120K a month in direct sales after switching.
[blank line]
Worth exploring what [company] could keep?

### Example 3: Asian Restaurant, Owner

[first_name], looked at [company]'s delivery setup. Your Grubhub review volume suggests around 600 monthly delivery orders — roughly $4.2K a month in commissions.
[blank line]
Owner.com moves those orders to your own branded platform at zero commission. Aburaya Fried Chicken saved over $100K in delivery fees and added $25K a month in direct online sales.
[blank line]
Worth seeing the math for [company]?

## CRITICAL CONSTRAINTS
- Never fabricate order volume or commission numbers — if data unavailable, use percentage ranges
- Always spell out "percent" — never use the percent symbol
- Format numbers as K/M (8K not 8000, 1.2K not 1200)
- Use em dash for ranges (30–40 percent)
- No exclamation marks
- Start with [first_name], — no "Hey" or "Hi"
- CTA starts with "Worth"
- Social proof must match cuisine type when possible
