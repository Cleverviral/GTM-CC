-- ============================================================================
-- parse_int_flex(text) → int
-- ----------------------------------------------------------------------------
-- Flexible integer parser that accepts Clay's display-formatted numbers.
-- Returns NULL instead of erroring on bad input, so a bad number in one
-- row doesn't abort the whole Clay push.
--
-- Handles:
--   "500"             → 500
--   "10,200"          → 10200                 (commas stripped)
--   "$42.5K"          → 42500                 (currency symbol stripped)
--   "10.2K" / "10.2k" → 10200                 (K suffix = ×1000, case-insensitive)
--   "1.5M" / "1.5m"   → 1500000               (M suffix = ×1000000)
--   "2B" / "2b"       → 2000000000            (B suffix = ×1000000000)
--   "  1,234.56M  "   → 1234560000            (whitespace tolerated)
--   "abc"             → NULL                  (unparseable → NULL, not error)
--   ""                → NULL
--   NULL              → NULL
--   "CLAYFORMATVALUE(...)"  → NULL            (via clay_clean)
--
-- Depends on: clay_clean() — see clay_clean.sql
-- ============================================================================

CREATE OR REPLACE FUNCTION public.parse_int_flex(t text) RETURNS int
LANGUAGE plpgsql IMMUTABLE
AS $$
DECLARE
    v_clean text;
    v_num numeric;
    v_mult numeric := 1;
    v_last char;
BEGIN
    v_clean := clay_clean(t);
    IF v_clean IS NULL THEN RETURN NULL; END IF;

    v_clean := UPPER(TRIM(v_clean));
    v_clean := REPLACE(v_clean, ',', '');
    v_clean := REPLACE(v_clean, ' ', '');
    v_clean := REPLACE(v_clean, '$', '');
    IF v_clean = '' THEN RETURN NULL; END IF;

    v_last := RIGHT(v_clean, 1);
    IF v_last = 'K' THEN
        v_mult := 1000;
        v_clean := LEFT(v_clean, LENGTH(v_clean) - 1);
    ELSIF v_last = 'M' THEN
        v_mult := 1000000;
        v_clean := LEFT(v_clean, LENGTH(v_clean) - 1);
    ELSIF v_last = 'B' THEN
        v_mult := 1000000000;
        v_clean := LEFT(v_clean, LENGTH(v_clean) - 1);
    END IF;

    BEGIN
        v_num := v_clean::numeric;
    EXCEPTION WHEN OTHERS THEN
        RETURN NULL;
    END;

    RETURN ROUND(v_num * v_mult)::int;
END;
$$;
