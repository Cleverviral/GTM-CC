# Add Leads to a Segment

Guide the Clay Operator (or Copy Strategist) through adding new leads to the database from a CSV file.

**ROLE CHECK:** This command is for the Clay Operator and Copy Strategist. If the current role is Campaign Operator, say: "This command is for the Clay Operator or Copy Strategist only."

## Step 1: Identify Client + Segment

```python
import sys; sys.path.insert(0, 'scripts')
from db import read_query

clients = read_query("SELECT client_id, client_name FROM clients WHERE client_status = 'active' LIMIT 50")
```

Show numbered list. After client selection:

```python
segments = read_query("SELECT segment_id, segment_name, segment_tag, status FROM segments WHERE client_id = $1 LIMIT 50", [str(client_id)])
```

Show segments. Ask:
> **Which segment should these leads be added to?**
> (Or type "new" to create a new segment — Copy Strategist only)

If "new" and role is Clay Operator, say: "Creating segments is a Copy Strategist task."

## Step 2: Accept the CSV

Ask:
> **Drop your CSV file or paste the file path.**
> The only required column is **email**. Everything else is optional.
> Column names don't need to match exactly — I'll auto-map them for you.

Read the CSV file. Parse the headers.

## Step 3: Auto-Map Columns

Map CSV headers to DB columns using fuzzy matching. The mapping rules:

### Recognized DB columns (map these automatically):
| DB Column | Accepted CSV Headers (case-insensitive) |
|-----------|----------------------------------------|
| email | email, email_address, e-mail, mail |
| first_name | first_name, firstname, first name, given_name |
| last_name | last_name, lastname, last name, surname, family_name |
| full_name | full_name, fullname, full name, name |
| job_title | job_title, title, jobtitle, job title, position, role |
| linkedin_profile_url | linkedin_profile_url, linkedin, linkedin_url, linkedin url, profile_url |
| company_name | company_name, company, companyname, company name, organization |
| company_domain | company_domain, domain, companydomain, company domain, website_domain |
| company_website | company_website, website, companywebsite, company website, url |
| industry | industry, sector |
| monthly_visits | monthly_visits, monthlyvisits, monthly visits, traffic, visits |
| employee_count | employee_count, employeecount, employees, employee count, company_size, headcount |

### Columns that NEVER get auto-mapped (operator chooses):
- Any unrecognized column → offer: "Skip" or "Store in extra_data as '{key_name}'"

### Show the mapping for confirmation:

> **Column Mapping:**
> | CSV Column | → DB Field | Status |
> |------------|-----------|--------|
> | Email Address | → email | ✓ Required |
> | First Name | → first_name | ✓ Mapped |
> | Company | → company_name | ✓ Mapped |
> | Revenue | → extra_data.revenue | ⚠ Custom field |
> | Notes | → SKIP | ✗ Skipped |
>
> **Does this mapping look correct?** (yes / adjust)

If `email` is not found in the CSV, STOP:
> **Error:** No email column found in your CSV. The CSV must have an email column. Check your headers and try again.

## Step 4: Dedup Check

Before inserting, check for existing leads:

```python
# Extract all emails from CSV
csv_emails = [row['email'].strip().lower() for row in csv_data if row.get('email')]

# Check which already exist in DB
existing = read_query("""
    SELECT lead_id, email, segment_ids
    FROM leads
    WHERE LOWER(email) = ANY($1)
""", [csv_emails])
```

Categorize and show:

> **Dedup Results:**
> - **{new_count} new leads** — will be INSERTED
> - **{existing_in_segment} already in this segment** — will be SKIPPED (no duplicates)
> - **{existing_other_segment} exist in DB but NOT in this segment** — segment will be ADDED to their segment_ids[]
> - **{no_email} rows with empty email** — will be SKIPPED
>
> **Total rows to process: {actionable_count}**
> Proceed? (yes / no)

## Step 5: Execute

### For NEW leads (INSERT):
```sql
INSERT INTO leads (email, first_name, last_name, full_name, job_title,
    linkedin_profile_url, company_name, company_domain, company_website,
    industry, monthly_visits, employee_count, segment_ids, extra_data)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
    ARRAY[$13]::int[], $14::jsonb)
```

- `segment_ids` starts as `ARRAY[{segment_id}]`
- `extra_data` is built from any custom-mapped columns as a JSONB object
- Empty strings → NULL (never store empty strings)

### For EXISTING leads (not in this segment — UPDATE):
```sql
UPDATE leads
SET segment_ids = array_append(segment_ids, $1)
WHERE lead_id = $2 AND NOT ($1 = ANY(segment_ids))
```

- Only APPENDS the segment_id — never removes existing segment_ids
- Never overwrites existing lead data with empty values from the CSV

### For EXISTING leads (already in this segment):
- SKIP entirely — no action needed

### Processing:
- Process in batches of 100
- Show progress every 100 rows
- Use `write_query()` with confirmation for the first batch, then auto-confirm remaining

## Step 6: Summary

> **Import Complete!**
> - New leads added: {inserted}
> - Existing leads added to segment: {updated}
> - Already in segment (skipped): {skipped}
> - Errors: {errors}
>
> **Segment "{segment_name}" now has {total_count} leads.**
>
> **Next steps:**
> - Run `/pull-leads` to verify the imported data
> - Use `/push-to-clay` when ready to enrich and generate emails

## Guard Rails

1. **email is mandatory** — reject any CSV without an email column
2. **Dedup by email** (case-insensitive LOWER()) — never create duplicate lead rows
3. **Never overwrite existing data with empty values** — if a lead exists and the CSV has an empty first_name, keep the existing first_name
4. **segment_ids is append-only** — never remove existing segment associations
5. **Max 500 rows per batch** — if CSV has more than 500 rows, process in batches of 500 with confirmation between batches
6. **extra_data keys use snake_case** — auto-convert "Revenue Range" → "revenue_range"
7. **Show the full dedup report before any writes** — operator must confirm
8. **No enrichment happens here** — this is just data import. Enrichment happens in Clay after `/push-to-clay`
