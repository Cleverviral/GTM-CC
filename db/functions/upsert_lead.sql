-- ============================================================================
-- upsert_lead(...) → jsonb
-- ----------------------------------------------------------------------------
-- The single Postgres function that Clay calls to push lead enrichment and
-- generated email outputs back into the TAM + Recipe DB.
--
-- One function, one HTTP endpoint, one body template — used across every
-- Clay table. Schema changes are made HERE (in this file) and propagate to
-- every Clay table automatically.
--
-- Required parameters:
--   p_email         text   — primary dedup key, lowercased + trimmed
--   p_segment_ids   text   — comma-separated segment_id ints (e.g. "54" or "54,28,37")
--                            First segment is the "primary" — used for email_outputs.segment_id
--
-- All other parameters are optional. Empty strings, NULLs, and Clay's
-- "CLAYFORMATVALUE(...)" placeholders are normalized to NULL by clay_clean().
--
-- Side effects:
--   1. Upserts a row in `leads` (INSERT new email, or UPDATE existing — never
--      overwrites existing non-null with null; arrays unioned; jsonb merged).
--   2. If any p_email_*_variant_* is non-null, ALSO inserts a new row in
--      `email_outputs` linked to the lead, primary segment, recipe, etc.
--      Email outputs are append-only (every push creates a new row).
--
-- Returns: { lead_id, lead_action, segment_ids_applied, output_id }
--
-- Example call (from Clay's HTTP column body via Neon SQL-over-HTTP):
--   SELECT upsert_lead(
--     p_email := 'sarah@stripe.com',
--     p_segment_ids := '54',
--     p_first_name := 'Sarah',
--     p_company_name := 'Stripe',
--     p_extra_data_pairs := 'product_category|fintech;aov|420',
--     p_recipe_id := 51,
--     p_recipe_version := 1,
--     p_email_1_variant_a := 'Sarah, your checkout drop-off ...'
--   );
--
-- Depends on: clay_clean() — see clay_clean.sql
-- ============================================================================

CREATE OR REPLACE FUNCTION public.upsert_lead(
    p_email text,
    p_segment_ids text,
    p_first_name text DEFAULT NULL,
    p_last_name text DEFAULT NULL,
    p_full_name text DEFAULT NULL,
    p_job_title text DEFAULT NULL,
    p_linkedin_profile_url text DEFAULT NULL,
    p_linkedin_username text DEFAULT NULL,
    p_company_name text DEFAULT NULL,
    p_company_domain text DEFAULT NULL,
    p_company_website text DEFAULT NULL,
    p_company_linkedin_url text DEFAULT NULL,
    p_industry text DEFAULT NULL,
    p_monthly_visits integer DEFAULT NULL,
    p_employee_count text DEFAULT NULL,
    p_email_verified text DEFAULT NULL,
    p_email_verified_at text DEFAULT NULL,        -- accepts text; safely parsed to timestamptz
    p_mx_provider text DEFAULT NULL,
    p_has_email_security_gateway text DEFAULT NULL,
    p_is_catchall text DEFAULT NULL,
    p_is_personal_email boolean DEFAULT NULL,
    p_city text DEFAULT NULL,
    p_country text DEFAULT NULL,
    p_info_tags text DEFAULT NULL,                -- comma-separated, parsed to text[]
    p_extra_data_pairs text DEFAULT NULL,         -- pipe format: "key1|val1;key2|val2"
    p_recipe_id integer DEFAULT NULL,
    p_recipe_version integer DEFAULT NULL,
    p_selected_approach text DEFAULT NULL,
    p_batch_id text DEFAULT NULL,
    p_email_1_variant_a text DEFAULT NULL,
    p_email_1_variant_b text DEFAULT NULL,
    p_email_2_variant_a text DEFAULT NULL,
    p_email_2_variant_b text DEFAULT NULL,
    p_email_3_variant_a text DEFAULT NULL,
    p_email_3_variant_b text DEFAULT NULL,
    p_company_summary text DEFAULT NULL,
    p_personalizations_pairs text DEFAULT NULL    -- pipe format: "key1|val1;key2|val2"
)
RETURNS jsonb
LANGUAGE plpgsql
AS $function$
DECLARE
    v_email text;
    v_segment_ids_array int[];
    v_primary_segment_id int;
    v_info_tags_array text[];
    v_extra_data jsonb := '{}'::jsonb;
    v_personalizations jsonb := '{}'::jsonb;
    v_lead_id int;
    v_inserted boolean;
    v_client_id uuid;
    v_output_id int;
    v_has_email_output boolean;
    v_unknown_segments int[];
    v_email_verified_at_ts timestamptz := NULL;
    -- Cleaned versions of every text input (Clay placeholders → NULL)
    v_first_name text := clay_clean(p_first_name);
    v_last_name text := clay_clean(p_last_name);
    v_full_name text := clay_clean(p_full_name);
    v_job_title text := clay_clean(p_job_title);
    v_linkedin_profile_url text := clay_clean(p_linkedin_profile_url);
    v_linkedin_username text := clay_clean(p_linkedin_username);
    v_company_name text := clay_clean(p_company_name);
    v_company_domain text := clay_clean(p_company_domain);
    v_company_website text := clay_clean(p_company_website);
    v_company_linkedin_url text := clay_clean(p_company_linkedin_url);
    v_industry text := clay_clean(p_industry);
    v_employee_count text := clay_clean(p_employee_count);
    v_email_verified text := clay_clean(p_email_verified);
    v_mx_provider text := clay_clean(p_mx_provider);
    v_has_email_security_gateway text := clay_clean(p_has_email_security_gateway);
    v_is_catchall text := clay_clean(p_is_catchall);
    v_city text := clay_clean(p_city);
    v_country text := clay_clean(p_country);
    v_info_tags text := clay_clean(p_info_tags);
    v_extra_data_pairs text := clay_clean(p_extra_data_pairs);
    v_selected_approach text := clay_clean(p_selected_approach);
    v_batch_id text := clay_clean(p_batch_id);
    v_e1a text := clay_clean(p_email_1_variant_a);
    v_e1b text := clay_clean(p_email_1_variant_b);
    v_e2a text := clay_clean(p_email_2_variant_a);
    v_e2b text := clay_clean(p_email_2_variant_b);
    v_e3a text := clay_clean(p_email_3_variant_a);
    v_e3b text := clay_clean(p_email_3_variant_b);
    v_company_summary text := clay_clean(p_company_summary);
    v_personalizations_pairs text := clay_clean(p_personalizations_pairs);
    v_email_verified_at_clean text := clay_clean(p_email_verified_at);
BEGIN
    -- ── Required field validation ──────────────────────────────────────────
    v_email := LOWER(TRIM(clay_clean(p_email)));
    IF v_email IS NULL OR v_email = '' THEN
        RAISE EXCEPTION 'p_email is required and cannot be empty';
    END IF;

    DECLARE
        v_seg_clean text := clay_clean(p_segment_ids);
    BEGIN
        IF v_seg_clean IS NULL OR TRIM(v_seg_clean) = '' THEN
            RAISE EXCEPTION 'p_segment_ids is required (comma-separated, e.g. ''54'' or ''54,28'')';
        END IF;
        SELECT ARRAY(
            SELECT DISTINCT TRIM(s)::int FROM unnest(string_to_array(v_seg_clean, ',')) AS s WHERE TRIM(s) <> ''
        ) INTO v_segment_ids_array;
    END;
    IF array_length(v_segment_ids_array, 1) IS NULL THEN
        RAISE EXCEPTION 'p_segment_ids did not contain any valid integers';
    END IF;

    SELECT ARRAY(SELECT s FROM unnest(v_segment_ids_array) s WHERE NOT EXISTS (SELECT 1 FROM segments WHERE segment_id = s)) INTO v_unknown_segments;
    IF array_length(v_unknown_segments, 1) IS NOT NULL THEN
        RAISE EXCEPTION 'These segment_ids do not exist: %', v_unknown_segments;
    END IF;
    v_primary_segment_id := v_segment_ids_array[1];

    -- ── Safe timestamp parse (bad input → NULL, doesn't fail the row) ──────
    IF v_email_verified_at_clean IS NOT NULL AND TRIM(v_email_verified_at_clean) <> '' THEN
        BEGIN
            v_email_verified_at_ts := v_email_verified_at_clean::timestamptz;
        EXCEPTION WHEN OTHERS THEN
            v_email_verified_at_ts := NULL;
        END;
    END IF;

    -- ── Parse info_tags (comma-separated → text[]) ────────────────────────
    IF v_info_tags IS NOT NULL AND v_info_tags <> '' THEN
        SELECT ARRAY(SELECT TRIM(t) FROM unnest(string_to_array(v_info_tags, ',')) AS t WHERE TRIM(t) <> '') INTO v_info_tags_array;
    ELSE
        v_info_tags_array := ARRAY[]::text[];
    END IF;

    -- ── Parse extra_data pairs ("key1|val1;key2|val2" → jsonb) ─────────────
    -- Skips pairs where value is empty or matches CLAYFORMATVALUE pattern
    IF v_extra_data_pairs IS NOT NULL AND v_extra_data_pairs <> '' THEN
        SELECT COALESCE(jsonb_object_agg(TRIM(split_part(pair, '|', 1)), TRIM(split_part(pair, '|', 2))), '{}'::jsonb)
        INTO v_extra_data FROM unnest(string_to_array(v_extra_data_pairs, ';')) AS pair
        WHERE TRIM(split_part(pair, '|', 1)) <> ''
          AND TRIM(split_part(pair, '|', 2)) <> ''
          AND TRIM(split_part(pair, '|', 2)) !~ '^CLAYFORMATVALUE\(.*\)$';
    END IF;

    -- ── Parse personalizations pairs (same format) ────────────────────────
    IF v_personalizations_pairs IS NOT NULL AND v_personalizations_pairs <> '' THEN
        SELECT COALESCE(jsonb_object_agg(TRIM(split_part(pair, '|', 1)), TRIM(split_part(pair, '|', 2))), '{}'::jsonb)
        INTO v_personalizations FROM unnest(string_to_array(v_personalizations_pairs, ';')) AS pair
        WHERE TRIM(split_part(pair, '|', 1)) <> ''
          AND TRIM(split_part(pair, '|', 2)) <> ''
          AND TRIM(split_part(pair, '|', 2)) !~ '^CLAYFORMATVALUE\(.*\)$';
    END IF;

    -- ── Upsert lead ───────────────────────────────────────────────────────
    INSERT INTO leads (
        email, first_name, last_name, full_name, job_title,
        linkedin_profile_url, linkedin_username,
        company_name, company_domain, company_website, company_linkedin_url,
        industry, monthly_visits, employee_count,
        email_verified, email_verified_at, mx_provider, has_email_security_gateway,
        is_catchall, is_personal_email, city, country,
        segment_ids, info_tags, extra_data
    ) VALUES (
        v_email, v_first_name, v_last_name, v_full_name, v_job_title,
        v_linkedin_profile_url, v_linkedin_username,
        v_company_name, v_company_domain, v_company_website, v_company_linkedin_url,
        v_industry, p_monthly_visits, v_employee_count,
        v_email_verified, v_email_verified_at_ts, v_mx_provider, v_has_email_security_gateway,
        v_is_catchall, p_is_personal_email, v_city, v_country,
        v_segment_ids_array, v_info_tags_array, v_extra_data
    )
    ON CONFLICT (email) DO UPDATE SET
        first_name                 = COALESCE(EXCLUDED.first_name, leads.first_name),
        last_name                  = COALESCE(EXCLUDED.last_name, leads.last_name),
        full_name                  = COALESCE(EXCLUDED.full_name, leads.full_name),
        job_title                  = COALESCE(EXCLUDED.job_title, leads.job_title),
        linkedin_profile_url       = COALESCE(EXCLUDED.linkedin_profile_url, leads.linkedin_profile_url),
        linkedin_username          = COALESCE(EXCLUDED.linkedin_username, leads.linkedin_username),
        company_name               = COALESCE(EXCLUDED.company_name, leads.company_name),
        company_domain             = COALESCE(EXCLUDED.company_domain, leads.company_domain),
        company_website            = COALESCE(EXCLUDED.company_website, leads.company_website),
        company_linkedin_url       = COALESCE(EXCLUDED.company_linkedin_url, leads.company_linkedin_url),
        industry                   = COALESCE(EXCLUDED.industry, leads.industry),
        monthly_visits             = COALESCE(EXCLUDED.monthly_visits, leads.monthly_visits),
        employee_count             = COALESCE(EXCLUDED.employee_count, leads.employee_count),
        email_verified             = COALESCE(EXCLUDED.email_verified, leads.email_verified),
        email_verified_at          = COALESCE(EXCLUDED.email_verified_at, leads.email_verified_at),
        mx_provider                = COALESCE(EXCLUDED.mx_provider, leads.mx_provider),
        has_email_security_gateway = COALESCE(EXCLUDED.has_email_security_gateway, leads.has_email_security_gateway),
        is_catchall                = COALESCE(EXCLUDED.is_catchall, leads.is_catchall),
        is_personal_email          = COALESCE(EXCLUDED.is_personal_email, leads.is_personal_email),
        city                       = COALESCE(EXCLUDED.city, leads.city),
        country                    = COALESCE(EXCLUDED.country, leads.country),
        segment_ids                = (SELECT array_agg(DISTINCT s) FROM unnest(leads.segment_ids || EXCLUDED.segment_ids) s),
        info_tags                  = (SELECT array_agg(DISTINCT t) FROM unnest(leads.info_tags || EXCLUDED.info_tags) t),
        extra_data                 = COALESCE(leads.extra_data, '{}'::jsonb) || EXCLUDED.extra_data
    RETURNING lead_id, (xmax = 0) INTO v_lead_id, v_inserted;

    -- ── Conditional email_outputs insert ──────────────────────────────────
    -- Triggered ONLY if at least one cleaned email variant has real content
    v_has_email_output := (
        v_e1a IS NOT NULL OR v_e1b IS NOT NULL OR
        v_e2a IS NOT NULL OR v_e2b IS NOT NULL OR
        v_e3a IS NOT NULL OR v_e3b IS NOT NULL
    );

    IF v_has_email_output THEN
        SELECT client_id INTO v_client_id FROM segments WHERE segment_id = v_primary_segment_id;
        IF p_recipe_id IS NOT NULL THEN
            IF NOT EXISTS (SELECT 1 FROM recipes WHERE recipe_id = p_recipe_id AND segment_id = v_primary_segment_id) THEN
                RAISE EXCEPTION 'p_recipe_id % does not match the primary segment (first in p_segment_ids: %)', p_recipe_id, v_primary_segment_id;
            END IF;
        END IF;
        INSERT INTO email_outputs (
            lead_id, client_id, segment_id, recipe_id, recipe_version,
            selected_approach, batch_id, company_summary,
            email_1_variant_a, email_1_variant_b,
            email_2_variant_a, email_2_variant_b,
            email_3_variant_a, email_3_variant_b,
            personalizations
        ) VALUES (
            v_lead_id, v_client_id, v_primary_segment_id,
            p_recipe_id, COALESCE(p_recipe_version, 1),
            v_selected_approach, v_batch_id, v_company_summary,
            v_e1a, v_e1b, v_e2a, v_e2b, v_e3a, v_e3b,
            v_personalizations
        )
        RETURNING output_id INTO v_output_id;
    END IF;

    -- ── Return result ─────────────────────────────────────────────────────
    RETURN jsonb_build_object(
        'lead_id', v_lead_id,
        'lead_action', CASE WHEN v_inserted THEN 'inserted' ELSE 'updated' END,
        'segment_ids_applied', v_segment_ids_array,
        'output_id', v_output_id
    );
END;
$function$;
