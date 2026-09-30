def run(db):
    # BlendSQL applies the ORDER BY / LIMIT before mapping, so only the last 5 rounds are mapped
    rows = db.sql("""
        SELECT T1.year || ' ' || T1.name AS key, T1.name
        FROM races AS T1
        WHERE T1.year = 1999
        ORDER BY T1.round DESC
        LIMIT 5
    """)
    keys = rows[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the race date. key: {key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="date")
    return rows.merge(keys, on="key", how="left")[["name", "date"]]
