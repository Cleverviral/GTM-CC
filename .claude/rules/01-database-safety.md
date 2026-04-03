---
globs: ["**"]
---

# Database Safety Rules

These rules apply to ALL interactions regardless of role.

## Forbidden Operations
- NEVER construct or execute DELETE statements
- NEVER construct or execute DROP statements
- NEVER construct or execute TRUNCATE statements
- NEVER construct or execute ALTER TABLE statements
- NEVER run UPDATE without a WHERE clause

## Query Safety
- ALWAYS use the `scripts/db.py` utility for database access — never raw HTTP calls
- ALWAYS use parameterized queries (pass values as params, not string interpolation)
- ALWAYS include LIMIT on SELECT queries (max 500)
- ALWAYS show the query before executing writes
- ALWAYS get operator confirmation before any INSERT or UPDATE

## Credential Safety
- NEVER print connection strings, API keys, or passwords in chat
- When reading .env, confirm the key exists but don't show the value
- NEVER include credentials in generated code that gets displayed

## Batch Safety
- Never operate on more than 500 rows in a single write operation without explicit confirmation
- For bulk updates, process in batches of 100 and show progress
- Always show a count of affected rows before executing

## Error Handling
- If a query fails, show the error message clearly
- Suggest fixes but don't auto-retry writes
- If something looks wrong, ask the operator to verify before proceeding
