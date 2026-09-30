import pandas as pd

TEMP_CTE = """
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS key
    FROM Player
"""
JOINED = f"""
    SELECT t2.id, t2.overall_rating, temp_cte.key
    FROM ({TEMP_CTE}) AS temp_cte INNER JOIN Player_Attributes AS t2 ON temp_cte.player_api_id = t2.player_api_id
    WHERE SUBSTR(t2.date, 1, 4) BETWEEN '2010' AND '2015'
"""


def run(db):
    keys = db.sql(JOINED)[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the player height (int). key: {key} Answer with the number only.", suffix="height")
    keys["height"] = pd.to_numeric(keys["height"].str.strip(), errors="coerce")
    return db.sql(f"""
        WITH temp2 AS (
            SELECT joined.id, joined.overall_rating, heights.height
            FROM ({JOINED}) AS joined LEFT JOIN heights ON heights.key = joined.key
        )
        SELECT CAST(SUM(temp2.overall_rating) AS REAL) / COUNT(temp2.id)
        FROM temp2
        WHERE temp2.height > 179
    """, heights=keys[["key", "height"]])
