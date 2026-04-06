# Identify Your Role

Ask the user to identify themselves:

> **Welcome to GTM-CC! Who am I working with today?**
>
> 1. **Copy Strategist** — Full access (recipes, segments, clients, all commands)
> 2. **Clay Operator** — Pull leads, push to Clay, enrichment, export
> 3. **Campaign Operator** — Check outputs, export CSV (read-only)
>
> Type your role name or number.

Once identified, confirm their role and show available commands:

### If Copy Strategist:
> You're set up as the **Copy Strategist** (admin role).
>
> Your commands:
> | Command | What It Does |
> |---------|-------------|
> | `/create-recipe` | Create a new recipe (guided) |
> | `/test-recipe` | Test recipe on sample leads |
> | `/pull-leads` | Pull leads for a client+segment (guided) |
> | `/add-leads` | Import leads from CSV into a segment |
> | `/push-to-clay` | Push leads to a Clay table via webhook |
> | `/generate-http-query` | Generate HTTP push-back query for Clay |
> | `/check-outputs` | View email output stats |
> | `/export-csv` | Export leads + emails as CSV |
>
> You also have full access to custom SQL queries (with safety rules).

### If Clay Operator:
> You're set up as the **Clay Operator**.
>
> Your commands:
> | Command | What It Does |
> |---------|-------------|
> | `/pull-leads` | Pull leads for a client+segment (guided) |
> | `/add-leads` | Import leads from CSV into a segment |
> | `/push-to-clay` | Push leads to a Clay table via webhook |
> | `/generate-http-query` | Generate HTTP push-back query for Clay |
> | `/check-outputs` | View email output stats |
> | `/export-csv` | Export leads + emails as CSV |
>
> **Start with `/pull-leads` for your typical workflow.**

### If Campaign Operator:
> You're set up as the **Campaign Operator**.
>
> Your commands:
> | Command | What It Does |
> |---------|-------------|
> | `/check-outputs` | View email output stats |
> | `/export-csv` | Export leads + emails as CSV |
>
> You have read-only access — nothing can be accidentally modified.
> If you need data changed, ask the Clay Operator or Copy Strategist.

Set the role context for the rest of this session.
