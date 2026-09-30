import pandas as pd


def run(db):
    drivers = db.sql("""
        SELECT DISTINCT T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key
        FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId
        WHERE T2.raceId = 872 AND T2.time IS NOT NULL
    """)
    keys = drivers[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the date of birth. key: {key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="dob")
    keys["dob"] = pd.to_datetime(keys["dob"].str.strip(), format="%Y-%m-%d",
                                 errors="coerce").dt.strftime("%Y-%m-%d")
    return db.sql("SELECT forename, surname FROM d ORDER BY dob DESC LIMIT 5",
                  d=drivers.merge(keys, on="key", how="left"))
