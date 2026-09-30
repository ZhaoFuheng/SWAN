def run(db):
    rows = db.sql("""
        SELECT schools.CDSCode, schools.Street
        FROM schools
        WHERE schools.MailState = 'CA' AND schools.StatusType = 'Active'
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    sj = streets.sem_filter("Is the address located in San Joaquin City? Street: {Street}")
    kept = rows[rows["Street"].isin(sj["Street"])]
    return [(int(kept["CDSCode"].notna().sum()),)]
