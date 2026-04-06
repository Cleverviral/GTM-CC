# Approach 1: Customer Empathy Mirror

## STRATEGY

Put the prospect in their customer's shoes through physical scenarios. Show them what shoppers experience when media loads slowly. Position SpeedSize as closing the experience gap between what brands want to show and what customers actually see. The narrative works with or without performance metrics — data strengthens it but is not required.

## CORE PRINCIPLES
- Lead with the customer's experience, not the brand's problem
- Physical scenarios make abstract performance metrics tangible
- CrUX and PageSpeed data validate the scenario when available — they do not replace it
- CDN positioning is comparative, not combative (even with Cloudflare, not despite Cloudflare)
- GAP validation is the proof point — always use "Our client GAP"
- Use "stress-tested" (hyphenated) to save words
- Data references must be conversational: "Your Google real-time data shows" or "This is your site's media load time via PageSpeed Insights"
- Acknowledge the CDN they have, show SpeedSize works alongside it

## VERBATAGE
Approved language and tone markers for copywriter:
- "we know that when shoppers..." / "picture shoppers..."
- "even with [CDN]" (not "despite" or "regardless of")
- "premium visual experience" (core product language)
- "loading images and videos much faster without sacrificing quality"
- "stress-tested us against [CDN] over 200M+ requests"
- "sponsored Media Speed test" (not "free trial" or "demo")
- "no commitments" (not "no strings attached")
- "Our client GAP" (always include "Our client")
- "saw 6.5X faster loads" (use "saw" not "showing" or "achieving")
- Natural openers: "we know that when shoppers..." or "picture shoppers..."

## VARIABLES REQUIRED

### Always Needed
- [first_name] - prospect first name
- [company] - company name
- [job_title] - prospect role
- [company_website] - company domain
- [product_category] - what they sell (from website scrape)

### Conditional
- [crux_poor_pct] - percentage of visitors with poor media experience (use only if indicates poor experience)
- [lcp_score] - media load time in seconds (use only if above 2.5s)
- [current_cdn] - detected CDN provider name
- [monthly_visits_formatted] - monthly site traffic, formatted K/M

## RESEARCH REQUIRED

Flag: NO

This approach is data-driven using pre-enriched Clay variables and website scrape context. No web research needed. The website scrape agent provides product category context for scenario construction.

## PATTERN

### Email 1 Structure

Paragraph 1 (Customer Scenario Opener):
[first_name], [physical customer scenario relevant to their product category with consequence of slow media].
[blank line]

Paragraph 2 (Data Validation — if available):
GOAL: Validate the scenario with the prospect's own site performance data. Make it specific to their situation. If no unhealthy data is available, skip this paragraph entirely and let the scenario speak for itself.
SIGNAL: Use [crux_poor_pct] if available (preferred). Otherwise use [lcp_score]. Reference [current_cdn] to show the problem persists even with their current infrastructure.
CONSTRAINT: Conversational data integration only. "Your Google real-time data shows" or "This is your site's media load time via PageSpeed Insights." Never state raw metrics without context. Never use data if it shows healthy performance (below 2.5s threshold).
[blank line]

Paragraph 3 (SpeedSize Solution + GAP Proof):
GOAL: Explain what SpeedSize does and validate with GAP proof point in a connected flow.
SIGNAL: Pull from {{valueprop}} — "premium visual experience," "loading images and videos much faster without sacrificing quality." Always include GAP stress-test. Include [current_cdn] in comparison if available.
CONSTRAINT: Two sentences maximum. Always say "Our client GAP." Use "stress-tested" (hyphenated). Plain language, no jargon.
[blank line]

Paragraph 4 (CTA):
GOAL: Low-friction ask with no commitments.
SIGNAL: Reference [company] name in the ask.
CONSTRAINT: Must start with "Worth." One sentence.

## EMAIL 2 MODE

Mode: Expand/Reframe

Write a follow-up email that takes a different angle on the same value proposition.

Instructions:
- Does NOT repeat what Email 1 said — shift from customer experience to business impact (Core Web Vitals, SEO, conversion)
- Reference the AWS-sponsored PoC specifically — 14-day validation, no dev work
- Can mention integration simplicity (one-click plugin or subdomain setup)
- Use a different benefit from {{valueprop}} than Email 1 used
- 40-60 words
- Start with [first_name], — no "Hey" or "Hi"
- CTA should be lighter and more casual than Email 1
- Use [blank line] markers between paragraphs
- No exclamation marks
- Conversational, peer-to-peer tone

## LOGIC FLOW

1. Open with a physical scenario the prospect can feel (customer waiting, bouncing, leaving)
2. If data available: validate with their own performance metrics (makes it personal)
3. Bridge to SpeedSize as the solution + GAP proof (credibility)
4. Close with low-friction sponsored test offer

## OUTPUT EXAMPLES

### Example 1: Fashion E-commerce, CrUX Data + Cloudflare

Jennifer, we know that when shoppers browse your denim collection, slow-loading images make them bounce.

[blank line]

Your Google real-time data shows 28 percent of shoppers wait over 2.5 seconds for media, even with Cloudflare.

[blank line]

SpeedSize loads images and videos much faster without sacrificing quality. Our client GAP stress-tested us against Cloudflare over 200M+ requests and saw 6.5X faster loads.

[blank line]

Worth a sponsored Media Speed test for Demule?

### Example 2: Outdoor Equipment, PSI LCP + Akamai

David, picture mobile shoppers waiting 3.4 seconds for your hero image to appear. They will most definitely bounce.

[blank line]

This is your site's media load time via PageSpeed Insights, even with your current Akamai CDN.

[blank line]

SpeedSize loads images and videos much faster without sacrificing quality. Our client GAP stress-tested us against Akamai over 200M+ requests and saw 6.5X faster loads.

[blank line]

Worth a sponsored Media Speed test for Topgear?

### Example 3: Furniture Retail, No Unhealthy Data

Sarah, imagine clicking through a living room collection and watching product images slowly materialize. That is frustrating even with a CDN in place.

[blank line]

SpeedSize ensures a premium visual experience by loading images and videos much faster without sacrificing quality. Our client GAP stress-tested SpeedSize over 200M+ requests and saw 6.5X faster loads.

[blank line]

Worth a sponsored Media Speed test for HomeStyle?

## CRITICAL CONSTRAINTS
- Never say "we will replace your CDN"
- Never fabricate metrics or data
- Only use LCP if above 2.5s (skip if at or below 2.5s)
- Only use CrUX if P75 above 2.5s (skip if at or below 2.5s)
- Prefer CrUX over PSI when both show unhealthy scores
- Target 75 words or under
- No question marks in body (only CTA)
- CTA starts with "Worth"
- Always say "Our client GAP"
- Always include [blank line] markers between paragraphs
- Complete sentences only
- No percent symbols, currency signs, exclamation marks, em dashes
- Plain language (8th grade readability)
- Start directly with [first_name], no "Hey" or "Hi"
- No line break between name and opener sentence
