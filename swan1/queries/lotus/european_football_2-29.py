def run(db):
    rows = db.sql("""SELECT 'Italy Serie A' AS "Italy Serie A" """)
    rows.columns = ["league"]  # a LOTUS column reference must be a plain identifier
    return rows.sem_agg(("Which country is the league Italy Serie A from? {league}" + " Answer with the value only, without any other words."))[["_output"]]
