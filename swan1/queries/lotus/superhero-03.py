def run(db):
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    blue = names.sem_filter("Does the hero has blue eye? superhero_name: {superhero_name}")
    return [(int(heroes["superhero_name"].isin(blue["superhero_name"]).sum()),)]
