def run(db):
    rows = db.sql("SELECT Street FROM schools WHERE StatusType = 'Closed'")
    streets = rows[["Street"]].dropna().drop_duplicates()
    streets = streets.sem_map(("Provide the county name based on the street address. Street: {Street}" + " Answer with the value only, without any other words."),
                              suffix="County")
    streets["County"] = streets["County"].str.strip()
    return db.sql("""
        WITH temp_cte AS (
            SELECT schools.*, m.County
            FROM schools LEFT JOIN m ON m.Street = schools.Street
            WHERE schools.StatusType = 'Closed'
        )
        SELECT COUNT(DISTINCT School)
        FROM temp_cte
        WHERE temp_cte.County = (SELECT T1.County
                                 FROM temp_cte AS T1
                                 GROUP BY T1.County ORDER BY COUNT(T1.School) DESC LIMIT 1)
          AND temp_cte.StatusType = 'Closed' AND temp_cte.school IS NOT NULL AND temp_cte.Street IS NOT NULL
    """, m=streets[["Street", "County"]])
