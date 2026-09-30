def run(db):
    rows = db.sql("""
        SELECT Team.team_long_name FROM Team
        WHERE Team.team_long_name = 'Queens Park Rangers'
    """)
    return rows.sem_agg(("Provide the 3 letters short team name {team_long_name}" + " Answer with the value only, without any other words."))[["_output"]]
