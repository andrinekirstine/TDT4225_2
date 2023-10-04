import mysql.connector as mysql
from mysql.connector import Error

def add_table(name: str, query: str):
    execute = cursor.execute(query)

    if execute != None:
        connection.commit()
        print(name," table added")
    else:
        print("Could not create table")



try:
    connection = mysql.connect(host='localhost',
                                database='sdd_1',
                                user='root',
                                password='mysql-password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        add_table("user", """
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL,
                has_labels BOOLEAN
            )
            """)
        add_table("activity", """
                CREATE TABLE IF NOT EXISTS Activity (
                    id SERIAL,
                    user_id VARCHAR(255),
                    transportation_mode VARCHAR(25),
                    start_date_time DATETIME,
                    end_date_time DATETIME
                )
                """)
        add_table("trackpoint","""
                CREATE TABLE IF NOT EXISTS TrackPoint (
                    id SERIAL,
                    activity_id VARCHAR(255),
                    lat DOUBLE,
                    lon DOUBLE,
                    altitude INT,
                    date_time DATETIME
                )
                """)
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")