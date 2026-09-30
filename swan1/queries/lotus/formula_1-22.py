def run(db):
    keys = db.sql("""
        SELECT T1.forename || ' ' || T1.surname AS key
        FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId
        WHERE T2.fastestLapTime IS NOT NULL
        ORDER BY T2.fastestLapSpeed DESC
        LIMIT 1
    """)
    keys = keys.sem_map(("Provide the nationality. key: {key}" + " Answer with the value only, without any other words."), suffix="nationality")
    return keys[["nationality"]]
