import pandas as pd

PLAYER_KEY = """
    SELECT T1.player_name,
           T1.player_api_id,
           'Player Name: ' || T1.player_name AS player_key
    FROM Player AS T1
"""


def run(db):
    keys = db.sql(PLAYER_KEY)[["player_key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the height in cm. player_key: {player_key} Answer with the number only.",
                        suffix="height")
    keys["height"] = pd.to_numeric(keys["height"].str.strip(), errors="coerce")
    return db.sql(f"""
        WITH player_key AS ({PLAYER_KEY}),
        temp_cte AS (
            SELECT player_key.*, answers.height
            FROM player_key LEFT JOIN answers ON answers.player_key = player_key.player_key
        )
        SELECT A
        FROM (
            SELECT AVG(T3.finishing) AS result, 'Max' AS A
            FROM temp_cte
            INNER JOIN Player_Attributes AS T3 ON temp_cte.player_api_id = T3.player_api_id
            WHERE temp_cte.height = (SELECT MAX(height) FROM temp_cte)

            UNION

            SELECT AVG(T3.finishing) AS result, 'Min' AS A
            FROM temp_cte
            INNER JOIN Player_Attributes AS T3 ON temp_cte.player_api_id = T3.player_api_id
            WHERE temp_cte.height = (SELECT MIN(height) FROM temp_cte)
        ) AS result_table
        ORDER BY result DESC
        LIMIT 1
    """, answers=keys[["player_key", "height"]])
