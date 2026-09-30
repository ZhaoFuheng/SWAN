import pandas as pd

PLAYER_KEY = """
    SELECT T1.player_name,
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
        SELECT temp_cte.player_name
        FROM temp_cte
        ORDER BY temp_cte.height ASC
        LIMIT 1
    """, answers=keys[["player_key", "height"]])
