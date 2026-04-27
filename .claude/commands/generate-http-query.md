# Generate HTTP Push-Back Body for a Clay Table

Help the operator wire a Clay table's HTTP column to push data back into Neon. Available to **Copy Strategist** and **Clay Operator**.

## What this command does (and doesn't)

Every Clay table now uses **one universal HTTP body** that calls a single Postgres function — `upsert_lead()`. There is no per-table SQL to write anymore. This command:

1. Helps the operator pick the **6 per-table placeholder values** that go into the universal body.
2. Generates a ready-to-paste body for that Clay table.
3. Walks them through Clay's "Apply template" quirks (Required toggle + "Don't have it" column).

It does **NOT** generate raw `UPDATE leads ...` or `INSERT INTO email_outputs ...` SQL — that pattern is retired. The function in `db/functions/upsert_lead.sql` handles all merge logic, type coercion, and the email_outputs insert in one call.

If the operator asks for a one-off raw SQL push-back, redirect them:
> "All Clay → Neon push-back goes through `upsert_lead()` now. Tell me which Clay table you're wiring up and I'll generate the body for you."

The full reference doc is `docs/clay-http-template.md`. This command is the conversational wrapper around it.

## Step 1: Identify the Clay table + segment

Ask:
> **Which Clay table are you wiring up?**
> - Clay table name (e.g. `"TryNow Beauty Apollo Set 1"`)
> - Which client + segment does it push into?

Pull client/segment context:

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query

clients = read_query("SELECT client_id, client_name FROM clients WHERE client_status = 'active' LIMIT 50")
# After client selection:
segments = read_query("SELECT segment_id, segment_name, segment_tag FROM segments WHERE client_id = $1 LIMIT 50", [str(client_id)])
```

Show numbered lists. Capture: `clay_table_name`, `segment_id` (or comma-separated multi).

## Step 2: Enrichment-only OR generating emails?

Ask:
> **What is this Clay table doing?**
> 1. **Enrichment only** — pushing verification + extra_data back, no emails generated yet
> 2. **Generating emails** — Clay table runs the recipe and produces email_1/2/3 outputs

This drives whether slots 24, 25, 26, 28–35 carry recipe + email content or stay empty.

If "generating emails", look up the active recipe for the primary segment:

```python
recipe = read_query("""
    SELECT recipe_id, version, clay_template_name, clay_template_link
    FROM recipes
    WHERE segment_id = $1 AND status = 'active'
    LIMIT 1
""", [primary_segment_id])
```

If no active recipe and the operator picked option 2, stop:
> No active recipe for segment {N}. Ask the Copy Strategist to create one with `/create-recipe` first.

## Step 3: Collect the 6 per-table placeholder values

The universal body has 6 slots that change per Clay table. Ask the operator for each:

| Slot | Placeholder | Question to ask | Example |
|---:|---|---|---|
| 2 | `<SEGMENT_ID>` | Use the segment_id from Step 1 | `"54"` or `"28,37"` |
| 21 | `<INFO_TAGS>` | "Any free-form info tags? Comma-separated, or empty." | `"q2-rerun, builtwith-data"` or `""` |
| 22 | `<EXTRA_DATA_BUILDER>` | "Which Clay columns should land in `leads.extra_data`? Give me a list of `key|Clay Column` pairs." | `"product_category|{{Product Category}};aov|{{AOV}}"` or `""` |
| 23 | `<CLAY_TABLE_NAMES>` | Use the Clay table name from Step 1 | `"TryNow Beauty Apollo Set 1"` |
| 24 | `<RECIPE_ID_OR_EMPTY>` | From Step 2 — recipe_id if generating, `""` if enrichment-only | `"51"` or `""` |
| 25 | `<RECIPE_VERSION_OR_EMPTY>` | From Step 2 — version if generating, `""` if enrichment-only | `"1"` or `""` |
| 35 | `<PERSONALIZATIONS_BUILDER_OR_EMPTY>` | "Any per-lead personalizations to capture in `email_outputs.personalizations`? Same `key|Clay Column` format. Empty if enrichment-only." | `"first_line|{{First Line}};research_report|{{Research Report}}"` or `""` |

### Builder format reminders (slots 22 + 35)

- **Pipe-and-semicolon, NOT JSON.** `key|{{Column}};key2|{{Column2}}`.
- Each pair: `snake_case_key | {{Clay Column Name}}`.
- Pairs separated by `;`.
- `key`s become jsonb keys in the DB; `{{...}}` is Clay's per-row substitution.
- Empty values + `CLAYFORMATVALUE(...)` are filtered out by the function. The operator does not need to wrap things in NULLIF.

## Step 4: Generate the body

Take the universal body from `docs/clay-http-template.md` and substitute the 6 placeholder values. Output the full JSON body in a code block, ready to copy-paste.

After the body, show the **endpoint config**:

> **Method:** POST
> **URL:** `https://ep-wild-bonus-anpaxuk6.c-6.us-east-1.aws.neon.tech/sql`
> **Headers:**
> - `Content-Type: application/json`
> - `Neon-Connection-String: <paste from .env → NEON_TEST_CONNECTION_STRING — never paste in chat>`

## Step 5: Walk through Clay's two quirks

Tell the operator:

> **Two things will trip you up in Clay's "Apply template" UI. Read this before clicking save.**
>
> **Quirk 1 — Required toggle.** Clay marks every variable as "required" by default and won't let the column run with anything unmapped. Walk down the variable list and **toggle OFF "Required" for every variable except `Email` and `p_segments_ids`**.
>
> **Quirk 2 — "Don't have it" column.** Clay still needs *something* mapped per variable. Make sure your Clay table has a column literally named `Don't have it` (always blank). For any `{{Variable}}` your table doesn't have a real column for, map it to `Don't have it`. The function normalizes the blank to NULL safely.

## Step 6: Test on 1 row

Tell the operator:

> **Run the HTTP column on 1 row first.** Then run this query to verify:
>
> ```sql
> SELECT lead_id, email, segment_ids, clay_table_names, info_tags, extra_data
> FROM leads
> WHERE email = '<email of the test lead>';
> ```
>
> If you see the lead with `clay_table_names` containing `"{clay_table_name}"`, the segment in `segment_ids[]`, and your enrichment keys in `extra_data`, you're good.
>
> If the response cell shows an error, the most common ones are:
> - `These segment_ids do not exist: {N}` → wrong segment_id in slot 2
> - `p_recipe_id N does not match the primary segment` → recipe_id in slot 24 isn't the active one for the primary segment
> - `truee` / `falsee` in stored verification fields → stray `e` after a `{{Variable}}` in the body, edit and remove

## Important

- Never include the connection string in chat or in the generated body. The operator pastes it in Clay's Headers config.
- Never write a raw `UPDATE leads ...` or `INSERT INTO email_outputs ...` query — everything goes through `upsert_lead()`.
- The function preserves the "new data never destroys old data" rule: empty incoming values leave existing values untouched. The operator does not need to defend against this in the body.
- Full reference (every slot, format details, error catalog) is in `docs/clay-http-template.md`.
