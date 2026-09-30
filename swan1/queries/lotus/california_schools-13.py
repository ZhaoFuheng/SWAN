def run(db):
    rows = db.sql("""
        SELECT 'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
        FROM frpm
    """)
    keys = rows[["district_school_key"]].dropna().drop_duplicates()
    local = keys.sem_filter(
        "Is the school locally funded under the charter funding type? district_school_key: {district_school_key}")
    return db.sql("""
        WITH temp_cte AS (
            SELECT *, 'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
            FROM frpm
        )
        SELECT COUNT(*)
        FROM temp_cte AS T1
        WHERE T1.district_school_key IN (SELECT district_school_key FROM local)
          AND (T1."Enrollment (K-12)" - T1."Enrollment (Ages 5-17)") >
              (SELECT AVG(T3."Enrollment (K-12)" - T3."Enrollment (Ages 5-17)")
               FROM temp_cte AS T3
               WHERE T3.district_school_key IN (SELECT district_school_key FROM local))
    """, local=local[["district_school_key"]])
