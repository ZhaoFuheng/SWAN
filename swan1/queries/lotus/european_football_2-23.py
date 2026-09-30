TEMP_CTE = """
    SELECT T1.player_name,
           T1.id,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
"""


def run(db):
    temp_cte = db.sql(TEMP_CTE)
    keys = temp_cte[["player_key"]].dropna().drop_duplicates()
    left = keys.sem_filter("Is player preferred foot left player_key: {player_key}")
    rows = temp_cte[temp_cte["player_key"].isin(left["player_key"])]
    return rows[["id", "player_name"]].drop_duplicates()
