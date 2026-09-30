def run(db):
    rows = db.sql("""
        SELECT T1.CDSCode, T1.Street,
               'District: ' || T3."District Name" || ' and School: ' || T3."School Name" AS district_school_key
        FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds
        JOIN frpm AS T3 ON T1.CDSCode = T3.CDSCode
        WHERE T2.NumTstTakr <= 250
    """)
    keys = rows[["district_school_key"]].dropna().drop_duplicates()
    direct = keys.sem_filter(
        "Is the school funded directly under the charter funding type? district_school_key: {district_school_key}")
    streets = rows[["Street"]].dropna().drop_duplicates()
    contra = streets.sem_filter("Is the address located in Contra Costa County? Street: {Street}")
    kept = rows[rows["district_school_key"].isin(direct["district_school_key"])
                & rows["Street"].isin(contra["Street"])]
    return [(int(kept["CDSCode"].notna().sum()),)]
