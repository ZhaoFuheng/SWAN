def run(db):
    race_data = db.sql("""
        SELECT DISTINCT T2.driverId, T1.year || ' ' || T1.name AS key
        FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId
            AND T2.time IS NOT NULL
    """)
    keys = race_data[["key"]].dropna().drop_duplicates()
    on_day = keys.sem_filter("Was the race on 2015-11-29? key: {key}")
    return [(int(race_data.loc[race_data["key"].isin(on_day["key"]), "driverId"].count()),)]
