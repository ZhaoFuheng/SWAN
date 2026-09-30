def run(db):
    options = sorted(db.table("superpower")["power_name"].dropna().unique())
    # LLMQA over (SELECT superhero_name FROM superhero WHERE superhero_name = '3-D Man')
    rows = db.sql("SELECT superhero_name FROM superhero WHERE superhero.superhero_name = '3-D Man'")
    answer = rows.sem_agg(
        "Provide a list of super powers seperated by comma. {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
    )
    temp = answer[["_output"]].rename(columns={"_output": "powers"})
    temp["powers"] = temp["powers"].str.strip()
    # BlendSQL's splitter, run as is on sqlite
    return db.sql("""
        WITH RECURSIVE Splitter AS (
            SELECT
                TRIM(SUBSTR(powers, 1, INSTR(powers || ',', ',') - 1)) AS superpower,
                TRIM(SUBSTR(powers, INSTR(powers || ',', ',') + 1)) AS remaining
            FROM temp_cte

            UNION ALL

            SELECT
                TRIM(SUBSTR(remaining, 1, INSTR(remaining || ',', ',') - 1)) AS superpower,
                TRIM(SUBSTR(remaining, INSTR(remaining || ',', ',') + 1)) AS remaining
            FROM Splitter
            WHERE remaining != ''
        )
        SELECT superpower FROM Splitter
    """, temp_cte=temp)
