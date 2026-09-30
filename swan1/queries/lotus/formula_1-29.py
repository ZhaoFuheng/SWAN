def run(db):
    keys = db.sql("""
        SELECT DISTINCT T1.location || ' ' || T1.name AS key
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T2.year = 2006 AND T1.location IS NOT NULL
    """)
    usa = keys.sem_filter("Was it in USA? key: {key}")
    return db.sql("""
        SELECT T1.name AS circuit_name, T1.location, T2.name AS race_name
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T1.location || ' ' || T1.name IN (SELECT key FROM m) AND T2.year = 2006
    """, m=usa[["key"]])
