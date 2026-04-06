# Approach 2: Ultra-Direct Recent Proof

## STRATEGY

State the problem directly without storytelling. Lead with investigation when performance data is available. Position against their current CDN immediately to show you understand their setup. Focus on mechanical explanation of what SpeedSize does differently, backed by GAP validation. This is the universal fallback approach — it works for any lead regardless of available data.

## CORE PRINCIPLES
- Investigation narrative when data available: "I ran your site on..."
- Direct problem statement when no data: state the media performance challenge plainly
- No storytelling, no scenarios, no analogies
- CDN positioning is immediate and specific
- GAP proof point is the closer
- Shorter and more direct than other approaches
- This approach always works — no special data requirements

## VERBATAGE
Approved language and tone markers for copywriter:
- "I ran your site on Google's real-time monitoring tool" (for CrUX)
- "I ran your site on PageSpeed Insights" (for PSI)
- "Seems like your media loads at [X] seconds for your shoppers" (PSI framing)
- "[X] percent of visitors experienced media loading after 2.5 seconds" (CrUX framing)
- "even with your current [CDN] CDN"
- "premium visual experience" (core product language)
- "loading images and videos much faster without sacrificing quality"
- "Our client GAP stress-tested us" (always include)
- "sponsored Media Speed test" / "no commitments"

## VARIABLES REQUIRED

### Always Needed
- [first_name] - prospect first name
- [company] - company name
- [job_title] - prospect role
- [company_website] - company domain

### Conditional
- [crux_poor_pct] - percentage of visitors with poor media experience (use only if indicates poor experience)
- [lcp_score] - media load time in seconds (use only if above 2.5s)
- [current_cdn] - detected CDN provider name
- [product_category] - what they sell (from website scrape)

## RESEARCH REQUIRED

Flag: NO

This approach is entirely data-driven or works as a universal fallback. No web research needed. When performance data is available, the investigation narrative carries the email. When no data is available, a direct problem statement works on its own.

## PATTERN

### Email 1 Structure

Paragraph 1 (Investigation or Direct Statement):
GOAL: Establish context immediately. When performance data is available, lead with "I ran your site" investigation narrative. When no data is available, state the media performance problem directly and plainly.
SIGNAL: Use [crux_poor_pct] if available (preferred), otherwise [lcp_score]. Reference [current_cdn] to show the problem persists with their current infrastructure. If no unhealthy data, state the general media performance challenge.
CONSTRAINT: No storytelling, no analogies. Direct statements only. "I ran your site on [tool]" when data exists. Never use data if it shows healthy performance.
[blank line]

Paragraph 2 (SpeedSize Solution + GAP Proof):
GOAL: Explain what SpeedSize does and validate with the strongest proof point.
SIGNAL: Pull from {{valueprop}} for the mechanism explanation. Always include GAP stress-test result. Include [current_cdn] in GAP comparison if available.
CONSTRAINT: Keep mechanism explanation to one sentence. GAP proof as separate sentence. Always say "Our client GAP." Use "stress-tested" (hyphenated).
[blank line]

Paragraph 3 (CTA):
Worth a sponsored media speed test for [company]?

## EMAIL 2 MODE

Mode: Expand/Reframe

Write a follow-up email that shifts to the integration angle.

Instructions:
- Does NOT repeat Email 1's data or investigation — shift to integration simplicity
- Emphasize: one-click plugin or subdomain setup, no dev work required
- Reference the 14-day AWS-sponsored validation period
- Can mention that their team reviews results using their own monitoring tools
- Use a different benefit from {{valueprop}} than Email 1 used
- 40-60 words
- Start with [first_name], — no "Hey" or "Hi"
- CTA should be lighter and more casual than Email 1
- Use [blank line] markers between paragraphs
- No exclamation marks
- Conversational, peer-to-peer tone

## LOGIC FLOW

1. When data available: lead with investigation ("I ran your site") to show you did homework
2. When no data: state the CDN performance gap directly
3. Explain SpeedSize mechanism + GAP proof (one-two punch)
4. Close with sponsored test ask

## OUTPUT EXAMPLES

### Example 1: CrUX Data Available + Cloudflare

Robert, I ran your site on Google's real-time monitoring tool. It shows 33 percent of visitors experienced media loading after 2.5 seconds, even with your current Cloudflare CDN.

[blank line]

SpeedSize loads images and videos much faster without sacrificing quality. Our client GAP stress-tested us against Cloudflare over 200M+ requests and saw 6.5X faster loads.

[blank line]

Worth a sponsored media speed test for RetailCo?

### Example 2: PSI LCP Available + Akamai

Michelle, I ran your site on PageSpeed Insights. Seems like your media loads at 3.2 seconds for your shoppers, even with your current Akamai CDN.

[blank line]

SpeedSize ensures a premium visual experience by loading images and videos much faster without sacrificing quality. Our client GAP stress-tested us against Akamai over 200M+ requests and saw 6.5X faster loads.

[blank line]

Worth a sponsored media speed test for GlobalShop?

### Example 3: No Unhealthy Data Available

Thomas, media optimization lags even with traditional CDNs like Akamai or Cloudflare in place.

[blank line]

SpeedSize ensures a premium visual experience by loading images and videos much faster without sacrificing quality. Our client GAP stress-tested SpeedSize over 200M+ requests and saw 6.5X faster loads and 100MB saved per session.

[blank line]

Worth a sponsored media speed test for FashionBrand?

## CRITICAL CONSTRAINTS
- Never say "we will replace your CDN"
- Never fabricate metrics or data
- Only use LCP if above 2.5s (skip if at or below 2.5s)
- Only use CrUX if P75 above 2.5s (skip if at or below 2.5s)
- Prefer CrUX over PSI when both show unhealthy scores
- Under 75 words strict
- No question marks in body (only CTA)
- Skip problem statement when unhealthy data is available (lead with investigation)
- Include problem statement only when all data healthy or unavailable
- CTA format: "Worth a sponsored media speed test for [company]?"
- No fillers, be direct
- Say "Seems like your media loads at X seconds for your shoppers" not "LCP resource loading duration"
- Always show investigation when using data
- Always say "Our client GAP"
- Complete sentences only
- No percent symbols, currency signs, exclamation marks, em dashes
- Plain language (8th grade readability)
- Start directly with [first_name], no "Hey" or "Hi"
- No line break between name and opener sentence
