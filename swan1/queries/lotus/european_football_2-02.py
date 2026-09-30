import pandas as pd

TEMP_CTE = """
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS key
    FROM Player
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["key"]].dropna().drop_duplicates()
    # as in BlendSQL: the height LLMMap maps every key of temp_cte, the birth-year LLMMap too
    heights = keys.sem_map("Provide the player height (int). key: {key} Answer with the number only.", suffix="height")
    heights["height"] = pd.to_numeric(heights["height"].str.strip(), errors="coerce")
    born = keys.sem_filter("Is the player born in between 1990 and 1995? key: {key}")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.id, heights.height
            FROM temp_cte LEFT JOIN heights ON heights.key = temp_cte.key
            WHERE temp_cte.key IN (SELECT key FROM born)
        )
        SELECT SUM(height) / COUNT(id)
        FROM temp2
    """, heights=heights[["key", "height"]], born=born[["key"]])
