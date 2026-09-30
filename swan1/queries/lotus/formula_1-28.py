import pandas as pd


def run(db):
    race_data = db.sql("""
        SELECT T2.raceId, T2.year || ' ' || T2.name AS key, T1.name AS circuit_name
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
    """)
    keys = race_data[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the race date. key: {key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="date")
    keys["date"] = pd.to_datetime(keys["date"].str.strip(), format="%Y-%m-%d",
                                  errors="coerce").dt.strftime("%Y-%m-%d")
    return db.sql("""
        SELECT DISTINCT circuit_name
        FROM r
        WHERE STRFTIME('%Y-%m', date) BETWEEN '1990-06' AND '2000-06'
        GROUP BY circuit_name
        HAVING COUNT(raceId) = 4
    """, r=race_data.merge(keys, on="key", how="left"))
