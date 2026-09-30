TEMP_CTE = """
    SELECT t1.id,
           hometeam.team_long_name AS home_team,
           awayteam.team_long_name AS away_team,
           t1.date,
           'Home Team: ' || hometeam.team_long_name || ', Away Team: ' || awayteam.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS awayteam ON t1.away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON t1.home_team_api_id = hometeam.team_api_id
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["match_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the football league name. match_key: {match_key}" + " Answer with the value only, without any other words."), suffix="league_name")
    keys["league_name"] = keys["league_name"].str.strip()
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.*, answers.league_name
            FROM temp_cte LEFT JOIN answers ON answers.match_key = temp_cte.match_key
        )
        SELECT league_name, COUNT(id)
        FROM temp2
        GROUP BY league_name
        ORDER BY COUNT(id) DESC
        LIMIT 1
    """, answers=keys[["match_key", "league_name"]])
