# Cursor Setup Guide for Team

## What You'll Need

1. **Cursor** (free download from cursor.com)
2. **GitHub account** (to clone the repo)
3. **Neon connection string** (get from Mayank)
4. **Node.js** (for the Neon MCP server — download from nodejs.org)

## Step-by-Step Setup

### 1. Install Cursor

Download from [cursor.com](https://cursor.com) and install.
It looks like VS Code — if you've used VS Code, it's identical.

### 2. Clone the Repository

Open Cursor → Terminal (Ctrl+` or Cmd+`) → Run:
```bash
git clone https://github.com/[your-org]/GTM-CC.git
cd GTM-CC
```

Then: File → Open Folder → select the GTM-CC folder.

### 3. Set Up Your Environment Variable

The Neon MCP server needs the connection string. Set it in your terminal:

**Mac/Linux:**
```bash
# Add this to your ~/.zshrc or ~/.bashrc
export NEON_API_KEY="your-neon-api-key-here"
```

Then restart Cursor (so it picks up the variable).

**Windows:**
```powershell
# Run in PowerShell as admin
[System.Environment]::SetEnvironmentVariable('NEON_API_KEY', 'your-neon-api-key-here', 'User')
```

Restart Cursor.

### 4. Create Your .env File

Copy the template:
```bash
cp .env.example .env
```

Edit `.env` and paste the Neon connection string (get from Mayank).

### 5. Verify MCP Connection

Open Cursor Settings → MCP → You should see "neon-postgres" listed.
If it shows a green dot, the connection is working.

If you see errors:
- Make sure Node.js is installed (`node --version` in terminal)
- Make sure the NEON_API_KEY environment variable is set
- Restart Cursor

### 6. Start Working

Open the Cursor AI chat (Cmd+L or Ctrl+L) and say:
> "Hi, I'm Kuldeep" (or Hasan, or Mayank)

Cursor will:
1. Identify your role
2. Show your available workflows
3. Guide you step-by-step through any task

## Your Workflows

### Clay Operator (Kuldeep)
Just tell Cursor what you want:
- "Pull leads for SpeedSize 1M+ segment"
- "Push these leads to Clay" (have webhook URL ready)
- "Check recent batches"
- "Export leads as CSV for Hasan"

Cursor will ask you the right questions. You don't need to know SQL.

### Campaign Operator (Hasan)
- "Get me a batch for SpeedSize"
- "Check email outputs for SpeedSize 1M+"
- "I need to reuse emails — bad infrastructure"

Your access is read-only. You can't accidentally break anything.

### Strategist (Mayank)
All of the above, plus:
- "Create a new recipe for SpeedSize 1M+"
- "Test this recipe on sample leads"
- "Review performance for SpeedSize"
- Or run any custom query

## FAQ

**Q: Do I need to know SQL?**
No. Cursor (Claude) handles all queries. Just describe what you want in plain English.

**Q: Can I break the database?**
No. DELETE, DROP, and UPDATE-without-WHERE are all blocked. Campaign Operator is fully read-only.

**Q: Do I need my own Claude subscription?**
No. The API key is shared. Mayank sets it up.

**Q: Where do exported CSVs go?**
In the `exports/` folder inside the project. You can find them in Cursor's file explorer on the left.

**Q: What if I get an error?**
Screenshot it and send to Mayank. Don't try to fix it yourself.
