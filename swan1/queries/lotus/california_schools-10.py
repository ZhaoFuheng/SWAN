def run(db):
    schools = db.table("schools")[["School", "Street"]]
    streets = schools[["Street"]].dropna().drop_duplicates()
    contra = streets.sem_filter("Is the address located in Contra Costa County? Street: {Street}")
    temp_cte = schools[schools["Street"].isin(contra["Street"])][["School"]]
    return db.sql("""
        SELECT sname
        FROM satscores
        WHERE sname IN (SELECT School FROM temp_cte)
        ORDER BY satscores.NumTstTakr DESC
        LIMIT 1
    """, temp_cte=temp_cte)
