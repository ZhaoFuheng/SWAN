TEMP_CTE = """
    SELECT "Match".id,
           'Hometeam: ' || hometeam.team_long_name || ', Awayteam: ' || awayteam.team_long_name AS teamnames,
           'Hometeam: ' || hometeam.team_long_name || ', Awayteam: ' || awayteam.team_long_name
               || ', Date: ' || "Match".date AS match_key
    FROM "Match"
    INNER JOIN Team AS awayteam ON "Match".away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON "Match".home_team_api_id = hometeam.team_api_id
    WHERE "Match".season = '2015/2016'
"""


def run(db):
    temp_cte = db.sql(TEMP_CTE)
    # as in BlendSQL: the league LLMMap maps every teamnames value of temp_cte, the draw LLMMap every match_key
    teams = temp_cte[["teamnames"]].dropna().drop_duplicates()
    teams = teams.sem_map(("Provide the football league name. teamnames: {teamnames}" + " Answer with the value only, without any other words."), suffix="league_name")
    teams["league_name"] = teams["league_name"].str.strip()
    matches = temp_cte[["match_key"]].dropna().drop_duplicates()
    draws = matches.sem_filter("Did the match end in a draw? match_key: {match_key}")
    return db.sql(f"""
        WITH temp_cte AS ({TEMP_CTE}),
        temp2 AS (
            SELECT temp_cte.id, leagues.league_name
            FROM temp_cte LEFT JOIN leagues ON leagues.teamnames = temp_cte.teamnames
            WHERE temp_cte.match_key IN (SELECT match_key FROM draws)
        )
        SELECT temp2.league_name
        FROM temp2
        GROUP BY temp2.league_name
        ORDER BY COUNT(temp2.id) DESC
        LIMIT 1
    """, leagues=teams[["teamnames", "league_name"]], draws=draws[["match_key"]])
