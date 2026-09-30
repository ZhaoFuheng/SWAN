import pandas as pd

TEMP_CTE = """
    SELECT t1.player_api_id, t2.player_name, t1.sprint_speed, t1.date
    FROM Player_Attributes AS t1 INNER JOIN Player AS t2 ON t1.player_api_id = t2.player_api_id
    WHERE SUBSTR(t1.date, 1, 10) BETWEEN '2013-01-01' AND '2015-12-31' AND t1.sprint_speed >= 97
"""


def run(db):
    names = db.sql(TEMP_CTE)[["player_name"]].dropna().drop_duplicates()
    names = names.sem_map("Provide the birthday for this player (in SQL Datetime format). player_name: {player_name}"
                          " Answer with the date only, in YYYY-MM-DD format.", suffix="birthday")
    names["birthday"] = pd.to_datetime(names["birthday"].str.strip(), errors="coerce").dt.strftime("%Y-%m-%d")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.*, answers.birthday
            FROM temp_cte LEFT JOIN answers ON answers.player_name = temp_cte.player_name
        )
        SELECT DATETIME('now') - birthday AS age
        FROM temp2
    """, answers=names[["player_name", "birthday"]])
