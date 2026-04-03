# Clay Formulas

## Purpose
This file contains all calculated variable formulas and the approach selector cascade for the Owner.com campaign. Implement these formulas in Clay.com to generate the required variables.

## Formulas

### estimated_monthly_delivery_orders
```
review_count x 0.15
```
Description: Estimates monthly delivery orders based on total delivery platform review count. Industry heuristic: roughly 1 review per 6-7 orders, applied as 15 percent of total reviews as monthly estimate. This is a rough proxy — acknowledge uncertainty in email copy.
Used in: Approach 1 (Here's the Math)

### estimated_monthly_commission
```
estimated_monthly_delivery_orders x 28 x 0.30
```
Description: Estimates monthly commission paid to third-party delivery apps. Uses $28 average delivery order value (restaurant industry benchmark) and 30 percent commission rate (DoorDash/UberEats standard). Round to nearest hundred.
Used in: Approach 1 (Here's the Math)

### estimated_monthly_delivery_orders_formatted
```
IF(estimated_monthly_delivery_orders >= 1000, ROUND(estimated_monthly_delivery_orders / 1000, 1) + "K", ROUND(estimated_monthly_delivery_orders, 0))
```
Description: Formats order count for natural reading (1200 becomes "1.2K", 800 stays "800").
Used in: Approach 1 (Here's the Math)

### estimated_monthly_commission_formatted
```
IF(estimated_monthly_commission >= 1000, "$" + ROUND(estimated_monthly_commission / 1000, 1) + "K", "$" + ROUND(estimated_monthly_commission, 0))
```
Description: Formats commission amount for natural reading ($8400 becomes "$8.4K", $600 stays "$600").
Used in: Approach 1 (Here's the Math)

### case_study_name
```
IF(cuisine_type contains "pizza", "Metro Pizza",
IF(cuisine_type contains "mexican" OR cuisine_type contains "latin" OR cuisine_type contains "taco", "Talkin Tacos",
IF(cuisine_type contains "asian" OR cuisine_type contains "chinese" OR cuisine_type contains "japanese" OR cuisine_type contains "ramen" OR cuisine_type contains "sushi" OR cuisine_type contains "indian" OR cuisine_type contains "thai" OR cuisine_type contains "vietnamese", "Aburaya Fried Chicken",
IF(cuisine_type contains "greek" OR cuisine_type contains "mediterranean", "Karv Greek Kouzina",
"Doo-Dah Diner"))))
```
Description: Maps cuisine type to the most relevant case study restaurant name for social proof matching.
Used in: All approaches

### case_study_result
```
IF(case_study_name = "Metro Pizza", "+$112K sales, 11K app installs",
IF(case_study_name = "Talkin Tacos", "$120K/mo direct sales, +$435K savings",
IF(case_study_name = "Aburaya Fried Chicken", "+$25K/mo, +$100K delivery savings",
IF(case_study_name = "Karv Greek Kouzina", "+$40K/mo, +300 percent growth",
"+$72K sales, +54 percent growth"))))
```
Description: Maps case study name to its headline result metric for email social proof.
Used in: All approaches

## Approach Selector (Priority Cascade)

### Data Check Columns

approach_1_eligible (Here's the Math):
```
IF(delivery_platform is not empty AND review_count is not empty AND review_count > 50, TRUE, FALSE)
```
Description: Returns TRUE when we have delivery platform data AND enough reviews to estimate order volume. Minimum 50 reviews for credible math.
Variables to check: delivery_platform, review_count

approach_2_eligible (Insider Remark):
```
TRUE
```
Description: Insider Remark is always eligible at the selector stage because research has not run yet. If research later returns INCONCLUSIVE, the copywriter uses MODE B fallback. This is the second priority — it gets selected when Math data is missing.
Note: This approach depends on research quality at runtime, but the selector cannot predict research outcomes.

approach_3_eligible (Customer Empathy):
```
TRUE
```
Description: Fallback approach. Always eligible, works for any restaurant with no special data requirements.

### Selector Column
selected_approach:
```
IF(approach_1_eligible, approach_1_column, IF(approach_2_eligible, approach_2_column, approach_3_column))
```
Description: Priority cascade. Math first (strongest when data available), Insider Remark second (research-dependent), Customer Empathy fallback (always works).

### Setup Instructions
1. Priority 1: Here's the Math — when delivery data is available, math is the most compelling
2. Priority 2: Insider Remark — when no delivery data but research can find a specific observable
3. Priority 3: Customer Empathy — universal fallback, works for any restaurant
4. If you want to shuffle priority order, just rearrange the IF nesting
5. Test with 10-20 sample rows before full deployment

## Implementation Notes
- All formulas use basic math operations compatible with Clay.com
- Variables referenced in formulas must exist as Clay columns
- Test formulas with sample data before deploying at scale
- The $28 average order value and 30 percent commission rate are industry defaults — adjust per campaign if client has better data
- Review count proxy is rough — always use uncertainty language in email copy
