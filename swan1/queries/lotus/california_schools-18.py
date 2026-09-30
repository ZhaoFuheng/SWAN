def run(db):
    rows = db.sql("""
        SELECT schools.School, schools.Street
        FROM satscores INNER JOIN schools ON satscores.cds = schools.CDSCode
        WHERE satscores.NumTstTakr >= 150 AND satscores.NumTstTakr <= 160
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    la = streets.sem_filter("Is the address located in Los Angeles County? Street: {Street}")
    rows = rows[rows["Street"].isin(la["Street"])]
    names = rows[["School"]].dropna().drop_duplicates()
    names = names.sem_map(("Provide the school website address for each school. School: {School}" + " Answer with the value only, without any other words."), suffix="Website")
    names["Website"] = names["Website"].str.strip()
    return rows.merge(names, on="School", how="left")[["Website"]]
