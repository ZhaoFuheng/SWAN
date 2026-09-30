def run(db):
    rows = db.sql("""
        SELECT schools.Street
        FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    streets = streets.sem_map(("Provide the city name based on the address. Street: {Street}" + " Answer with the value only, without any other words."), suffix="City")
    streets["City"] = streets["City"].str.strip()
    return db.sql("""
        WITH temp_cte AS (
            SELECT frpm."Enrollment (K-12)", m.City
            FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode
            LEFT JOIN m ON m.Street = schools.Street
        )
        SELECT temp_cte.City
        FROM temp_cte
        GROUP BY temp_cte.City
        ORDER BY SUM(temp_cte."Enrollment (K-12)") ASC
        LIMIT 2
    """, m=streets[["Street", "City"]])
