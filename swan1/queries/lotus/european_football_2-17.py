def run(db):
    rows = db.sql("""
        SELECT t1.player_name, t1.weight
        FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id
        ORDER BY t2.overall_rating DESC
        LIMIT 1
    """)
    return rows.sem_agg(("What is the player birthday (format: YYYY-MM-DD HH:MI:SS) {player_name} {weight}" + " Answer with the value only, without any other words."))[["_output"]]
