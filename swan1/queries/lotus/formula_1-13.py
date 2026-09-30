def run(db):
    # BlendSQL applies the ORDER BY / LIMIT before mapping, so only the top 5 rows are mapped
    rows = db.sql("""
        WITH driver_data AS (
            SELECT DISTINCT T1.forename || ' ' || T1.surname AS key, fastestLapSpeed
            FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId
            WHERE T2.raceId = 933 AND T2.fastestLapTime IS NOT NULL
        )
        SELECT key FROM driver_data ORDER BY fastestLapSpeed DESC LIMIT 5
    """)
    keys = rows[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the nationality. key: {key}" + " Answer with the value only, without any other words."), suffix="nationality")
    return rows.merge(keys, on="key", how="left")[["nationality"]]
