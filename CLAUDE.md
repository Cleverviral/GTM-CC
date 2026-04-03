# GTM-CC: DB-Powered Campaign System

## Role Detection (ALWAYS DO THIS FIRST)

At the **start of every conversation**, ask:

> "Who am I working with today?
> 1. **Kuldeep** — Clay Operator
> 2. **Hasan** — Campaign Operator
> 3. **Mayank** — Strategist
>
> Type your name or role number."

Once identified, enforce that role's permissions for the entire session. Refer to the permissions matrix below. If someone tries to do something outside their role, politely redirect them.

After identifying the role, show their available commands:
- Clay Operator: `/pull-leads`, `/push-to-clay`, `/check-batch`, `/export-csv`
- Campaign Operator: `/get-batch`, `/check-outputs`, `/reuse-emails`
- Strategist: `/create-recipe`, `/test-recipe`, `/review-performance` + all Clay/Campaign commands

---

## System Overview

GTM-CC is a cold email campaign system with:
- **1 Neon PostgreSQL database** (connection string in `.env` as `NEON_CONNECTION_STRING` or `NEON_TEST_CONNECTION_STRING`)
- **5 tables**: clients, segments, leads, recipes, email_outputs
- **3 roles**: Strategist, Clay Operator, Campaign Operator
- **Clay integration**: Webhook push (Neon → Clay) + 3 HTTP columns push-back (Clay → Neon)

---

## Database Schema (v3.1)

### clients
| Column | Type | Notes |
|--------|------|-------|
| client_id | UUID PK | From Tally onboarding |
| client_name | text | |
| client_website | text | |
| client_status | text | in_onboarding / active / paused / churned |
| target_icp_details | text | ICP lives on CLIENT, not segment |
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
| status | text | active / paused / archived |

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
| lcp | float | Largest Contentful Paint |
| tti | float | Time to Interactive |
| aov | float | Average Order Value |
| segment_ids | int[] | Array of segment IDs |
| info_tags | text[] | Free-form context tags |
| extra_data | jsonb | Flexible catch-all |

### recipes
| Column | Type | Notes |
|--------|------|-------|
| recipe_id | serial PK | |
| client_id | UUID FK | |
| segment_id | int FK | |
| version | int | Bumps on ANY change |
| status | text | active / inactive / testing |
| approach_content | text | Full playbook |
| value_prop | text | |
| clay_instructions | text | Step-by-step for Clay operator |

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
| subject_line_1, subject_line_2 | text | |
| email_1_variant_a/b/c | text | 3 variants per email |
| email_2_variant_a/b/c | text | |
| email_3_variant_a/b/c | text | |
| company_summary | text | |
| batch_id | text | Groups a Clay run |

---

## Permissions Matrix

| Action | Strategist | Clay Operator | Campaign Operator |
|--------|-----------|---------------|-------------------|
| SELECT any table | Yes | Yes | Yes |
| INSERT/UPDATE clients | Yes | No | No |
| INSERT/UPDATE segments | Yes | No | No |
| UPDATE leads (enrichment) | Yes | Yes (via commands) | No |
| INSERT/UPDATE recipes | Yes | No | No |
| INSERT email_outputs | Yes | Yes (via Clay) | No |
| Export CSV | Yes | Yes | Yes |
| Push to Clay webhook | Yes | Yes | No |
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

## Available Commands

### Clay Operator (Kuldeep)
| Command | What It Does |
|---------|-------------|
| `/pull-leads` | Pull leads for a client+segment with guided filters |
| `/push-to-clay` | Push pulled leads to a Clay table via webhook |
| `/check-batch` | View recent batch history and status |
| `/export-csv` | Export leads + emails as CSV for campaign operator |

### Campaign Operator (Hasan)
| Command | What It Does |
|---------|-------------|
| `/get-batch` | Get a ready batch with emails as CSV |
| `/check-outputs` | View email output stats for a client+segment |
| `/reuse-emails` | Pull existing emails for bad-infra re-send |

### Strategist (Mayank)
All of the above, plus:
| Command | What It Does |
|---------|-------------|
| `/create-recipe` | Create a new recipe (guided) |
| `/test-recipe` | Test a recipe on sample leads |
| `/review-performance` | View batch stats and output history |
