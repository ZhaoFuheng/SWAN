import pandas as pd

TEMP_CTE = """
    SELECT t1.id,
           t1.player_name,
           t1.weight,
           'Player Name: ' || t1.player_name || ', Weight: ' || t1.weight AS player_info_key
    FROM Player AS t1
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["player_info_key"]].dropna().drop_duplicates()
    left = keys.sem_filter("Is the player__ preferred foot left? player_info_key: {player_info_key}")
    keys = keys.sem_map("Provide the player birthday (YYYY-MM-DD). player_info_key: {player_info_key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="birthday")
    keys["birthday"] = pd.to_datetime(keys["birthday"].str.strip(), errors="coerce").dt.strftime("%Y-%m-%d")
    keys["is_left_foot"] = keys["player_info_key"].isin(left["player_info_key"]).astype(int)
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.id, temp_cte.player_name, temp_cte.weight, answers.is_left_foot, answers.birthday
            FROM temp_cte LEFT JOIN answers ON answers.player_info_key = temp_cte.player_info_key
        )
        SELECT CAST(COUNT(CASE WHEN temp2.is_left_foot THEN temp2.id ELSE NULL END) AS REAL) * 100 / COUNT(temp2.id) AS percent
        FROM temp2
        WHERE SUBSTR(birthday, 1, 4) BETWEEN '1987' AND '1992'
    """, answers=keys[["player_info_key", "is_left_foot", "birthday"]])
