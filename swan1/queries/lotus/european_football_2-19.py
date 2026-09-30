import pandas as pd

TEMP_CTE = """
    SELECT t1.id,
           t1.date,
           t1.season,
           hometeam.team_long_name AS home_team,
           awayteam.team_long_name AS away_team,
           'Home Team: ' || hometeam.team_long_name || ', Away Team: ' || awayteam.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS awayteam ON t1.away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON t1.home_team_api_id = hometeam.team_api_id
    WHERE t1.season = '2010/2011'
"""


def run(db):
    keys = db.sql(TEMP_CTE)[["match_key"]].dropna().drop_duplicates()
    poland = keys.sem_filter("Is the match in country Poland. match_key: {match_key}")
    keys = keys.sem_map("Provide the home team goals. match_key: {match_key} Answer with the number only.",
                        suffix="home_team_goal")
    keys["home_team_goal"] = pd.to_numeric(keys["home_team_goal"].str.strip(), errors="coerce")
    keys["in_Poland"] = keys["match_key"].isin(poland["match_key"]).astype(int)
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.match_key, temp_cte.id, answers.home_team_goal, answers.in_Poland
            FROM temp_cte LEFT JOIN answers ON answers.match_key = temp_cte.match_key
        )
        SELECT CAST(SUM(temp2.home_team_goal) AS REAL) / COUNT(temp2.id) AS avg_home_goals
        FROM temp2
        WHERE temp2.in_Poland
    """, answers=keys[["match_key", "home_team_goal", "in_Poland"]])
