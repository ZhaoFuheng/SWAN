def run(db):
    keys = db.sql("""
        SELECT DISTINCT 'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
        FROM frpm
    """)
    keys = keys.dropna().drop_duplicates()
    keys = keys.sem_map(("What is the school Charter Funding Type? district_school_key: {district_school_key}" + " Answer with the value only, without any other words."),
                        suffix="FundingType")
    keys["FundingType"] = keys["FundingType"].str.strip()
    return db.sql("""
        WITH temp2 AS (
            SELECT frpm.*, m.FundingType
            FROM frpm
            LEFT JOIN m ON m.district_school_key =
                'District: ' || frpm."District Name" || ' and School: ' || frpm."School Name"
        )
        SELECT T1.sname, temp2.FundingType
        FROM satscores AS T1 INNER JOIN temp2 ON T1.cds = temp2.CDSCode
        WHERE temp2."District Name" LIKE 'Riverside%'
        GROUP BY T1.sname, temp2.FundingType
        HAVING CAST(SUM(T1.AvgScrMath) AS REAL) / COUNT(T1.cds) > 400
    """, m=keys[["district_school_key", "FundingType"]])
