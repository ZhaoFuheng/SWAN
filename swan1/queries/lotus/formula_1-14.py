def run(db):
    keys = db.sql("""
        SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
        FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
        WHERE T1.raceId = 347 AND T1.q2 LIKE '1:15%'
    """)
    out = keys.sem_agg(("Where is he from? {key}" + " Answer with the value only, without any other words."), suffix="_output")
    return [(out["_output"].iloc[0],)]
