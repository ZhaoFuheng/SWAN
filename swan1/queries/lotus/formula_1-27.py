import pandas as pd


def run(db):
    drivers = db.sql("SELECT forename, surname, forename || ' ' || surname AS key FROM drivers")
    keys = drivers[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the date of birth. key: {key}"
                        " Answer with the date only, in YYYY-MM-DD format.", suffix="dob")
    keys = keys.sem_map(("Provide the nationality. key: {key}" + " Answer with the value only, without any other words."), suffix="nationality")
    keys["dob"] = pd.to_datetime(keys["dob"].str.strip(), format="%Y-%m-%d",
                                 errors="coerce").dt.strftime("%Y-%m-%d")
    keys["nationality"] = keys["nationality"].str.strip()
    return db.sql("""
        SELECT STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', dob), forename, surname
        FROM t
        WHERE nationality = 'Japanese'
        ORDER BY dob DESC
        LIMIT 8
    """, t=drivers.merge(keys, on="key", how="left"))
