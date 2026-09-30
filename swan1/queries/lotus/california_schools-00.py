OPTIONS = ["Traditional", "Juvenile Court School", "County Community School", "State Special School",
           "Alternative School of Choice", "Continuation School", "Special Education School",
           "Community Day School", "Home and Hospital", "Opportunity School", "Youth Authority School",
           "District Special Education Consortia School"]


def run(db):
    frpm = db.sql("""
        SELECT "Free Meal Count (Ages 5-17)" / "Enrollment (Ages 5-17)" AS rate,
               'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
        FROM frpm
        WHERE "Free Meal Count (Ages 5-17)" / "Enrollment (Ages 5-17)" IS NOT NULL
    """)
    keys = frpm[["district_school_key"]].dropna().drop_duplicates()
    keys = keys.sem_map(
        "What is the educational option type of the school? district_school_key: {district_school_key}"
        " Answer with exactly one of: " + ", ".join(OPTIONS) + ".",
        suffix="option_type",
    )
    rows = frpm.merge(keys, on="district_school_key")
    rows = rows[rows["option_type"].str.strip() == "Continuation School"]
    return rows.sort_values("rate").head(10)[["rate"]]
