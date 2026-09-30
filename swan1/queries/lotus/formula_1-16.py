def run(db):
    keys = db.sql("""
        SELECT DISTINCT races.year || ' ' || races.name AS key
        FROM races INNER JOIN results AS T2 ON T2.raceId = races.raceId
        WHERE races.year = 1983
    """)
    on_day = keys.sem_filter("Was the race on 07-16? key: {key}")
    return db.sql("""
        SELECT CAST(COUNT(CASE WHEN T2.time IS NOT NULL THEN T2.driverId END) AS REAL) * 100 / COUNT(T2.driverId)
        FROM races INNER JOIN results AS T2 ON T2.raceId = races.raceId
        WHERE races.year = 1983 AND races.year || ' ' || races.name IN (SELECT key FROM m)
    """, m=on_day[["key"]])
