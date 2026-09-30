def run(db):
    rows = db.sql("""
        SELECT T2.year || ' ' || T2.name AS key
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T1.name = 'Brands Hatch' AND T2.name = 'British Grand Prix'
        ORDER BY T2.year DESC LIMIT 3
    """)
    keys = rows[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the race date. key: {key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="date")
    return rows.merge(keys, on="key", how="left")[["date"]]
