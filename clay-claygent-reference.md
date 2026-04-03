# Clay & Claygent: Complete Reference Document

> Last researched: March 2026. Sources include Clay's official docs, Clay University, community forums, and third-party tutorials.

---

## Table of Contents

1. [What is Clay?](#1-what-is-clay)
2. [Clay's AI Features Overview](#2-clays-ai-features-overview)
3. [Claygent: The AI Research Agent](#3-claygent-the-ai-research-agent)
4. [Claygent Navigator](#4-claygent-navigator)
5. [The "Use AI" Column](#5-the-use-ai-column)
6. [Claygent Builder (Workspace-Level Agents)](#6-claygent-builder-workspace-level-agents)
7. [What Claygent CAN Do (Capabilities)](#7-what-claygent-can-do-capabilities)
8. [What Claygent CANNOT Do (Limitations)](#8-what-claygent-cannot-do-limitations)
9. [Writing Effective Claygent Prompts](#9-writing-effective-claygent-prompts)
10. [JSON Output Structure in Clay](#10-json-output-structure-in-clay)
11. [Prompt Examples and Templates](#11-prompt-examples-and-templates)
12. [Model Selection Guide](#12-model-selection-guide)
13. [Clay for GTM Workflows](#13-clay-for-gtm-workflows)
14. [Clay + Claude / MCP Integration](#14-clay--claude--mcp-integration)
15. [Pricing and Credits](#15-pricing-and-credits)

---

## 1. What is Clay?

Clay (app.clay.com) is a go-to-market (GTM) data enrichment and workflow automation platform. It is not a standalone lead database — instead it functions as a connector and orchestration layer over 150+ external data providers (Apollo, Clearbit, LinkedIn, etc.), plus its own AI research tools.

**Core value proposition:**
- Pull data from 150+ providers through a single spreadsheet-like interface
- Waterfall enrichment: query multiple providers sequentially, pay only when data is found
- AI-powered research via Claygent for unstructured, custom data points
- Generate personalized outreach copy at scale using AI

**Scale indicators (as of mid-2025):**
- 300,000+ GTM teams use Clay
- Clay reached $100M ARR by end of 2025
- Claygent surpassed 1 billion cumulative runs in June 2025
- 30% of Clay customers use Claygent daily, generating ~500,000 research tasks per day

**Best suited for:** Mid-size to enterprise B2B sales teams, RevOps engineers, GTM engineers, and technical marketers who run sophisticated enrichment and outreach workflows.

**Not ideal for:** Small or non-technical sales teams, customer support automation, or teams needing a single governed enterprise database (ZoomInfo may fit better).

---

## 2. Clay's AI Features Overview

Clay has three distinct AI capabilities:

| Feature | What It Does | Use Case |
|---|---|---|
| **Claygent** | AI web scraper and research agent; browses public websites to extract custom data | Research only — finding publicly visible info on company/people websites |
| **Use AI Column** | Runs GPT, Claude, or Gemini on data already in your table | Copywriting, transforming/cleaning data, classifying records, personalization |
| **Claygent Builder** | Workspace-level agent creation tool for reusable, versioned AI agents | Building shared research agents used across multiple tables |

These are separate but complementary. Claygent goes out to the web to find data. The "Use AI" column operates on data already in your table. The Builder is where you create and manage agents at the workspace level.

---

## 3. Claygent: The AI Research Agent

### What It Is

Claygent is Clay's AI web scraper and research agent, powered by GPT-4 (and optionally Claude Opus or Clay's proprietary Neon/Argon models). It acts like a virtual human researcher: it visits websites, reads pages, extracts targeted information, and returns structured results — at scale.

Unlike a standard data provider that returns results from a static database, Claygent actively browses the web in response to your instructions.

### How It Works Technically

1. User provides a prompt and a starting URL (company domain or LinkedIn profile URL)
2. Claygent uses GPT-4 to infer which section of a website is most likely to contain the needed information (e.g., SOC-2 compliance is usually in the footer)
3. It scrapes only the relevant section rather than the entire page, saving compute
4. NLP processes and structures the extracted content
5. Result is returned to the Clay table column

### Accessing Claygent

1. In a Clay table, click **"Add Enrichment"**
2. Navigate to **Tools → AI**
3. Select **"Web Research (Claygent)"**

---

## 4. Claygent Navigator

Claygent Navigator is Clay's most advanced model, launched in 2025. Inspired by OpenAI's Operator, it goes beyond passive reading to actively interact with web pages.

### What Navigator Can Do That Standard Claygent Cannot

- **Click buttons** and toggle filters on web pages
- **Fill out search forms** on public portals
- **Paginate through results** (click "next page" repeatedly)
- **Navigate dashboards** and apply multi-step filters
- **Process PDFs, XML, and CSV files** embedded in web pages
- **Handle public registries and government databases** (FINRA BrokerCheck, SEC filing search, business license databases)

### How Navigator Works

Navigator combines visual reasoning with GPT-5's deep research capabilities. It executes "multi-hop, multi-source" web research — following a chain of actions across multiple pages. Every run produces a **step-by-step replay** so you can see exactly how it navigated to the answer.

### Navigator vs. Standard Claygent

| Attribute | Standard Claygent (Neon/Argon) | Navigator |
|---|---|---|
| Page interaction | Read only | Click, fill, paginate |
| PDFs | Limited | Yes |
| Government portals | Partial | Yes |
| Cost | 1–3 credits | 6 credits per run |
| Private API keys | Supported | Not currently supported |
| Best for | Website scraping, simple lookups | Multi-step, form-based research |

### Navigator Use Case Examples

- Searching FINRA BrokerCheck by name to verify broker credentials
- Pulling company registrations from state business portals
- Verifying professional licenses from government databases
- Navigating filtered dashboards where data is hidden behind buttons

---

## 5. The "Use AI" Column

Separate from Claygent, the "Use AI" column lets you run AI models (GPT, Claude, or Gemini) directly on data already inside your Clay table.

### Two Modes

**Generate Tab (Recommended for most users):** Describe your task in plain English. Clay automatically constructs an optimized prompt, recommends the best model, and sets up output fields.

**Configure Tab (Advanced):** Full manual control over prompt, model, output schema, and JSON structure.

### What Use AI is Good For

- Writing personalized outreach copy using enriched data in columns
- Classifying records (B2B vs. B2C, ICP fit, etc.)
- Transforming or cleaning data (standardizing job titles, removing noise)
- Summarizing text already scraped into the table
- Extracting structured fields from unstructured text

### Available Models

Clay integrates three model families in Use AI:
- **GPT** (OpenAI — including GPT-4, GPT-4o, GPT-4o-mini)
- **Claude** (Anthropic)
- **Gemini** (Google)

Users can connect personal API keys to reduce costs.

---

## 6. Claygent Builder (Workspace-Level Agents)

The Claygent Builder is a workspace-level tool introduced to enable teams to create, test, version, and share AI agents across multiple tables.

### Key Features

- **Centralized management**: Agents live at the workspace level, not locked to individual tables
- **Free test cases**: First 5 test rows don't consume credits; teams can iterate on prompts at no cost
- **Version control**: Full version history; A/B test multiple versions before publishing
- **Permissions**: Editors can create/modify agents; viewers can reference approved agents in tables

### Creation Workflow

1. Navigate to Claygents → click **"+ Create Agent"**
2. Choose your AI model
3. Draft prompt logic using variables in the editor
4. Add and run test cases to validate functionality
5. Save (version history is automatically captured)

### Example Agent Types Built in the Builder

- ICP qualification agents that score professional profile fit
- Cold email composition agents that research and draft personalized outreach
- Email timing agents that pull Salesforce data and recommend optimal send times

---

## 7. What Claygent CAN Do (Capabilities)

> **Important distinction:** Claygent is a **research-only tool**. It browses a prospect's public website and extracts text that is explicitly written there — nothing more. Think of it as Claude or GPT with a URL. It does **not** pull from databases. Copywriting, classification, and data transformation happen in the **"Use AI" column** (Section 5).

### What Claygent Is Reliably Good At

Claygent excels when the information you need is **explicitly written on the prospect's own website**. Based on real usage, the most reliable use cases are:

- **Product offerings**: What products or services the company sells, how they're described, key features
- **New launches**: Recently announced products, features, or collections visible on their site
- **Pricing and plans**: Pricing tiers, plan names, and pricing model (subscription, one-time, custom) if publicly listed
- **Return and refund policies**: Exact policy language for use in competitive or qualification research
- **About / mission / values**: Company story, founding context, stated mission, core values
- **Target customer description**: Who they say they serve (industries, company sizes, roles mentioned on the site)
- **Case studies and customer logos**: Publicly displayed customer names and the outcomes described
- **FAQs and support content**: Common questions, onboarding info, product limitations they disclose publicly

### What Claygent CANNOT Reliably Do

| Data Point | Why It Fails | What to Use Instead |
|---|---|---|
| **Funding / investor data** | Not written on company websites. Private companies especially have nothing. | Clay's Crunchbase or PitchBook enrichment columns |
| **Tech stack** | Companies don't list their internal tools on their website. Careers pages are often blocked or JS-gated. | Clay's BuiltWith or Datanyze enrichment columns |
| **News and trigger events** | Many newsrooms are JS-rendered (appear blank to scrapers) or don't exist. Third-party news coverage is not on the company's own site. | Clay's news enrichment providers (e.g., Diffbot, NewsAPI) |
| **Job openings** | Careers pages are frequently 403-blocked or require JavaScript to render. | Clay's LinkedIn Jobs enrichment columns |
| **Competitive intelligence** | Companies never name competitors on their own website. | Manual research or third-party review sites |

### First-Party Data + MCP Connections

- Connect Claygent to MCP servers for your own private data: Gong transcripts, Salesforce opportunities, Google Docs
- This is the only way to bring non-public context into a Claygent prompt

---

## 8. What Claygent CANNOT Do (Limitations)

### Hard Technical Limitations

- **No access to paywalled or gated content**: Cannot retrieve information behind login walls, subscriptions, or authentication barriers
- **No access to private data**: Cannot access internal company documents, CRM data, or private communications unless explicitly connected via MCP
- **No persistent memory across rows**: Each row execution is fully independent; Claygent does not build context from previous lookups
- **No real-time verification**: Results are based on what's currently publicly visible but Claygent cannot confirm information is current as of today
- **Standard Claygent cannot interact with web pages**: Can only read, not click, scroll, or fill forms (Navigator model required for this)

### Accuracy and Quality Limitations

- **Hallucinations are possible**: AI interpretation of unstructured content can produce fabricated or incorrect answers; accuracy is not guaranteed
- **Accuracy varies by source type**: Structured sources (LinkedIn, directories) yield higher accuracy; unstructured content (blog posts, PDFs) introduces more variance
- **Data freshness gaps**: If a company website or LinkedIn profile hasn't been updated recently, Claygent will return stale information
- **Industry/regional variance**: Accuracy and data availability vary significantly by industry, company size, and geography
- **No published accuracy/hallucination baseline**: Clay does not publish universal hit rates; expect significant variance

### Scope and Strategic Limitations

- **Research tool, not strategy tool**: Claygent finds information; it does not interpret what that information means for your GTM motion
- **Not a customer support tool**: Cannot integrate with Zendesk, Confluence, Slack, or other support knowledge bases
- **Not a full-scale outreach platform**: Does not send emails or manage sequences natively
- **Anti-bot and rate limits**: Some websites block scraping; complex sites may cause timeouts or failures

### Cost and Operational Limitations

- **Credit consumption is high for complex tasks**: Multi-step AI workflows can consume 6–25 credits per row
- **Failed lookups still cost credits** in some configurations
- **Significant learning curve**: Requires understanding of conditional logic, prompt engineering, and workflow architecture
- **Not designed for non-technical users**: Built for GTM engineers and RevOps professionals, not frontline sales reps

---

## 9. Writing Effective Claygent Prompts

### The S.P.I.C.E. Framework

Clay recommends structuring prompts using five components, separated by section headers with hashtags:

```
#VARIABLES#
{variable_name} = [mapped column]

#CONTEXT#
Background information that focuses the AI on what you're trying to accomplish.

#INSTRUCTIONS#
Step-by-step directions for what the agent should do.

#EXAMPLES#
Sample input → output pairs demonstrating the exact format you want.

#OUTPUT#
Specification of the exact format and structure of the response.
```

**S** = **Sections** — Structural components separated by `#HASHTAGS#`
**P** = **Prompt variables** — Placeholders in `{curly_brackets}` referencing table columns
**I** = **Instructions** — Step-by-step directions
**C** = **Context** — Background information focusing the AI
**E** = **Examples** — Sample outputs showing desired format (few-shot prompting)

### Core Prompt Writing Rules

**1. Use second-person language directed at the agent**
```
Good: "Visit this company's website at {company_website} and find..."
Bad:  "Find the pricing page"
```

**2. Be specific about where to look**
```
Good: "Visit {company_website}/pricing and look for the highest-tier plan price"
Bad:  "What is this company's price?"
```

**3. Provide fallback logic**
```
"If no pricing page exists, check for a 'Contact us for pricing' message and return 'Custom pricing only'"
"If the company has not posted recently, summarize their LinkedIn About section instead"
```

**4. Constrain output length and format**
```
"Keep output under 50 words"
"Return only a number, no words"
"Return only 'true' or 'false', no other output"
```

**5. Include examples (few-shot prompting)**
For specialized or structured outputs, provide 2–3 input → output examples inside `#EXAMPLES#`. This dramatically improves consistency for downstream use in emails and other workflows.

**6. Use `{variable}` syntax for dynamic inputs**
Map column values directly into your prompt:
```
"Visit {company_website} and find whether they mention {competitor_name} as a tool they use."
```

**7. Specify timeframes when relevant**
```
"Find any funding announcements from the past 6 months"
"Only consider job postings created in the last 30 days"
```

**8. Set explicit output format constraints**
```
"Output format: $[price] per [month/year]"
"Return as a comma-separated list of up to 3 job titles. Do not include numbers or extra text."
"Return only 'B2B' or 'B2C'. No other output is acceptable."
```

### The PORT Framework (Alternative to S.P.I.C.E.)

Some Clay practitioners use PORT for copy-generation prompts:
- **P** = Persona (who the AI is writing as)
- **O** = Objective (what the message needs to accomplish)
- **R** = Rules (constraints: tone, word count, what to avoid)
- **T** = Template (the exact template or format to fill in)

### Using the "Help Me" Button

Inside Clay's Claygent prompt editor, the **"Help me"** button auto-generates an optimized prompt based on a plain-English description of your task. Use this as a starting point, then refine with the S.P.I.C.E. framework.

### Testing Before Scaling

Always use **Test Run** on 3–10 rows before running on your full dataset. The Claygent Builder provides free test cases for prompt iteration. This avoids wasting credits on misconfigured prompts.

---

## 10. JSON Output Structure in Clay

### How Clay Handles JSON

Claygent **does not natively return true JSON objects** — it returns text that is structured in JSON format. To work with proper parsed JSON:

1. Have Claygent return text structured as JSON
2. Add a second "Use AI" column (using GPT-4o-mini with JSON mode enabled)
3. Prompt that column to take the Claygent output and return it as a proper JSON object

Alternatively, in the **Claygent Builder** and **"Use AI" Configure tab**, you can define a JSON Schema that Clay will use with OpenAI's Structured Outputs to enforce the format directly.

### Clay's JSON Schema Rules (OpenAI Structured Outputs)

Clay uses OpenAI Structured Outputs with stricter requirements than standard JSON Schema. Violating these rules causes silent failures or malformed output.

**The 8 Critical Rules:**

**Rule 1: Root must be an object**
```json
{ "type": "object" }  // Correct
// Arrays at root level are NOT allowed
```

**Rule 2: No validation keywords**
Prohibited: `minLength`, `maxLength`, `minimum`, `maximum`, `pattern`, `format`, `const`, `default`

**Rule 3: Every object must have `additionalProperties: false`**
```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": { ... }
}
```

**Rule 4: Nullable fields use `anyOf` with null**
```json
"website": {
  "anyOf": [
    { "type": "string" },
    { "type": "null" }
  ]
}
```

**Rule 5: ALL properties must be listed in `required` array**
Use `anyOf` with `null` (Rule 4) to make a field optional while still including it in `required`.

**Rule 6: Only `anyOf` is permitted — no `oneOf`, `allOf`, or `not`**

**Rule 7: Use enums for fixed/categorical values**
```json
"business_model": {
  "type": "string",
  "enum": ["B2B", "B2C", "B2B2C"]
}
```
Enums enforce canonical values, enabling reliable downstream filtering.

**Rule 8: Arrays must define their `items` schema**
```json
"technologies": {
  "type": "array",
  "items": { "type": "string" }
}
```

### Full Example: Valid Clay JSON Schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["company_name", "funding_amount", "business_model", "is_saas", "technologies"],
  "properties": {
    "company_name": {
      "type": "string"
    },
    "funding_amount": {
      "anyOf": [
        { "type": "string" },
        { "type": "null" }
      ]
    },
    "business_model": {
      "type": "string",
      "enum": ["B2B", "B2C", "B2B2C", "unknown"]
    },
    "is_saas": {
      "type": "boolean"
    },
    "technologies": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

### Common JSON Mistakes to Avoid

| Problem | Solution |
|---|---|
| Using `"format": "email"` or `"format": "uri"` | Remove `format`, use `"type": "string"` only |
| Optional fields missing from `required` array | Add to `required`, use `anyOf` with `null` |
| Missing `additionalProperties: false` on nested objects | Add to every object in the schema |
| Root-level array | Wrap in an object property (e.g., `"results": { "type": "array", ... }`) |
| Keys without double quotes | Ensure all keys use `"double_quotes"` |
| Trailing commas in objects or arrays | Remove all trailing commas |

### Defining Column Outputs (Non-JSON)

For simpler outputs, use Clay's column output types:
- **Text** — Names, descriptions, summaries
- **Number** — Financial figures (enables sorting and calculation)
- **URL** — Clickable links
- **True/False** — Boolean signals
- **Custom** — Specialized format requirements

Both defining column outputs AND telling Claygent in the prompt which value goes where are required. Defining the column alone is not sufficient.

---

## 11. Prompt Examples and Templates

### Research Prompts

**Company Mission (for personalized outreach):**
```
What is the mission of the company using this input: '{Social Media Company Description}'
Be specific and use keywords in the description not normally found in other companies.
Keep the output under 6 words and make it conversational.
Complete this prompt: 'I was on your company page and it looks like you're focused on...'
```

**Funding Round Summary:**
```
Visit {company_website} and search for recent press releases or news pages.
Find any funding announcements from the past 12 months.
Return: funding amount, round type (Seed/Series A/etc.), and a one-sentence summary of what the funds will be used for.
If no funding information is found, return 'No recent funding found'.
```

**Technology Stack Detection:**
```
Visit {company_website} and their job postings page.
Identify all software tools and technologies mentioned across their job postings.
Return a comma-separated list of up to 8 specific tools (e.g., Salesforce, HubSpot, Snowflake).
Do not include generic terms like 'CRM' — only specific product names.
```

**Pain Point from Job Posting:**
```
Tell me what problem this company is trying to solve based on this open job listing: {job_title}
Keep it short and be specific based on what that job title is known to do.
Complete this prompt: 'I saw your company was hiring for a {job_title}. In my experience this means you're trying to improve your company's'
```

**B2B vs. B2C Classification:**
```
A B2B company sells to other companies. A B2C company sells to consumers.
Using this input: {company_description}
Is this company a B2B or B2C company?
Return ONLY 'B2B' or 'B2C'. No other output is acceptable.
```

**SaaS Identification:**
```
Is the company in this input a SaaS company?
A SaaS company offers software for a monthly or annual subscription to multiple users.
Input: {company_description}
Return ONLY 'true' if it is a SaaS company, or 'false' if it is not.
```

**ICP Qualification (Boolean):**
```
Visit {company_website}.
Does this company sell primarily to enterprise customers (500+ employees)?
Look for case studies, customer logos, or pricing that indicates enterprise focus.
Return ONLY 'true' or 'false'. If unclear, return 'false'.
```

### People/Contact Prompts

**LinkedIn Role Summary (for personalized outreach):**
```
Tell me what this person focuses on based on their title and LinkedIn summary.
Title: {job_title}
LinkedIn summary: {linkedin_summary}
Be specific and casual. Complete this prompt in under 6 words:
'As the {job_title}, I'd imagine you focus on'
```

**Buyer Personas from Company Description:**
```
What job titles does this company sell to, based on this description: {company_description}
Who gets the most value from their product? What are their typical job titles?
Return up to 3 job titles as a comma-separated list.
No numbers, no extra information. Just the titles.
```

**Job Title Cleaning:**
```
Clean this job title from unimportant information.
People sometimes list two titles, add 'we're hiring', or place seniority oddly.
Keep only the core job title.
Input: {raw_job_title}
```

### Copywriting Prompts

**News Article Opener:**
```
Using this headline, complete my sentence using keywords specific to the article.
Compliment them on the findings. Keep it very short and casual. No corporate jargon.
Shorten company names where applicable. No reference to when the article was published.
Headline: {news_headline}
Complete this: 'I saw the recent news article about'
```

**Social Post Opener:**
```
Use this LinkedIn post to complete my sentence in under 8 words.
Be specific and use keywords from the post.
Post: {linkedin_post}
Complete this: 'I just wanted to reach out because I saw your post about'
```

**Personalized Value Prop:**
```
#CONTEXT#
You are a sales rep at {our_company}. We help {ICP_description} with {value_proposition}.

#INSTRUCTIONS#
Based on the prospect's company description and recent news, write a 1-2 sentence personalized value prop.
Explain specifically why {our_company} is relevant to their current situation.
Reference: {company_description} and {recent_news_headline}.

#RULES#
- Maximum 40 words
- No corporate jargon
- First person ("I noticed..." not "Our research shows...")
- No placeholder brackets in the output

#OUTPUT#
One sentence only. Conversational tone.
```

---

## 12. Model Selection Guide

### Clay's Native Models

| Model | Credit Cost | Best For | Accuracy |
|---|---|---|---|
| **Helium** | ~$0.03/row | Simple lookups, budget-sensitive runs | ~50% on complex queries |
| **Neon** | ~$0.07/row | Data extraction, formatting, multi-column outputs | High for structured data |
| **Argon** | ~$0.10/row | Complex analysis requiring highest accuracy | ~100% on complex queries |
| **Navigator** | 6 credits/run | Multi-step, form-based, interactive web research | Highest for interactive sites |

### Third-Party Models (Available via API Key)

| Model | Best For |
|---|---|
| **GPT-4 / GPT-4o** | Deep reasoning, complex analysis |
| **Claude Opus (Anthropic)** | Long-context reasoning, nuanced interpretation |
| **GPT-4o-mini** | JSON mode, cost-efficient structured output transformation |
| **Gemini** | Available in Use AI column for general tasks |

### Selection Guidance

- **1-credit equivalent (Helium)**: Simple yes/no questions, basic classifications
- **2-credit equivalent (Neon)**: Moderate complexity, extracting named data points, multi-column outputs
- **3-credit equivalent (Argon)**: Complex analysis requiring multiple data points or reasoning
- **6 credits (Navigator)**: Any task requiring form fills, clicks, pagination, or interactive web navigation
- **Use GPT-4/Claude for "Use AI" column**: When running copy generation or reasoning on data already in your table

**Best practice**: Start with lighter models for initial runs; escalate to Argon/Navigator only when needed. Always test on 3–5 rows before scaling.

---

## 13. Clay for GTM Workflows

### The Core GTM Workflow Architecture

```
Data Sources → Enrichment (Waterfall) → AI Research (Claygent) → Qualification (AI scoring) → Personalization (Use AI) → Outreach Sequences
```

**Step 1: Build the list**
Pull leads from Clay's 150+ integrations (Apollo, LinkedIn Sales Navigator, Crunchbase, etc.) or import a CSV.

**Step 2: Waterfall enrichment**
Use multiple providers sequentially. Clay tries Provider 1 → if no data, tries Provider 2 → etc. You pay only when data is found. This dramatically increases coverage vs. using a single provider.

**Step 3: Claygent research**
Add custom research columns for data points no structured provider has:
- Technology stack from job postings
- Recent funding details
- ICP qualification signals
- Competitive intelligence

**Step 4: AI qualification**
Use a "Use AI" column to score each row against your ICP criteria. Generate a fit score, tier (A/B/C), or disqualification reason.

**Step 5: AI personalization**
Generate modular "AI snippets" for each prospect:
- Funding-based opener
- Role-based value prop
- News-based conversation starter
Combine snippets into a full email via a formula column.

**Step 6: Push to sequencer**
Export or sync enriched + personalized records to your outreach tool (Salesloft, Outreach, Instantly, Apollo sequences, etc.).

### Waterfall Enrichment Detail

The waterfall engine queries providers in a defined order:
- If Provider 1 returns the field → stops there, charges 1 credit
- If Provider 1 fails → tries Provider 2 → etc.
- Terminates on first success
- Purpose: maximize hit rate while minimizing cost

Results from this approach:
- Anthropic tripled their enrichment rate vs. previous solution
- OpenAI went from ~40% enrichment coverage to ~80%+ using Clay's waterfall

### Trigger-Based Workflows

Clay can be set up to respond to trigger events:
- New hire or leadership change at a target account → auto-enrich + add to sequence
- New funding round detected → generate funding-specific outreach
- New job posting → infer pain point → create relevant outreach
- Company appears in news → generate news-based opener

### Personalized Content Strategy: Modular AI Snippets

Rather than basic `{{company_name}}` substitution, Clay's approach to personalization uses full AI-generated sentences per prospect:

1. Create a "funding snippet" column: AI generates "I saw you raised your $50M Series C to expand into enterprise"
2. Create a "pain snippet" column: AI generates "with a new VP of Sales coming on board, I imagine you're focused on building pipeline process"
3. Combine with a formula: `=[Subject Line] & " " & [Funding Snippet] & " " & [Pain Snippet] & " " & [CTA]`

This produces genuinely personalized copy at scale while maintaining message quality.

---

## 14. Clay + Claude / MCP Integration

### Clay's Official MCP Server

Clay has built an official MCP (Model Context Protocol) server that connects Clay's prospecting and enrichment capabilities directly into AI environments like Claude.

**What this enables:**
- Use Clay's 150+ data providers as native tool calls within Claude Code sessions
- Enrich records, research prospects, and run Claygent lookups from inside Claude's chat interface
- For agentic workflows: Clay enrichment becomes a callable API within Claude's agentic loop — no context switching required

### Clay as a Claude MCP App (January 2026)

In January 2026, Clay was included in Anthropic's initial launch of "MCP Apps" — a feature enabling MCP servers to render interactive UIs directly inside Claude's interface. Sales teams can:
- View and interact with Clay tables inside Claude
- Draft outreach materials using enriched Clay data without leaving Claude
- Trigger Clay workflows from within a Claude conversation

### Claygent + First-Party MCP Connections

Within Clay itself, Claygent can connect to any MCP server to enrich research with private, internal context:
- **Gong**: Pull call transcript summaries and talking points into Claygent research context
- **Salesforce**: Reference opportunity history, deal stage, and account data in AI prompts
- **Google Docs / Custom Documents**: Ground Claygent in internal positioning docs, personas, or battlecards

This bridges the gap between public web research and private business context.

---

## 15. Pricing and Credits

### Pricing Tiers (as of 2025)

| Plan | Monthly Price | Credits |
|---|---|---|
| Free | $0 | 100 credits |
| Starter | $149/month | 2,000 credits |
| Explorer | $349/month | 10,000 credits |
| Pro | $800/month | 50,000 credits |
| Enterprise | Custom | Custom |

### Credit Consumption Guide

| Action | Credit Cost |
|---|---|
| Basic data enrichment (single provider) | 1 credit |
| Claygent Helium | ~1–2 credits |
| Claygent Neon | ~2 credits |
| Claygent Argon | ~3 credits |
| Claygent Navigator | 6 credits |
| Multi-step AI workflow | Up to 25 credits |
| Failed lookups | May still consume credits |

### Cost Management Best Practices

- Test on 3–5 rows before scaling to full dataset
- Use lighter models first; escalate only when needed
- Use waterfall enrichment to avoid re-querying expensive providers
- Set clear output constraints to reduce token usage
- Use the Claygent Builder's free test cases for prompt iteration
- Monitor credit burn rate when running broad workflow parameters

---

## Key Takeaways for Prompt Writers

1. **Always assign more than three tasks per Claygent.** Each Claygent run costs credits — maximize value by combining multiple research tasks into a single agent call. For example, one prompt can simultaneously extract product offerings, pricing model, target customer description, and return policy in a single structured JSON output.

2. **Claygent is research-only. Copywriting is "Use AI".** Claygent browses public websites and extracts what's visible — the same as Claude or GPT with a URL. It does not write copy. Copy generation, classification, and data transformation all happen in the "Use AI" column using data already in your table.

3. **Claygent is not a structured database connector.** Funding data (Crunchbase), tech stack (BuiltWith), and job postings (LinkedIn) are available via Clay's separate enrichment integrations — not through Claygent. Claygent only finds what is explicitly written on a company's public website, which is highly variable by brand.

4. **The S.P.I.C.E. framework** (Sections, Prompt variables, Instructions, Context, Examples) is the recommended structure for professional-grade Claygent prompts.

5. **Few-shot examples dramatically improve consistency.** For any prompt where output format matters (especially for downstream email assembly), include 2–3 input → output examples.

6. **Always include fallback instructions.** "If X is not found, return Y" prevents empty cells and downstream errors.

7. **Constrain your output aggressively.** Word limits, specific formats, enum values, and explicit instructions like "Return ONLY 'true' or 'false'" are essential for reliable, filterable data.

8. **JSON in Clay has strict rules.** Root must be an object, `additionalProperties: false` is required on every object, all properties must be in `required`, nullable fields use `anyOf`, and no validation keywords are allowed.

9. **Validate before scaling.** Sample results manually before using AI-generated data in customer-facing communications. Hallucinations are possible.

10. **Navigator for interactive tasks.** If the data you need is behind a search form, requires clicking through pages, or lives in a government portal, use Navigator (6 credits) rather than standard Claygent.

---

*Sources: Clay.com, Clay University (university.clay.com), Clay Community Forums, ColdIQ, Databar, Octave, AutoClaygent, utmost.agency, databar.ai, eesel.ai, OpenAI Case Study, and Clay GTM Engineering Substack.*
