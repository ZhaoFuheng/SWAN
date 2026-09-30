def run(db):
    options = sorted(db.table("colour")["colour"].dropna().unique())
    # LLMQA over the two-row UNION (sorted and deduplicated by sqlite)
    rows = db.sql("""
        SELECT 'Apocalypses' AS superhero_name
        UNION SELECT superhero_name FROM superhero AS T1 WHERE T1.superhero_name = 'Apocalypse'
    """)
    answer = rows.sem_agg(
        "What is the colour of Apocalypses skin? {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
    )
    return answer[["_output"]].assign(_output=answer["_output"].str.strip())
