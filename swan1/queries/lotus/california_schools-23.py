def run(db):
    rows = db.sql("""
        SELECT schools.School, schools.Street
        FROM schools
        WHERE schools.DOC = 52 AND strftime('%Y', schools.OpenDate) = '1980'
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    alameda = streets.sem_filter("Is the address located in Alameda County? Street: {Street}")
    return db.sql("SELECT CAST(COUNT(DISTINCT School) AS REAL) / 12 FROM kept",
                  kept=rows[rows["Street"].isin(alameda["Street"])])
