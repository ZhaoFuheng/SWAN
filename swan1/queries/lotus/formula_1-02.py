def run(db):
    locs = db.sql("""
        SELECT DISTINCT T1.location
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T1.location IS NOT NULL
    """)
    locs = locs.sem_map(("Provide the country name. location: {location}" + " Answer with the value only, without any other words."), suffix="country")
    locs["country"] = locs["country"].str.strip()
    return db.sql("""
        SELECT DISTINCT T2.name
        FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        INNER JOIN m ON m.location = T1.location
        WHERE m.country = 'Germany'
    """, m=locs)
