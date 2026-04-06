# GTM-CC: DB-Powered Campaign System

## Role Detection (ALWAYS DO THIS FIRST)

At the **start of every conversation**, ask:

> "Who am I working with today?
> 1. **Copy Strategist** — creates recipes, manages clients/segments, full DB access
> 2. **Clay Operator** — pulls leads, pushes to Clay, manages enrichment
> 3. **Campaign Operator** — exports CSVs, views email outputs (read-only)
>
> Type your role number."

Once identified, enforce that role's permissions for the entire session. Refer to the permissions matrix below. If someone tries to do something outside their role, politely redirect them.

After identifying the role, show their available commands:
- Copy Strategist: `/create-recipe`, `/test-recipe`, `/pull-leads`, `/add-leads`, `/push-to-clay`, `/export-csv`, `/check-outputs`, `/generate-http-query` + free-form SQL
- Clay Operator: `/pull-leads`, `/add-leads`, `/push-to-clay`, `/export-csv`, `/generate-http-query`
- Campaign Operator: `/export-csv`, `/check-outputs`

---

## System Overview

GTM-CC is a cold email campaign system with:
- **1 Neon PostgreSQL database** (connection string in `.env` as `NEON_CONNECTION_STRING` or `NEON_TEST_CONNECTION_STRING`)
- **5 tables**: clients, segments, leads, recipes, email_outputs
- **3 roles**: Copy Strategist (admin), Clay Operator, Campaign Operator
- **Clay integration**: Webhook push (Neon → Clay) + HTTP columns push-back (Clay → Neon)

---

## Database Schema (v4.0)

### clients
| Column | Type | Notes |
|--------|------|-------|
| client_id | UUID PK | From Tally onboarding |
| client_name | text | |
| client_website | text | |
| client_status | text | in_onboarding / active / paused / churned |
| target_icp_details | text | ICP lives on CLIENT |
| target_persona | text | |
| pain_points | text | |
| client_usp_differentiators | text | |
| approved | boolean | Must be true before use |

### segments
| Column | Type | Notes |
|--------|------|-------|
| segment_id | serial PK | Stored in leads.segment_ids[] |
| client_id | UUID FK → clients | |
| segment_name | text | e.g., "1M+ Qualified" |
| segment_tag | text | Human-readable label |
| description | text | |
| status | text | active / paused / archived |
| leadlist_context | text | Targeting criteria for this segment |
| value_prop | text | Value proposition for this segment |

### leads
| Column | Type | Notes |
|--------|------|-------|
| lead_id | serial PK | |
| email | text UNIQUE | Primary dedup key |
| first_name, last_name, full_name | text | |
| job_title | text | |
| linkedin_profile_url | text | |
| company_name, company_domain, company_website | text | |
| industry | text | |
| monthly_visits | int | |
| employee_count | text | Clay sends ranges |
| email_verified | text | |
| email_verified_at | timestamptz | |
| is_catchall | text | |
| mx_provider | text | |
| has_email_security_gateway | text | |
| lcp | float | Largest Contentful Paint |
| tti | float | Time to Interactive |
| aov | float | Average Order Value |
| segment_ids | int[] | Array of segment IDs |
| info_tags | text[] | Free-form context tags |
| extra_data | jsonb | Flexible catch-all for Clay enrichment data |

### recipes
| Column | Type | Notes |
|--------|------|-------|
| recipe_id | serial PK | |
| client_id | UUID FK | |
| segment_id | int FK | |
| version | int | Bumps on ANY change |
| status | text | active / inactive / testing |
| approach_content | text | Full playbook (reference, NOT pushed to Clay) |
| data_variables_required | text[] | What data the recipe needs |
| clay_template_name | text | Saved Clay template to use |
| clay_instructions | text | Step-by-step for Clay operator |
| sample_email_id | text | ID from Notion sample email repo (for campaign naming + dashboard) |
| notes | text | What changed in this version |

### email_outputs
| Column | Type | Notes |
|--------|------|-------|
| output_id | serial PK | |
| lead_id | int FK → leads | |
| client_id | UUID FK | Denormalized for queries |
| segment_id | int FK | |
| recipe_id | int FK | |
| recipe_version | int | |
| selected_approach | text | Which approach ran |
| email_1_variant_a | text | Primary email 1 |
| email_1_variant_b | text | A/B variant |
| email_2_variant_a | text | Primary email 2 |
| email_2_variant_b | text | A/B variant |
| email_3_variant_a | text | Primary email 3 |
| email_3_variant_b | text | A/B variant |
| company_summary | text | |
| batch_id | text | Groups a Clay run |

