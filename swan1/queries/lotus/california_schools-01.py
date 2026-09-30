def run(db):
    rows = db.sql("""
        SELECT T2.Zip,
               'District: ' || T1."District Name" || ' and School: ' || T1."School Name" AS district_school_key
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE T1."District Name" = 'Fresno County Office of Education'
    """)
    keys = rows[["district_school_key"]].dropna().drop_duplicates()
    charter = keys.sem_filter("Is this a charter school? district_school_key: {district_school_key}")
    return rows[rows["district_school_key"].isin(charter["district_school_key"])][["Zip"]]
