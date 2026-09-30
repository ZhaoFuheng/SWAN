WITH marvel AS (
SELECT superhero_name, COUNT(*) AS count FROM superhero AS T1 
WHERE {{ LLMMap(
            'Is the publisher Marvel Comics?'
            'T1::superhero_name'
        ) }} = TRUE
),
superstrength AS (
SELECT COUNT(*) AS count FROM marvel
WHERE {{ LLMMap(
            'Does the hero has Super Strength?'
            'marvel::superhero_name'
        ) }} = TRUE
)
SELECT CAST(superstrength.count AS REAL) * 100 / marvel.count FROM superstrength, marvel
