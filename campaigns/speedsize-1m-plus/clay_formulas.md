# Clay Formulas

## Purpose
This file contains all calculated variable formulas and the approach selector cascade for the SpeedSize 1M+ campaign. Implement these formulas in Clay.com to generate the required variables.

## Formulas

### monthly_visits_formatted
```
IF(monthly_visits >= 1000000, ROUND(monthly_visits / 1000000, 1) + "M", IF(monthly_visits >= 1000, ROUND(monthly_visits / 1000, 0) + "K", monthly_visits))
```
Description: Formats monthly visit count for natural reading (9477898 becomes "9.5M", 153000 becomes "153K").
Used in: Approach 1 (Customer Empathy), Approach 3 (Insider Remark)

### lcp_unhealthy
```
IF(lcp is not empty AND lcp > 2.5, TRUE, FALSE)
```
Description: Returns TRUE when PageSpeed LCP score indicates poor media performance (above 2.5 second threshold).
Used in: Approach 1, Approach 2

### crux_unhealthy
```
IF(crux_lcp_p75 is not empty AND crux_lcp_p75 > 2500, TRUE, FALSE)
```
Description: Returns TRUE when CrUX P75 LCP indicates poor real-user media experience (above 2500ms threshold). Note: CrUX values are in milliseconds.
Used in: Approach 1, Approach 2

### crux_poor_pct
```
IF(crux_unhealthy, ROUND((crux_lcp_p75 - 2500) / 2500 * 100, 0) + " percent", "")
```
Description: Estimates the percentage of visitors experiencing poor media loads based on CrUX P75 deviation from 2.5s threshold. Rough proxy for narrative use.
Used in: Approach 1, Approach 2

## Approach Selector (Single Column)

One formula column determines which approach to use per lead. No separate eligibility columns needed.

### selected_approach
```
IF(
  OR(lcp_unhealthy = TRUE, crux_unhealthy = TRUE),
  approach_1_column,
  IF(
    researchReport is not empty AND researchReport != "RESEARCH INCONCLUSIVE",
    approach_3_column,
    approach_2_column
  )
)
```
Description: Priority cascade in one formula. Checks data availability inline and selects the best-fit approach.
- Priority 1: Customer Empathy Mirror — fires when LCP or CrUX shows unhealthy performance (data validates the scenario)
- Priority 2: Insider Remark — fires when no unhealthy data but research returned usable findings
- Priority 3: Ultra-Direct Recent Proof — universal fallback, always works

### Setup Instructions
1. Create one formula column called "selected_approach"
2. Paste the formula above — it references lcp_unhealthy, crux_unhealthy (formula columns above), researchReport (Claygent output), and the three approach content columns
3. The approach_1_column, approach_2_column, approach_3_column reference the Clay columns where each approach file content is stored
4. To shuffle priority order, rearrange the IF nesting
5. Test with 10-20 sample rows before full deployment

## Implementation Notes
- All formulas use basic operations compatible with Clay.com
- CrUX values are in milliseconds (2500ms = 2.5 seconds)
- PageSpeed LCP values are in seconds
- Variables referenced in formulas must exist as Clay columns
- Test formulas with sample data before deploying at scale
- The approach selector cascade runs AFTER enrichment and research columns
