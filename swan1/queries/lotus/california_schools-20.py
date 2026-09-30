def run(db):
    rows = db.sql("""
        SELECT T2.School, T1.AvgScrRead
        FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
    """)
    names = rows[["School"]].dropna().drop_duplicates()
    virtual = names.sem_filter("Is the school operate exclusively virtual? School: {School}")
    return db.sql("SELECT School FROM kept ORDER BY AvgScrRead DESC LIMIT 5",
                  kept=rows[rows["School"].isin(virtual["School"])])
