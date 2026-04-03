# Data Variables Required

## Always Needed (Every Row)
- [first_name] - prospect first name
- [company] - restaurant name
- [job_title] - prospect role (owner, GM, operator)
- [company_website] - restaurant domain
- [cuisine_type] - restaurant cuisine category (pizza, Mexican, Asian, Mediterranean, American, etc.)
- [case_study_name] - cuisine-matched case study restaurant name (calculated via lookup)
- [case_study_result] - cuisine-matched case study headline result (calculated via lookup)

## Conditional (Approach-Dependent)
- [delivery_platform] - which third-party delivery app(s) the restaurant is listed on (DoorDash, UberEats, Grubhub) — used by Approach 1 (Math) and Approach 3 (Customer Empathy) for specificity
- [review_count] - total review count across delivery platforms — used by Approach 1 (Math) for order volume estimation
- [review_count_formatted] - review count formatted K/M — used by Approach 1 (Math)

## Calculated (Clay Formulas)
- [estimated_monthly_delivery_orders] - estimated monthly delivery orders based on review count proxy (see clay_formulas.md)
- [estimated_monthly_delivery_orders_formatted] - formatted K/M for email copy
- [estimated_monthly_commission] - estimated monthly commission paid to delivery platforms (see clay_formulas.md)
- [estimated_monthly_commission_formatted] - formatted with dollar sign and K/M for email copy
- [case_study_name] - cuisine-type lookup (see clay_formulas.md)
- [case_study_result] - case study result lookup (see clay_formulas.md)
