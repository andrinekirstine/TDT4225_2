import mysql.connector as mysql
from mysql.connector import Error
from dotenv import load_dotenv
import os

def send_query(connection, message: str, query: str):
    cursor = connection.cursor()
    cursor.execute(query)

    connection.commit()
    print(message)

label_list = ["010","020","021","052","053","056","058","059","060","062","064","065",
"067","068","069","073","075","076","078","080","081","082","084","085","086","087","088",
"089","091","092","096","097","098","100","101","102","104","105","106","107","108","110",
"111","112","114","115","116","117","118","124","125","126","128","129","136","138","139",
"141","144","147","153","154","161","163","167","170","174","175","179"]

def set_users():
    user_list = []
    for i in range(182):
        user = { "_id": f"{i:03}", "hasLabel": False} 
        if user["_id"] in label_list:
            user["hasLabel"] = True

        user_list.append(user)
    
    #print(user_list)
    return user_list



def add_users(connection):
    user_list: list = set_users()
    cursor = connection.cursor()
    # Inserts a new User if one does not exist, if it does it updates it.
    sql = """INSERT INTO User (user_id, has_labels)
        VALUES (%(_id)s, %(hasLabel)s)
        ON DUPLICATE KEY UPDATE has_labels = %(hasLabel)s
    """

    for user in user_list:
        cursor.execute(sql, user)

    connection.commit()
    print("Users added successfully")

def create_database_connection():
    load_dotenv()
    return mysql.connect(
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        allow_local_infile=True
    )

def run_migration():
    try:
        connection = create_database_connection()
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            send_query(connection, "user table", """
                CREATE TABLE IF NOT EXISTS User (
                    user_id VARCHAR(3) PRIMARY KEY,
                    has_labels BOOLEAN
                )
                """)
            send_query(connection, "activity table ", """
                    CREATE TABLE IF NOT EXISTS Activity (
                        activity_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(3),
                        FOREIGN KEY (user_id) REFERENCES User(user_id),
                        transportation_mode VARCHAR(25),
                        start_date_time DATETIME,
                        end_date_time DATETIME
                    )
                    """)
            send_query(connection, "trackpoint table","""
                    CREATE TABLE IF NOT EXISTS TrackPoint (
                        trackpoint_id INT AUTO_INCREMENT PRIMARY KEY,
                        activity_id INT,
                        FOREIGN KEY (activity_id) REFERENCES Activity(activity_id),
                        lat DOUBLE,
                        lon DOUBLE,
                        altitude INT,
                        date_time DATETIME
                    )
                    """)      
            add_users(connection)
    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    run_migration()