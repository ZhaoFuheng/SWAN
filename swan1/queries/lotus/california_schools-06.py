def run(db):
    top = db.sql("""
        SELECT T1.Phone, 'Street: ' || T1.Street || ' and School: ' || T1.School AS address
        FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds
        ORDER BY CAST(T2.NumGE1500 AS REAL) / T2.NumTstTakr DESC
        LIMIT 10
    """)
    addresses = top[["address"]].dropna().drop_duplicates()
    addresses = addresses.sem_map(("Provide the city name based on the address. address: {address}" + " Answer with the value only, without any other words."), suffix="City")
    addresses["City"] = addresses["City"].str.strip()
    return top.merge(addresses, on="address", how="left")[["Phone", "City"]]
