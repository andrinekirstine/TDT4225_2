import mysql.connector as mysql
from mysql.connector import Error
from pathlib import Path
import sys
from Connect import create_database_connection

if __name__ == "__main__":
    queries = list(map(Path, sys.argv[1:]))

    connection = create_database_connection()
    cursor = connection.cursor()
    for query in queries:
        print(f"Running {query}")
        query = query.read_text()
        for result in cursor.execute(query, multi=True):
            if result.with_rows:
                print(result.statement)
                print(result.fetchall())
        
    connection.close()