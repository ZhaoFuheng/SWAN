import sqlite3
import time
import sys
import os

def execute_query(db_path, sql, output):
    #print("in execute query")
    try:
        conn = sqlite3.connect(db_path, uri=True)
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        output.put_nowait(result)
    except Exception as e:
        # Raise an exception with additional error information
        output.put_nowait(Exception(f"An error occurred during SQL execution: {str(e)}"))
    finally:
        cursor.close()
        conn.close()
    return
