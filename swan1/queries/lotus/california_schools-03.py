def run(db):
    rows = db.sql("""
        SELECT T2.Phone,
               'District: ' || T1."District Name" || ' and School: ' || T1."School Name" AS district_school_key
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE T2.OpenDate > '2000-01-01'
    """)
    keys = rows[["district_school_key"]].dropna().drop_duplicates()
    keys = keys.sem_filter("Is this a charter school? district_school_key: {district_school_key}")
    keys = keys.sem_filter(
        "Is the school funded directly under the charter funding type? district_school_key: {district_school_key}")
    return rows[rows["district_school_key"].isin(keys["district_school_key"])][["Phone"]]
