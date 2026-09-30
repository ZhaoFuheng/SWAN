-- sqlite's bare superhero_name in an aggregate without GROUP BY -> any_value(); MATERIALIZED because
-- marvel is read twice and must be evaluated (and its AI calls made) once
WITH marvel AS MATERIALIZED (
    SELECT any_value(superhero_name) AS superhero_name, COUNT(*) AS count
    FROM superhero AS T1
    WHERE ai_filter('Is the publisher Marvel Comics? superhero_name: ' || T1.superhero_name)
),
superstrength AS (
    SELECT COUNT(*) AS count
    FROM marvel
    WHERE ai_filter('Does the hero has Super Strength? superhero_name: ' || marvel.superhero_name)
)
SELECT CAST(superstrength.count AS DOUBLE) * 100 / marvel.count
FROM superstrength, marvel
