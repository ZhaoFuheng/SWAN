def run(db):
    rows = db.sql("""
        SELECT T2."School Code" AS school_code,
               'District: ' || T2."District Name" || ' and School: ' || T2."School Name" AS district_school_key
        FROM satscores AS T1 INNER JOIN frpm AS T2 ON T1.cds = T2.CDSCode
        WHERE T1.AvgScrMath > 560
    """)
    keys = rows[["district_school_key"]].dropna().drop_duplicates()
    direct = keys.sem_filter(
        "Is the school funded directly under the charter funding type? district_school_key: {district_school_key}")
    kept = rows[rows["district_school_key"].isin(direct["district_school_key"])]
    return [(int(kept["school_code"].notna().sum()),)]
