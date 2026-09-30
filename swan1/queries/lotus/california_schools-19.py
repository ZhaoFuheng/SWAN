def run(db):
    rows = db.sql("""
        SELECT T1.NumTstTakr, schools.Street
        FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
        WHERE strftime('%Y', schools.OpenDate) = '1980'
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    fresno = streets.sem_filter("Is the address located in Fresno County? Street: {Street}")
    return db.sql("SELECT AVG(NumTstTakr) FROM kept", kept=rows[rows["Street"].isin(fresno["Street"])])
