def run(db):
    rows = db.sql("""
        WITH temp_cte AS (
            SELECT *, 'Location: ' || location || ', Name: ' || name AS key
            FROM circuits
        )
        SELECT temp_cte.key
        FROM temp_cte INNER JOIN races AS T2 ON T2.circuitId = temp_cte.circuitId
        WHERE temp_cte.name = 'Circuit de Barcelona-Catalunya'
    """)
    keys = rows[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map(("Provide the wiki url. key: {key}" + " Answer with the value only, without any other words."), suffix="url")
    return rows.merge(keys, on="key", how="left")[["url"]]
