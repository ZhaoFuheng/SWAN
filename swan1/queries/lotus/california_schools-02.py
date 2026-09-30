def run(db):
    top = db.sql("""
        SELECT T2.MailStreet, T2.Street
        FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
        ORDER BY T1."FRPM Count (K-12)" DESC
        LIMIT 1
    """)
    context = db.sql("""
        SELECT T4.Street
        FROM frpm AS T3 INNER JOIN schools AS T4 ON T3.CDSCode = T4.CDSCode
        ORDER BY T3."FRPM Count (K-12)" DESC
        LIMIT 1
    """)
    city = context.sem_agg(("Provide the city name based on the address. {Street}" + " Answer with the value only, without any other words."), suffix="_output")
    top["City"] = city["_output"].iloc[0]
    return top[["MailStreet", "City"]]
