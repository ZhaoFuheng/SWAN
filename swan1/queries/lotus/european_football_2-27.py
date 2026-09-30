TEAM_KEY = """
    SELECT t1.team_long_name, t2.buildUpPlayPassing, 'Team Long Name: ' || t1.team_long_name AS team_key
    FROM Team AS t1
    INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id
    WHERE t2.buildUpPlaySpeedClass = 'Fast'
"""


def run(db):
    # as in BlendSQL: the LLMMap maps every team_key of team_key; buildUpPlayPassing > 70 is applied after it
    keys = db.sql(TEAM_KEY)[["team_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the 3 letters team short name. team_key: {team_key}" + " Answer with the value only, without any other words."), suffix="team_short_name")
    keys["team_short_name"] = keys["team_short_name"].str.strip()
    return db.sql(f"""
        WITH team_key AS ({TEAM_KEY}),
        temp_cte AS (
            SELECT team_key.buildUpPlayPassing, answers.team_short_name
            FROM team_key LEFT JOIN answers ON answers.team_key = team_key.team_key
        )
        SELECT DISTINCT temp_cte.team_short_name
        FROM temp_cte
        WHERE temp_cte.buildUpPlayPassing > 70
    """, answers=keys[["team_key", "team_short_name"]])
