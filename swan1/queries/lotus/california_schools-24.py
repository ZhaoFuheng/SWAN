def run(db):
    rows = db.sql("""
        SELECT schools.DOC, schools.Street
        FROM schools
        WHERE schools.StatusType = 'Merged'
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    if len(streets):
        streets = streets.sem_filter("Is the address located in Orange County? Street: {Street}")
    return db.sql("""
        SELECT CAST(SUM(CASE WHEN DOC = 54 THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN DOC = 52 THEN 1 ELSE 0 END)
        FROM schools
        WHERE StatusType = 'Merged' AND Street IN (SELECT Street FROM orange)
    """, orange=streets[["Street"]])
