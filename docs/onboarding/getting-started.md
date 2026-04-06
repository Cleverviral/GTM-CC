# Getting Started with GTM-CC

## What is this?

GTM-CC is a database-powered cold email campaign system. Instead of managing dozens of Clay tables and spreadsheets, everything lives in one Neon PostgreSQL database. You interact with it through Cursor (or Claude Code) using simple slash commands.

## How to Set Up

See the **GTM-CC Setup Guide** (`docs/gtm-cc-setup-guide.pdf`) for step-by-step instructions.

Quick version:
1. Install Cursor from cursor.com
2. Clone the repo: `git clone https://github.com/cleverviral-mayank/GTM-CC.git`
3. Open the folder in Cursor
4. Download the `.env` file from Google Drive → drop it in the GTM-CC folder
5. Type `/whoami` in the AI chat → pick your role

## Roles

| # | Role | Access Level |
|---|------|-------------|
| 1 | Copy Strategist | Full access — admin role |
| 2 | Clay Operator | Pull leads, push to Clay, enrichment, export |
| 3 | Campaign Operator | Check outputs, export CSV (read-only) |

## Available Commands

### Clay Operator
| Command | What It Does |
|---------|-------------|
| `/pull-leads` | Pull leads for a client + segment (guided) |
| `/push-to-clay` | Push leads to a Clay table via webhook |
| `/generate-http-query` | Generate HTTP push-back query for Clay columns |
| `/check-outputs` | View email output stats |
| `/export-csv` | Export leads + emails as CSV |

### Campaign Operator
| Command | What It Does |
|---------|-------------|
| `/check-outputs` | View email output stats |
| `/export-csv` | Export leads + emails as CSV |

### Copy Strategist (all of the above, plus:)
| Command | What It Does |
|---------|-------------|
| `/create-recipe` | Create a new email recipe |
| `/test-recipe` | Test a recipe on sample leads |

The Copy Strategist can also run custom database queries in plain English.

## Key Things to Know

1. **You can't break anything.** Dangerous operations are blocked. Campaign Operator is fully read-only.
2. **Claude asks the right questions.** You don't need SQL. Just follow the prompts.
3. **Everything is tracked.** Every email output is stored with recipe version and approach name.
4. **Keeping updated:** Run `git pull` in the terminal to get the latest commands.

## Need Help?

- Type `/whoami` to see your role and commands
- Ask Claude "what can I do?" for a quick reference
- If something feels wrong, stop and ask the Copy Strategist
