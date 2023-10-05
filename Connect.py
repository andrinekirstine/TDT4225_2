import mysql.connector as mysql
from mysql.connector import Error

def send_query(message: str, query: str):
    execute = cursor.execute(query)

    if execute != None:
        connection.commit()
        print(message)
    else:
        print("Could not send query")

label_list = ["010","020","021","052","053","056","058","059","060","062","064","065",
"067","068","069","073","075","076","078","080","081","082","084","085","086","087","088",
"089","091","092","096","097","098","100","101","102","104","105","106","107","108","110",
"111","112","114","115","116","117","118","124","125","126","128","129","136","138","139",
"141","144","147","153","154","161","163","167","170","174","175","179"]

def set_users():
    user_list = []
    for i in range(182):
        user = { "_id": "", "hasLabel": False} 
        if i < 10:
            user["_id"] = "00" + str(i)
        elif i < 100:
            user["_id"] = "0" + str(i)
        else:
            user["_id"] = str(i)
        
        if user["_id"] in label_list:
            user["hasLabel"] = True

        user_list.append(user)
    
    #print(user_list)
    return user_list



def add_users():
    user_list: [] = set_users()

    for user in user_list:
        user_id: [] = user["_id"]
        has_label: [] = user["hasLabel"]

        sql = "INSERT INTO User (user_id, has_labels) VALUES (%s, %s);"
        val = (user_id, has_label)

        execute = cursor.execute(sql, val, multi=True)

        if execute != None:
            connection.commit()
            print(user["_id"], " user added")
        else:
            print("Could not add users")
     


try:
    connection = mysql.connect(host='localhost',
                                database='test1',
                                user='root',
                                password='mysql-password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        send_query("user table", """
            CREATE TABLE IF NOT EXISTS User (
                user_id VARCHAR(3) PRIMARY KEY,
                has_labels BOOLEAN
            )
            """)
        send_query("activity table ", """
                CREATE TABLE IF NOT EXISTS Activity (
                    activity_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(3),
                    FOREIGN KEY (user_id) REFERENCES User(user_id),
                    transportation_mode VARCHAR(25),
                    start_date_time DATETIME,
                    end_date_time DATETIME
                )
                """)
        send_query("trackpoint table","""
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
        add_users()
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")