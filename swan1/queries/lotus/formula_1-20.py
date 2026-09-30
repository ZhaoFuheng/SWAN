def run(db):
    keys = db.sql("""
        SELECT DISTINCT T1.year || ' ' || T1.name AS key
        FROM races AS T1
        WHERE T1.raceId = 901
    """)
    keys = keys.sem_map(("Provide the wiki season URL. key: {key}" + " Answer with the value only, without any other words."), suffix="season_url")
    return keys[["season_url"]]
