-- Generates a cryptographically secure web-safe random string
CREATE OR REPLACE FUNCTION gen_prefixed_id(prefix TEXT, length INT DEFAULT 21) 
RETURNS TEXT AS $$
DECLARE
    alphabet TEXT := 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    alphabet_length INT := length(alphabet);
    result TEXT := '';
    i INT := 0;
    random_index INT;
    trimmed_prefix TEXT;
BEGIN
    -- Prevents bypassing checks with spaces
    trimmed_prefix := trim(prefix);

    -- Guards against empty prefixes
    IF prefix IS NULL OR trimmed_prefix = '' THEN
        RAISE EXCEPTION 'Invalid resource prefix: Prefix cannot be NULL or empty.'
            USING ERRCODE = 'invalid_parameter_value',
                  HINT = 'Please check your SQLAlchemy model server_default configurations. Every model must supply a valid 3-4 character token string (e.g., ''usr'').';
    END IF;

    -- Guards against excessively long or short prefixes
    IF length(trimmed_prefix) < 2 OR length(trimmed_prefix) > 5 THEN
        RAISE EXCEPTION 'Invalid resource prefix length: Current length is %, but it must be between 2 and 5 characters.', length(trimmed_prefix)
            USING ERRCODE = 'string_data_right_truncation',
                  HINT = 'Shorten or lengthen your resource prefix to fit the standard enterprise schema bounds (e.g., ''usr'', ''post'', ''doc'').';
    END IF;

    -- Generate random characters one by one
    WHILE i < length LOOP
        -- Use random bytes multiplied by the alphabet ceiling for safe uniform distribution
        random_index := floor(random() * alphabet_length + 1)::INT;
        result := result || substr(alphabet, random_index, 1);
        i := i + 1;
    END LOOP;

    RETURN prefix || '_' || result;
END;
$$ LANGUAGE plpgsql VOLATILE;