def run(db):
    locs = db.sql("""
        SELECT DISTINCT T1.location
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T2.year = 2010 AND T1.location IS NOT NULL
    """)
    outside = locs.sem_filter("Is the location outside Asia and Europe? location: {location}")
    return db.sql("""
        SELECT COUNT(T2.raceId)
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T1.location IN (SELECT location FROM m) AND T2.year = 2010
    """, m=outside[["location"]])
