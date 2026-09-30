def run(db):
    keys = db.sql("""
        SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
        FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
        WHERE T1.raceId = 45 AND T1.q3 LIKE '1:33%'
    """)
    keys = keys.sem_map(("Provide the F1 driver abbreviated code. key: {key}" + " Answer with the value only, without any other words."), suffix="driver_code")
    return keys[["driver_code"]]
