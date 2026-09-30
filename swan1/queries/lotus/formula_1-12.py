def run(db):
    drivers = db.sql("""
        SELECT DISTINCT T2.driverId, T2.forename, T2.surname, T2.forename || ' ' || T2.surname AS key
        FROM lapTimes AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
        WHERE T1.raceId = 161 AND T1.time LIKE '1:27%'
    """)
    keys = drivers[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the wiki url. key: {key}" + " Answer with the value only, without any other words."), suffix="person_url")
    rows = drivers.merge(keys, on="key", how="left")
    return rows[["forename", "surname", "person_url"]].drop_duplicates()
