-- ============================================================================
-- upsert_lead(...) -> jsonb
-- ----------------------------------------------------------------------------
-- The single Postgres function that Clay calls to push lead enrichment and
-- generated email outputs back into the TAM + Recipe DB.
--
-- One function, one HTTP endpoint, one body template - used across every
-- Clay table. Schema changes are made HERE and propagate automatically.
--
-- Required parameters:
--   p_email         text  - primary dedup key, lowercased + trimmed
--   p_segment_ids   text  - comma-separated segment_id ints (e.g. "54" or "54,28,37")
--                           First segment is "primary" - used for email_outputs.segment_id
--
-- Merge rules ("new data never destroys old data"):
--   SCALAR fields  - COALESCE(new, existing). New wins if non-null; else keep.
--   ARRAY fields   - segment_ids, info_tags: empty incoming -> keep existing;
--                    non-empty -> union, dedupe, sort. Never NULL.
--   JSONB fields   - extra_data: empty incoming -> keep existing;
--                    non-empty -> jsonb merge (new wins per key). Never NULL.
--
-- ZERO type casts in the Clay body:
--   p_monthly_visits, p_recipe_id, p_recipe_version, p_is_personal_email are
--   ALL typed text in the function signature and parsed internally:
--     - parse_int_flex() handles "10.2K" / "1.5M" / "$42,000" / CLAYFORMATVALUE
--     - boolean parser handles "true"/"false"/"yes"/"no"/"1"/"0" + CLAYFORMATVALUE
--   This makes the Clay body brittle-free against ANY garbage Clay might send.
--   Bad values become NULL silently; the row still succeeds.
--
-- All optional params are clay_clean()-ed: NULL, empty string, and Clay's
-- "CLAYFORMATVALUE(...)" placeholders are normalized to NULL.
--
-- Auto-derived fields (when operator does not provide them):
--   full_name           <- first_name + last_name
--   company_domain      <- normalize_company_domain(company_website)
--   linkedin_username   <- extract_linkedin_username(linkedin_profile_url)
--   is_personal_email   <- is_personal_email_domain(email)
--
-- Recipe fallback (for email_outputs insert):
--   If p_recipe_id is NULL and the row has email content, the function looks
--   up the active recipe for the primary segment and uses it. Returns a
--   clear error if no active recipe exists.
--
-- Side effects:
--   1. Upserts a row in `leads` (INSERT or UPDATE merging arrays + jsonb).
--   2. If any p_email_*_variant_* is non-null, ALSO inserts a new row in
--      `email_outputs` linked to the lead, primary segment, recipe.
--      Email outputs are append-only (every push creates a new row).
--
-- Returns:
--   { lead_id, lead_action, segment_ids_applied, recipe_id_used, output_id }
--
-- Depends on:
--   clay_clean()              - clay_clean.sql
--   parse_int_flex()          - parse_int_flex.sql
--   is_personal_email_domain(), normalize_company_domain(), extract_linkedin_username()
--                             - clay_helpers.sql
-- ============================================================================

