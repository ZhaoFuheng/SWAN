def run(db):
    rows = db.sql("""
        SELECT T1."School Name" AS school_name, 'Street: ' || T2.Street || ' and School: ' || T2.School AS address
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        WHERE T1."Free Meal Count (Ages 5-17)" BETWEEN 1910 AND 2000
    """)
    addresses = rows[["address"]].dropna().drop_duplicates()
    addresses = addresses.sem_map(("Provide the website based on the school address. address: {address}" + " Answer with the value only, without any other words."),
                                  suffix="Website")
    addresses["Website"] = addresses["Website"].str.strip()
    return rows.merge(addresses, on="address", how="left")[["Website", "school_name"]]
