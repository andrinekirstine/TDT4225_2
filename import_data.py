from walk_dataset import walk_dataset
from pathlib import Path
from datetime import datetime
from Connect import create_database_connection

def get_users_with_labels(data_directory: Path) -> set:
    labeled_ids = Path(data_directory, "labeled_ids.txt").read_text()
    return set(labeled_ids.split())

LABELS_DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

def get_labels(user_dir: Path):
    labels_path = user_dir / "labels.txt"
    if not labels_path.exists():
        return None        
    labels = list()

    for label in labels_path.read_text().split("\n")[1:-1]:
        label = label.split("\t")
        labels.append(dict(
            start_time=datetime.strptime(label[0], LABELS_DATETIME_FORMAT),
            end_time=datetime.strptime(label[1], LABELS_DATETIME_FORMAT),
            mode=label[2]
        ))
    return labels

def add_activity(mysql_connection, user_id: str, data_file: Path, labels):
    print(f"Creating new activity for {user_id}, {data_file}")
    cursor = mysql_connection.cursor()
    cursor.execute("INSERT INTO Activity(user_id) VALUES (%s)", (user_id,))
    activity_id = cursor.lastrowid
    cursor.execute("LOAD DATA LOCAL INFILE %s INTO TABLE TrackPoint FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (lat, lon, altitude, date_time) SET activity_id=%s", (str(data_file), activity_id))
    cursor.execute("SELECT MIN(date_time) AS start_time, MAX(date_time) AS end_time FROM TrackPoint WHERE activity_id = %s", (activity_id,))
    start_time, end_time = cursor.fetchone()
    print(start_time, end_time)
    mode_of_transport = None
    if labels is not None:
        for l in labels:
            if l["start_time"] == start_time and l["end_time"] == end_time:
                mode_of_transport = l["mode"]

    
    cursor.execute("UPDATE Activity SET start_date_time = %s, end_date_time = %s, transportation_mode = %s WHERE activity_id = %s", (start_time, end_time, mode_of_transport, activity_id))
    connection.commit()


def import_data_to_mysql(mysql_connection, data_directory: Path):
    with open(".completed_users", "r+") as fh:
        completed_users = fh.read().split()
    with open(".completed_files", "r+") as fh:
        completed_files = fh.read().split()
    print(completed_files, completed_users)
    print(f"Importing from {data_directory}")
    for file, user in walk_dataset(data_directory):
        if user in completed_users:
            continue
        if file in completed_files:
            continue

        file = data_directory / file
        labels = get_labels(file.parent.parent)
        add_activity(mysql_connection, user, file, labels)
        with open(".completed_files", "a+") as fh:
            fh.write(f"{file}\n")
            


if __name__ == "__main__":
    import sys
    connection = create_database_connection()
    try:
        for folder in sys.argv[1:]:
            import_data_to_mysql(connection, Path(folder))
    finally:
        connection.close()