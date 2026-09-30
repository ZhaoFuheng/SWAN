SELECT ai_agg(
    list('player_name: ' || player_name || ', weight: ' || weight),
    'What is the player birthday (format: YYYY-MM-DD HH:MI:SS)' || ' Answer with the value only, without any other words.'
)
FROM (
    SELECT t1.player_name, t1.weight
    FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id
    ORDER BY t2.overall_rating DESC
    LIMIT 1
)
