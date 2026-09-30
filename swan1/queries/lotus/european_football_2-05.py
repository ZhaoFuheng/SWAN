import pandas as pd

TEMP_CTE = """
    SELECT t1.date,
           away.team_long_name AS away_team,
           home.team_long_name AS home_team,
           'Home Team: ' || home.team_long_name || ', Away Team: ' || away.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS away ON t1.away_team_api_id = away.team_api_id
    INNER JOIN Team AS home ON t1.home_team_api_id = home.team_api_id
    WHERE t1.season = '2009/2010'
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["match_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the league name for this match. match_key: {match_key}" + " Answer with the value only, without any other words."), suffix="league_name")
    keys = keys.sem_map("Provide the goals for home and away teams in this match. match_key: {match_key}"
                        " Answer with the number only.", suffix="goal_difference")
    keys["league_name"] = keys["league_name"].str.strip()
    keys["goal_difference"] = pd.to_numeric(keys["goal_difference"].str.strip(), errors="coerce")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.away_team, answers.league_name, answers.goal_difference
            FROM temp_cte LEFT JOIN answers ON answers.match_key = temp_cte.match_key
        )
        SELECT away_team
        FROM temp2
        WHERE league_name = 'Scotland Premier League'
          AND goal_difference > 0
        GROUP BY away_team
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """, answers=keys[["match_key", "league_name", "goal_difference"]])
