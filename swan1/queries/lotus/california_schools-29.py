def run(db):
    rows = db.sql("""
        SELECT T2.Street
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE T2.EdOpsCode = 'SSS'
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    fremont = streets.sem_filter("Is the address located in Fremont City? Street: {Street}")
    return db.sql("""
        SELECT T1."Enrollment (Ages 5-17)"
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE T2.EdOpsCode = 'SSS' AND T2.Street IN (SELECT Street FROM fremont)
          AND T1."Academic Year" >= 2014 AND T1."Academic Year" <= 2015
    """, fremont=fremont[["Street"]])
