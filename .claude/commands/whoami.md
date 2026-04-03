# Identify Your Role

Ask the user to identify themselves:

> **Welcome to GTM-CC! Who am I working with today?**
>
> 1. **Kuldeep** — Clay Operator (pull leads, push to Clay, export batches)
> 2. **Hasan** — Campaign Operator (download batches, upload to sequencer)
> 3. **Mayank** — Strategist (create recipes, review performance, full access)
>
> Type your name or number.

Once identified, confirm their role and show available commands:

### If Clay Operator (Kuldeep):
> **Hey Kuldeep!** You're set up as the **Clay Operator**.
>
> Your commands:
> | Command | What It Does |
> |---------|-------------|
> | `/pull-leads` | Pull leads for a client+segment (guided) |
> | `/push-to-clay` | Push leads to a Clay table via webhook |
> | `/check-batch` | View recent batch history |
> | `/export-csv` | Export leads + emails as CSV |
>
> **Start with `/pull-leads` for your typical workflow.**

### If Campaign Operator (Hasan):
> **Hey Hasan!** You're set up as the **Campaign Operator**.
>
> Your commands:
> | Command | What It Does |
> |---------|-------------|
> | `/get-batch` | Download a ready batch as CSV for sequencer |
> | `/check-outputs` | View email output stats |
> | `/reuse-emails` | Pull existing emails for bad-infra re-send |
>
> **Start with `/get-batch` to download a batch for your sequencer.**
> You have read-only access — nothing can be accidentally modified.

### If Strategist (Mayank):
> **Hey Mayank!** You're set up as the **Strategist** with full access.
>
> Your commands (plus all Clay/Campaign commands):
> | Command | What It Does |
> |---------|-------------|
> | `/create-recipe` | Create a new recipe (guided) |
> | `/test-recipe` | Test recipe on sample leads |
> | `/review-performance` | View batch stats and output history |
>
> You also have access to all Clay Operator and Campaign Operator commands.

Set the role context for the rest of this session.
