def run(db):
    keys = db.sql("""
        SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
        FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
        WHERE T1.raceId = 355 AND T1.q2 LIKE '1:40%'
    """)
    keys = keys.sem_map(("Provide the nationality. key: {key}" + " Answer with the value only, without any other words."), suffix="nationality")
    return keys[["nationality"]].drop_duplicates()
