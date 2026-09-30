TEMP_CTE = """
    SELECT T1.id,
           T1.player_name,
           T1.weight,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
    WHERE T1.weight < 130
"""


def run(db):
    temp_cte = db.sql(TEMP_CTE)
    keys = temp_cte[["player_key"]].dropna().drop_duplicates()
    left = keys.sem_filter("Is the player preferred foot left? player_key: {player_key}")
    rows = temp_cte[temp_cte["player_key"].isin(left["player_key"])]
    return [(int(rows["id"].nunique()),)]
