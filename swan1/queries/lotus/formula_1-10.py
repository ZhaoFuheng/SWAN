def run(db):
    keys = db.sql("""
        SELECT DISTINCT T1.name || ' ' || T1.year AS key
        FROM races AS T1 INNER JOIN seasons AS T2 ON T2.year = T1.year
        WHERE T1.raceId = 901
    """)
    keys = keys.sem_map(("Provide the wiki season URL. key: {key}" + " Answer with the value only, without any other words."), suffix="season_url")
    return keys[["season_url"]]
