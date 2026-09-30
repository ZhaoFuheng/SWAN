def run(db):
    rows = db.sql("""
        SELECT T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key, T2.points, T2.wins
        FROM drivers AS T1 INNER JOIN driverStandings AS T2 ON T2.driverId = T1.driverId
        WHERE T2.wins = 1
    """)
    keys = rows[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the nationality. key: {key}" + " Answer with the value only, without any other words."), suffix="nationality")
    return db.sql("""
        SELECT forename, surname, nationality, AVG(points) AS avg_points
        FROM r
        GROUP BY forename, surname, nationality
        ORDER BY COUNT(wins) DESC
        LIMIT 10
    """, r=rows.merge(keys, on="key", how="left")[["forename", "surname", "nationality", "points", "wins"]])
