import pandas as pd

TEMP_CTE = """
    SELECT t1.date, t2.team_long_name AS home_team, t3.team_long_name AS away_team,
           'Home Team: ' || t2.team_long_name || ', Away Team: ' || t3.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS t2 ON t1.home_team_api_id = t2.team_api_id
    INNER JOIN Team AS t3 ON t1.away_team_api_id = t3.team_api_id
    WHERE t1.season = '2015/2016'
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["match_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the league name. match_key: {match_key}" + " Answer with the value only, without any other words."), suffix="league_name")
    keys = keys.sem_map("Provide the total goals for this match. match_key: {match_key} Answer with the number only.",
                        suffix="total_goals")
    keys["league_name"] = keys["league_name"].str.strip()
    keys["total_goals"] = pd.to_numeric(keys["total_goals"].str.strip(), errors="coerce")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.*, answers.league_name, answers.total_goals
            FROM temp_cte LEFT JOIN answers ON answers.match_key = temp_cte.match_key
        )
        SELECT league_name
        FROM temp2
        GROUP BY league_name
        ORDER BY SUM(total_goals) DESC
        LIMIT 1
    """, answers=keys[["match_key", "league_name", "total_goals"]])