---

## Permissions Matrix

| Action | Copy Strategist | Clay Operator | Campaign Operator |
|--------|----------------|---------------|-------------------|
| SELECT any table | Yes | Yes | Yes |
| INSERT/UPDATE clients | Yes | No | No |
| INSERT/UPDATE segments | Yes | No | No |
| UPDATE leads (enrichment) | Yes | Yes (via commands) | No |
| INSERT/UPDATE recipes | Yes | No | No |
| INSERT email_outputs | Yes | Yes (via Clay HTTP) | No |
| Export CSV | Yes | Yes | Yes |
| Push to Clay webhook | Yes | Yes | No |
| Generate HTTP queries | Yes | Yes | No |
| Free-form SQL queries | Yes | No | No |

---

## Database Access

All database operations go through the `scripts/db.py` utility. Use it like this:

```python
import sys; sys.path.insert(0, 'scripts')
from db import query, read_query, write_query
```

- `read_query(sql, params=[])` — SELECT queries. Always use this.
- `write_query(sql, params=[])` — INSERT/UPDATE. Shows preview + asks confirmation.
- NEVER construct raw HTTP calls to Neon. ALWAYS use db.py.

---

## Safety Rules (ALL ROLES)

1. **NEVER** run DELETE, DROP, TRUNCATE, or ALTER statements
2. **NEVER** run UPDATE without a WHERE clause
3. **NEVER** expose connection strings, API keys, or credentials in chat
4. **ALWAYS** show the query and row count before any write operation
5. **ALWAYS** confirm with the operator before executing writes
6. **ALWAYS** use parameterized queries (pass values as params, not string concatenation)
7. **ALWAYS** include LIMIT on SELECT queries (max 500 rows)
8. When reading `.env`, confirm the key exists but NEVER print the actual value

---

## API Key Management

When a user shares an API key or secret:
- Immediately save it to `.env`
- Use SCREAMING_SNAKE_CASE for the variable name
- Never expose the value in chat — just confirm it was saved
- If a key exists for the same service, update it

---

## Clay Integration

### Webhook Push (Neon → Clay): 38 Fields
When pushing leads to Clay, ALL 38 fields must be included. See `/push-to-clay` command for the complete payload spec.

### HTTP Push-back (Clay → Neon)
- HTTP Col 1: Verification data → UPDATE leads (email_verified, is_catchall, mx_provider)
- HTTP Col 2: Enrichment data → UPDATE leads (lcp + extra_data JSONB merge)
- HTTP Col 3: Email outputs → INSERT email_outputs (9 params: lead_id, client_id, segment_id, recipe_id, recipe_version, selected_approach, email_1/2/3_variant_a)

### Approach Selection
Approaches live in saved Clay templates, NOT in the webhook payload. The recipe stores the `clay_template_name` so the operator knows which template to use.

---

## Available Commands

### Copy Strategist (all commands + free-form SQL)
| Command | What It Does |
|---------|-------------|
| `/create-recipe` | Create a new recipe (guided flow) |
| `/test-recipe` | Test a recipe on sample leads (dry run) |
| `/pull-leads` | Pull leads for a client+segment with guided filters |
| `/add-leads` | Import leads from CSV into a segment |
| `/push-to-clay` | Push leads to Clay table via webhook (38 fields) |
| `/export-csv` | Export leads + emails as CSV |
| `/check-outputs` | View email output stats for a client+segment |
| `/generate-http-query` | Generate HTTP push-back query for Clay operator |

### Clay Operator
| Command | What It Does |
|---------|-------------|
| `/pull-leads` | Pull leads for a client+segment with guided filters |
| `/add-leads` | Import leads from CSV into a segment |
| `/push-to-clay` | Push leads to Clay table via webhook (38 fields) |
| `/export-csv` | Export leads + emails as CSV |
| `/generate-http-query` | Generate HTTP push-back query (enrichment or email outputs) |

### Campaign Operator
| Command | What It Does |
|---------|-------------|
| `/export-csv` | Export leads + emails as CSV with tracking fields |
| `/check-outputs` | View email output stats for a client+segment |
