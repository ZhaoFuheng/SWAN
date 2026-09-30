import pandas as pd

TEMP_CTE = """
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS key
    FROM Player
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the player height (int). key: {key} Answer with the number only.", suffix="height")
    keys["height"] = pd.to_numeric(keys["height"].str.strip(), errors="coerce")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE})
        SELECT temp_cte.player_name
        FROM temp_cte LEFT JOIN heights ON heights.key = temp_cte.key
        ORDER BY heights.height DESC
        LIMIT 1
    """, heights=keys[["key", "height"]])
