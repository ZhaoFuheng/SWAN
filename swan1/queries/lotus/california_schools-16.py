def run(db):
    rows = db.sql("""
        SELECT 'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
        FROM frpm
    """)
    keys = rows[["district_school_key"]].dropna().drop_duplicates()
    charter = keys.sem_filter("Is this a charter school? district_school_key: {district_school_key}")
    return db.sql("""
        SELECT T2.AdmEmail1
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE 'District: ' || T1."District Name" || ' and School: ' || T1."School Name"
              IN (SELECT district_school_key FROM charter)
        ORDER BY T1."Enrollment (K-12)" ASC
        LIMIT 1
    """, charter=charter[["district_school_key"]])
