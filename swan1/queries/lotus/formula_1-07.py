import pandas as pd


def run(db):
    # BlendSQL maps every circuit's location in its CTE, before the join and the race-name filter
    locs = db.table("circuits")[["location"]].dropna().drop_duplicates()
    locs = locs.sem_map("Provide the latitude based on location (float). location: {location}"
                        " Answer with the number only.", suffix="lat")
    locs = locs.sem_map("Provide the longitude based on location (float). location: {location}"
                        " Answer with the number only.", suffix="lng")
    locs["lat"] = pd.to_numeric(locs["lat"].str.strip(), errors="coerce")
    locs["lng"] = pd.to_numeric(locs["lng"].str.strip(), errors="coerce")
    return db.sql("""
        SELECT DISTINCT m.lat, m.lng
        FROM circuits AS T1 INNER JOIN m ON m.location = T1.location
        INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
        WHERE T2.name = 'Abu Dhabi Grand Prix'
    """, m=locs)
