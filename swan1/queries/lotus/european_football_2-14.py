import pandas as pd

TEMP_CTE = """
    SELECT T1.player_name,
           T1.weight,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["player_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the preferred foot (left or right). player_key: {player_key}" + " Answer with the value only, without any other words."), suffix="preferred_foot")
    keys = keys.sem_map("Provide the player__ birthday (YYYY-MM-DD). player_key: {player_key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="birthday")
    keys["preferred_foot"] = keys["preferred_foot"].str.strip()
    keys["birthday"] = pd.to_datetime(keys["birthday"].str.strip(), errors="coerce").dt.strftime("%Y-%m-%d")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.player_name, temp_cte.player_key, answers.preferred_foot, answers.birthday
            FROM temp_cte LEFT JOIN answers ON answers.player_key = temp_cte.player_key
        )
        SELECT temp2.preferred_foot
        FROM temp2
        ORDER BY temp2.birthday DESC
        LIMIT 1
    """, answers=keys[["player_key", "preferred_foot", "birthday"]])