CREATE OR REPLACE FUNCTION public.upsert_lead(p_email text, p_segment_ids text, p_first_name text DEFAULT NULL::text, p_last_name text DEFAULT NULL::text, p_full_name text DEFAULT NULL::text, p_job_title text DEFAULT NULL::text, p_linkedin_profile_url text DEFAULT NULL::text, p_linkedin_username text DEFAULT NULL::text, p_company_name text DEFAULT NULL::text, p_company_domain text DEFAULT NULL::text, p_company_website text DEFAULT NULL::text, p_company_linkedin_url text DEFAULT NULL::text, p_industry text DEFAULT NULL::text, p_monthly_visits text DEFAULT NULL::text, p_employee_count text DEFAULT NULL::text, p_email_verified text DEFAULT NULL::text, p_email_verified_at text DEFAULT NULL::text, p_mx_provider text DEFAULT NULL::text, p_has_email_security_gateway text DEFAULT NULL::text, p_is_catchall text DEFAULT NULL::text, p_is_personal_email text DEFAULT NULL::text, p_city text DEFAULT NULL::text, p_country text DEFAULT NULL::text, p_info_tags text DEFAULT NULL::text, p_extra_data_pairs text DEFAULT NULL::text, p_recipe_id text DEFAULT NULL::text, p_recipe_version text DEFAULT NULL::text, p_selected_approach text DEFAULT NULL::text, p_batch_id text DEFAULT NULL::text, p_email_1_variant_a text DEFAULT NULL::text, p_email_1_variant_b text DEFAULT NULL::text, p_email_2_variant_a text DEFAULT NULL::text, p_email_2_variant_b text DEFAULT NULL::text, p_email_3_variant_a text DEFAULT NULL::text, p_email_3_variant_b text DEFAULT NULL::text, p_company_summary text DEFAULT NULL::text, p_personalizations_pairs text DEFAULT NULL::text)
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
    v_effective_recipe_id int;
    v_effective_recipe_version int;
    v_monthly_visits_int int;
    v_recipe_id_int int;
    v_recipe_version_int int;
    v_ipe_clean text;
    v_is_personal_email_bool boolean;
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
    v_email := LOWER(TRIM(clay_clean(p_email)));
    IF v_email IS NULL OR v_email = '' THEN
        RAISE EXCEPTION 'p_email is required and cannot be empty';
    END IF;

    DECLARE v_seg_clean text := clay_clean(p_segment_ids);
    BEGIN
        IF v_seg_clean IS NULL OR TRIM(v_seg_clean) = '' THEN
            RAISE EXCEPTION 'p_segment_ids is required';
        END IF;
        SELECT ARRAY(SELECT DISTINCT TRIM(s)::int FROM unnest(string_to_array(v_seg_clean, ',')) AS s WHERE TRIM(s) <> '') INTO v_segment_ids_array;
    END;
    IF array_length(v_segment_ids_array, 1) IS NULL THEN
        RAISE EXCEPTION 'p_segment_ids did not contain any valid integers';
    END IF;
    SELECT ARRAY(SELECT s FROM unnest(v_segment_ids_array) s WHERE NOT EXISTS (SELECT 1 FROM segments WHERE segment_id = s)) INTO v_unknown_segments;
    IF array_length(v_unknown_segments, 1) IS NOT NULL THEN
        RAISE EXCEPTION 'These segment_ids do not exist: %', v_unknown_segments;
    END IF;
    v_primary_segment_id := v_segment_ids_array[1];

    v_monthly_visits_int := parse_int_flex(p_monthly_visits);
    v_recipe_id_int := parse_int_flex(p_recipe_id);
    v_recipe_version_int := parse_int_flex(p_recipe_version);

    v_ipe_clean := clay_clean(p_is_personal_email);
    IF v_ipe_clean IS NULL THEN
        v_is_personal_email_bool := NULL;
    ELSE
        v_is_personal_email_bool := CASE
            WHEN LOWER(TRIM(v_ipe_clean)) IN ('true','t','1','yes','y') THEN true
            WHEN LOWER(TRIM(v_ipe_clean)) IN ('false','f','0','no','n') THEN false
            ELSE NULL
        END;
    END IF;

    IF v_full_name IS NULL AND (v_first_name IS NOT NULL OR v_last_name IS NOT NULL) THEN
        v_full_name := TRIM(CONCAT_WS(' ', v_first_name, v_last_name));
    END IF;
    IF v_company_domain IS NULL AND v_company_website IS NOT NULL THEN
        v_company_domain := normalize_company_domain(v_company_website);
    END IF;
    IF v_linkedin_username IS NULL AND v_linkedin_profile_url IS NOT NULL THEN
        v_linkedin_username := extract_linkedin_username(v_linkedin_profile_url);
    END IF;
    IF v_is_personal_email_bool IS NULL AND v_email IS NOT NULL THEN
        v_is_personal_email_bool := is_personal_email_domain(v_email);
    END IF;

    IF v_email_verified_at_clean IS NOT NULL AND TRIM(v_email_verified_at_clean) <> '' THEN
        BEGIN
            v_email_verified_at_ts := v_email_verified_at_clean::timestamptz;
        EXCEPTION WHEN OTHERS THEN
            v_email_verified_at_ts := NULL;
        END;
    END IF;

    IF v_info_tags IS NOT NULL AND v_info_tags <> '' THEN
        SELECT ARRAY(SELECT TRIM(t) FROM unnest(string_to_array(v_info_tags, ',')) AS t WHERE TRIM(t) <> '') INTO v_info_tags_array;
    ELSE
        v_info_tags_array := ARRAY[]::text[];
    END IF;

    IF v_extra_data_pairs IS NOT NULL AND v_extra_data_pairs <> '' THEN
        SELECT COALESCE(jsonb_object_agg(TRIM(split_part(pair, '|', 1)), TRIM(split_part(pair, '|', 2))), '{}'::jsonb)
        INTO v_extra_data FROM unnest(string_to_array(v_extra_data_pairs, ';')) AS pair
        WHERE TRIM(split_part(pair, '|', 1)) <> ''
          AND TRIM(split_part(pair, '|', 2)) <> ''
          AND TRIM(split_part(pair, '|', 2)) !~ '^CLAYFORMATVALUE\(.*\)$';
    END IF;

    IF v_personalizations_pairs IS NOT NULL AND v_personalizations_pairs <> '' THEN
        SELECT COALESCE(jsonb_object_agg(TRIM(split_part(pair, '|', 1)), TRIM(split_part(pair, '|', 2))), '{}'::jsonb)
        INTO v_personalizations FROM unnest(string_to_array(v_personalizations_pairs, ';')) AS pair
        WHERE TRIM(split_part(pair, '|', 1)) <> ''
          AND TRIM(split_part(pair, '|', 2)) <> ''
          AND TRIM(split_part(pair, '|', 2)) !~ '^CLAYFORMATVALUE\(.*\)$';
    END IF;

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
        v_industry, v_monthly_visits_int, v_employee_count,
        v_email_verified, v_email_verified_at_ts, v_mx_provider, v_has_email_security_gateway,
        v_is_catchall, v_is_personal_email_bool, v_city, v_country,
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
        segment_ids = CASE
            WHEN COALESCE(array_length(EXCLUDED.segment_ids, 1), 0) = 0 THEN COALESCE(leads.segment_ids, ARRAY[]::int[])
            ELSE COALESCE(
                (SELECT array_agg(DISTINCT s ORDER BY s) FROM unnest(COALESCE(leads.segment_ids, ARRAY[]::int[]) || EXCLUDED.segment_ids) s),
                COALESCE(leads.segment_ids, ARRAY[]::int[])
            )
        END,
        info_tags = CASE
            WHEN COALESCE(array_length(EXCLUDED.info_tags, 1), 0) = 0 THEN COALESCE(leads.info_tags, ARRAY[]::text[])
            ELSE COALESCE(
                (SELECT array_agg(DISTINCT t ORDER BY t) FROM unnest(COALESCE(leads.info_tags, ARRAY[]::text[]) || EXCLUDED.info_tags) t),
                COALESCE(leads.info_tags, ARRAY[]::text[])
            )
        END,
        extra_data = CASE
            WHEN EXCLUDED.extra_data IS NULL OR EXCLUDED.extra_data = '{}'::jsonb THEN COALESCE(leads.extra_data, '{}'::jsonb)
            ELSE COALESCE(leads.extra_data, '{}'::jsonb) || EXCLUDED.extra_data
        END
    RETURNING lead_id, (xmax = 0) INTO v_lead_id, v_inserted;

    v_has_email_output := (
        v_e1a IS NOT NULL OR v_e1b IS NOT NULL OR
        v_e2a IS NOT NULL OR v_e2b IS NOT NULL OR
        v_e3a IS NOT NULL OR v_e3b IS NOT NULL
    );
    IF v_has_email_output THEN
        SELECT client_id INTO v_client_id FROM segments WHERE segment_id = v_primary_segment_id;
        IF v_recipe_id_int IS NOT NULL THEN
            IF NOT EXISTS (SELECT 1 FROM recipes WHERE recipe_id = v_recipe_id_int AND segment_id = v_primary_segment_id) THEN
                RAISE EXCEPTION 'p_recipe_id % does not match primary segment %', v_recipe_id_int, v_primary_segment_id;
            END IF;
            v_effective_recipe_id := v_recipe_id_int;
            v_effective_recipe_version := COALESCE(v_recipe_version_int, 1);
        ELSE
            SELECT recipe_id, version INTO v_effective_recipe_id, v_effective_recipe_version
            FROM recipes WHERE segment_id = v_primary_segment_id AND status = 'active' LIMIT 1;
            IF v_effective_recipe_id IS NULL THEN
                RAISE EXCEPTION 'No active recipe found for segment %', v_primary_segment_id;
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
            v_effective_recipe_id, v_effective_recipe_version,
            v_selected_approach, v_batch_id, v_company_summary,
            v_e1a, v_e1b, v_e2a, v_e2b, v_e3a, v_e3b,
            v_personalizations
        )
        RETURNING output_id INTO v_output_id;
    END IF;

    RETURN jsonb_build_object(
        'lead_id', v_lead_id,
        'lead_action', CASE WHEN v_inserted THEN 'inserted' ELSE 'updated' END,
        'segment_ids_applied', v_segment_ids_array,
        'recipe_id_used', v_effective_recipe_id,
        'output_id', v_output_id
    );
END;
$function$

