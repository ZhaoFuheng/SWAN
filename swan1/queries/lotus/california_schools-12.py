def run(db):
    rows = db.sql("""
        SELECT T1."School Name" AS school_name, T2.Zip, T2.Street, T2.State
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE T1."Free Meal Count (Ages 5-17)" > 800 AND T1."School Type" = 'High Schools (Public)'
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    streets = streets.sem_filter("Is the address located in Monterey County? Street: {Street}")
    streets = streets.sem_map(("Provide the city name based on the address. Street: {Street}" + " Answer with the value only, without any other words."), suffix="City")
    streets["City"] = streets["City"].str.strip()
    kept = rows.merge(streets, on="Street")
    return kept[["school_name", "Zip", "Street", "City", "State"]]
