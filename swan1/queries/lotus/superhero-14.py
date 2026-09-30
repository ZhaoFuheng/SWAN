def run(db):
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    yes = names.sem_filter("Is the publisher Marvel Comics? superhero_name: {superhero_name}")
    # BlendSQL's marvel CTE: an aggregate with a bare superhero_name, i.e. ONE row; sqlite picks the name
    marvel = db.sql("""
        SELECT superhero_name, COUNT(*) AS count FROM superhero AS T1
        WHERE T1.superhero_name IN (SELECT superhero_name FROM yes)
    """, yes=yes)
    rest = marvel[["superhero_name"]].dropna().drop_duplicates()
    strong = rest.sem_filter("Does the hero has Super Strength? superhero_name: {superhero_name}") if len(rest) else rest
    return db.sql("""
        WITH superstrength AS (
            SELECT COUNT(*) AS count FROM marvel WHERE superhero_name IN (SELECT superhero_name FROM strong)
        )
        SELECT CAST(superstrength.count AS REAL) * 100 / marvel.count FROM superstrength, marvel
    """, marvel=marvel, strong=strong)
