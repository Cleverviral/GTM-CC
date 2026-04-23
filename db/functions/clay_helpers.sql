-- ============================================================================
-- Clay → Neon derivation helpers
-- ----------------------------------------------------------------------------
-- Three immutable helper functions used by upsert_lead() to auto-derive
-- common lead fields when the operator doesn't provide them explicitly.
-- Ported from the behavior of Supabase's upsert_contact RPC.
--
--   is_personal_email_domain(email) → boolean
--   normalize_company_domain(website) → text
--   extract_linkedin_username(profile_url) → text
-- ============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
-- is_personal_email_domain
-- Returns TRUE if the email's domain is a known personal-email provider.
-- Returns NULL if the email is NULL or malformed (no @).
--
-- Examples:
--   is_personal_email_domain('sarah@gmail.com')  → true
--   is_personal_email_domain('sarah@stripe.com') → false
--   is_personal_email_domain(NULL)               → NULL
--   is_personal_email_domain('invalid')          → NULL
-- ─────────────────────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION public.is_personal_email_domain(email_input text)
RETURNS boolean
LANGUAGE sql IMMUTABLE
AS $$
    SELECT CASE
        WHEN email_input IS NULL OR email_input = '' THEN NULL
        WHEN POSITION('@' IN email_input) = 0 THEN NULL
        ELSE LOWER(SPLIT_PART(email_input, '@', 2)) = ANY(ARRAY[
            'gmail.com', 'googlemail.com',
            'yahoo.com', 'yahoo.co.uk', 'yahoo.ca', 'yahoo.co.in', 'yahoo.in',
            'yahoo.fr', 'yahoo.de', 'yahoo.it', 'yahoo.es', 'yahoo.com.br',
            'yahoo.com.mx', 'yahoo.com.au', 'ymail.com', 'rocketmail.com',
            'hotmail.com', 'hotmail.co.uk', 'hotmail.fr', 'hotmail.de',
            'hotmail.it', 'hotmail.es', 'hotmail.com.br',
            'outlook.com', 'outlook.fr', 'outlook.de', 'outlook.com.br',
            'live.com', 'live.co.uk', 'msn.com',
            'icloud.com', 'me.com', 'mac.com',
            'aol.com', 'aim.com',
            'protonmail.com', 'proton.me', 'pm.me',
            'gmx.com', 'gmx.net', 'gmx.de', 'gmx.co.uk',
            'mail.com',
            'zoho.com', 'zohomail.com',
            'yandex.com', 'yandex.ru',
            'fastmail.com', 'fastmail.fm',
            'tutanota.com',
            'hey.com',
            'rediffmail.com',
            'qq.com', '163.com', '126.com', 'sina.com', 'sohu.com',
            'naver.com', 'daum.net',
            'duck.com', 'duckduckgo.com'
        ])
    END
$$;


-- ─────────────────────────────────────────────────────────────────────────────
-- normalize_company_domain
-- Strips protocol (http/https), www., and path/query/fragment from a
-- company website URL, returning the bare lowercase domain.
--
-- Examples:
--   normalize_company_domain('https://www.Club-Med.com/Path/page?q=x') → 'club-med.com'
--   normalize_company_domain('stripe.com')                             → 'stripe.com'
--   normalize_company_domain('http://www.example.com')                 → 'example.com'
--   normalize_company_domain(NULL)                                     → NULL
--   normalize_company_domain('')                                       → NULL
-- ─────────────────────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION public.normalize_company_domain(website text)
RETURNS text
LANGUAGE sql IMMUTABLE
AS $$
    SELECT CASE
        WHEN website IS NULL OR TRIM(website) = '' THEN NULL
        ELSE NULLIF(
            LOWER(
                REGEXP_REPLACE(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(TRIM(website), '^https?://', '', 'i'),
                        '^www\.', '', 'i'
                    ),
                    '[/:?#].*$', ''
                )
            ),
            ''
        )
    END
$$;


-- ─────────────────────────────────────────────────────────────────────────────
-- extract_linkedin_username
-- Extracts the lowercase LinkedIn username (the part after /in/) from a
-- LinkedIn profile URL. Returns NULL if the URL doesn't contain /in/.
--
-- Examples:
--   extract_linkedin_username('http://linkedin.com/in/QuentinBriard/')             → 'quentinbriard'
--   extract_linkedin_username('https://linkedin.com/in/jane-doe-123abc?utm=x')    → 'jane-doe-123abc'
--   extract_linkedin_username('http://linkedin.com/company/stripe')                → NULL
--   extract_linkedin_username(NULL)                                                → NULL
-- ─────────────────────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION public.extract_linkedin_username(profile_url text)
RETURNS text
LANGUAGE sql IMMUTABLE
AS $$
    SELECT CASE
        WHEN profile_url IS NULL OR TRIM(profile_url) = '' THEN NULL
        WHEN profile_url !~* '/in/' THEN NULL
        ELSE NULLIF(
            LOWER(
                REGEXP_REPLACE(
                    REGEXP_REPLACE(profile_url, '^.*/in/', '', 'i'),
                    '[/?#].*$', ''
                )
            ),
            ''
        )
    END
$$;
