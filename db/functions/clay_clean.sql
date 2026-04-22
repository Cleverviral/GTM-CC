-- ============================================================================
-- clay_clean(text) → text
-- ----------------------------------------------------------------------------
-- Helper used by upsert_lead() to normalize Clay's empty-format placeholders.
--
-- Clay substitutes the literal string "CLAYFORMATVALUE()" or
-- "CLAYFORMATVALUE(undefined)" into HTTP request bodies when a referenced
-- column is empty for a given row. This helper recognizes those patterns
-- (along with NULL and whitespace-only strings) and returns NULL — so
-- downstream logic can treat them uniformly as "no value".
--
-- Behavior:
--   clay_clean(NULL)                            → NULL
--   clay_clean('')                              → NULL
--   clay_clean('   ')                           → NULL
--   clay_clean('CLAYFORMATVALUE()')             → NULL
--   clay_clean('CLAYFORMATVALUE(undefined)')    → NULL
--   clay_clean('CLAYFORMATVALUE(anything)')     → NULL
--   clay_clean('hello')                         → 'hello'
-- ============================================================================

CREATE OR REPLACE FUNCTION public.clay_clean(t text)
 RETURNS text
 LANGUAGE sql
 IMMUTABLE
AS $function$
    SELECT CASE
        WHEN t IS NULL THEN NULL
        WHEN TRIM(t) = '' THEN NULL
        WHEN t ~ '^CLAYFORMATVALUE\(.*\)$' THEN NULL
        ELSE t
    END
$function$;
