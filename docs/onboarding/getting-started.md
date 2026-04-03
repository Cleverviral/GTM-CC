# Getting Started with GTM-CC

## What is this?

GTM-CC is our database-powered cold email campaign system. Instead of managing hundreds of Clay tables, everything lives in one Neon PostgreSQL database. You interact with it through Claude Code using simple commands.

## How to Access

### Option A: Claude Code on the Web (Recommended)
1. Go to [claude.ai/code](https://claude.ai/code)
2. Connect the GTM-CC GitHub repository
3. Start a conversation — Claude will ask who you are
4. Use your role's commands (listed below)

### Option B: Claude Code in Terminal
1. Open Terminal
2. Navigate to the GTM-CC folder
3. Run `claude` to start
4. Claude will ask who you are

## First Steps

When you start a session, Claude will ask:

> "Who am I working with today?"
> 1. Kuldeep — Clay Operator
> 2. Hasan — Campaign Operator
> 3. Mayank — Strategist

Pick your role. Claude will show your available commands and enforce your permissions.

## Your Commands

### Clay Operator (Kuldeep)
| Type This | What Happens |
|-----------|-------------|
| `/pull-leads` | Step-by-step guide to select client, segment, and pull leads |
| `/push-to-clay` | Push pulled leads to your Clay table via webhook |
| `/check-batch` | See recent batch history |
| `/export-csv` | Export leads + emails as CSV |

### Campaign Operator (Hasan)
| Type This | What Happens |
|-----------|-------------|
| `/get-batch` | Download a ready batch for sequencer upload |
| `/check-outputs` | View email output stats for any client/segment |
| `/reuse-emails` | Pull existing emails when you need fresh infrastructure |

### Strategist (Mayank)
All of the above, plus:
| Type This | What Happens |
|-----------|-------------|
| `/create-recipe` | Create a new email recipe |
| `/test-recipe` | Test a recipe on sample leads |
| `/review-performance` | View stats and batch history |

## Key Things to Know

1. **You can't break anything.** The system has safety guardrails. Dangerous operations are blocked.
2. **Claude asks the right questions.** You don't need to know SQL. Just follow the prompts.
3. **Everything is tracked.** Every email output is stored with recipe version, batch ID, and approach.
4. **Read-only is safe.** Campaign operators can only read data — no accidental modifications possible.

## Need Help?

- Type `/whoami` to see your role and commands
- Ask Claude "what can I do?" for a quick reference
- If something feels wrong, stop and ask Mayank
