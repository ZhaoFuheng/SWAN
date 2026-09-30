TEMP_CTE = """
    SELECT t1.date,
           hometeam.team_long_name AS home_team,
           awayteam.team_long_name AS away_team,
           'Home Team: ' || hometeam.team_long_name || ', Away Team: ' || awayteam.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS awayteam ON t1.away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON t1.home_team_api_id = hometeam.team_api_id
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["match_key"]].dropna().drop_duplicates()
    netherlands = keys.sem_filter("Is the match in country Netherlands? match_key: {match_key}")
    keys = keys.sem_map(("Provide the league name. match_key: {match_key}" + " Answer with the value only, without any other words."), suffix="league_name")
    keys["league_name"] = keys["league_name"].str.strip()
    keys["in_Netherlands"] = keys["match_key"].isin(netherlands["match_key"]).astype(int)
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.match_key, answers.league_name, answers.in_Netherlands
            FROM temp_cte LEFT JOIN answers ON answers.match_key = temp_cte.match_key
        )
        SELECT temp2.league_name
        FROM temp2
        GROUP BY temp2.league_name
        HAVING in_Netherlands
    """, answers=keys[["match_key", "league_name", "in_Netherlands"]])
