# Data Variables Required

## Always Needed (Every Row)
- [first_name] - prospect first name
- [company] - company name
- [job_title] - prospect role
- [company_website] - company domain
- [industry] - company industry or vertical
- [product_category] - what they sell (extracted from website scrape)

## Conditional (Approach-Dependent)
- [lcp_score] - media load time in seconds, used by Approach 1 and 2 (only used if above 2.5s)
- [crux_lcp_p75] - real-user P75 media load time in milliseconds, used by Approach 1 and 2 (only used if above 2500ms)
- [crux_poor_pct] - percentage of visitors with poor media experience, used by Approach 1 and 2
- [current_cdn] - detected CDN provider name (Cloudflare, Akamai, CloudFront, etc.), used by all approaches when available
- [monthly_visits] - raw monthly site traffic count, used for formatting
- [researchReport] - structured research report from Researcher Agent, used by Approach 3

## Calculated (Clay Formulas)
- [monthly_visits_formatted] - monthly traffic formatted K/M (see clay_formulas.md)
- [lcp_unhealthy] - boolean, TRUE if LCP above 2.5s (see clay_formulas.md)
- [crux_unhealthy] - boolean, TRUE if CrUX P75 above 2500ms (see clay_formulas.md)
- [approach_1_eligible] - boolean, TRUE if unhealthy performance data available (see clay_formulas.md)
- [approach_3_eligible] - boolean, TRUE if research returned usable findings (see clay_formulas.md)
- [selected_approach] - the full approach content selected for this lead via priority cascade (see clay_formulas.md)
