TEMP_CTE = """
    SELECT t1.team_long_name,
           'Team Long Name: ' || t1.team_long_name AS team_key
    FROM Team AS t1
    INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id
    WHERE t2.chanceCreationPassingClass = 'Risky'
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["team_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the team short name (3 letters code). team_key: {team_key}" + " Answer with the value only, without any other words."), suffix="team_short_name")
    keys["team_short_name"] = keys["team_short_name"].str.strip()
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.team_long_name, answers.team_short_name
            FROM temp_cte LEFT JOIN answers ON answers.team_key = temp_cte.team_key
        )
        SELECT DISTINCT temp2.team_short_name
        FROM temp2
    """, answers=keys[["team_key", "team_short_name"]])
