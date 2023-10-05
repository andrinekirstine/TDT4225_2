
## Trackpoints er good så der må vi bare kjøre query per fil
# trenger en func for å gå gjennom hver fil

from pathlib import Path


def add_trackpoints():
    return None


## Actvitity trenger vi et object per fil med trackpoints 
# Foreach vibe
# Lage en func som tar inn en fil, legger inn bruker ID'en basert på mappa
# Så legger den til en ny activity per fil og gir ID'en vidre til alle TP's som blir adda fra fila


def remove_columns(output_file_path: Path):        
    with open(output_file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []

    for line in lines:
        coulmn = line.strip().split(',')
        
        # Delete 5 first bc else index moves
        del coulmn[4]  
        del coulmn[2]
        
        modified_line = ','.join(coulmn)
        modified_lines.append(modified_line)

    with open(output_file_path, 'w') as file:
        file.writelines('\n'.join(modified_lines))


def process_file(input_file_path: Path, output_file_path: Path):
    print(f"processing: {input_file_path} -> {output_file_path}")
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_file_path, output_file_path)
    
    if input_file_path.suffix != ".plt":
        return
    
    remove_lines(output_file_path, 6)
    
    if check_length(output_file_path) > 2500:
        delete_file(output_file_path)
        return
    remove_columns(output_file_path)
    column_merger(output_file_path)












def process_folder(folder_path, db_connection):
    cursor = db_connection.cursor()

    for subfolder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder_name)

        if os.path.isdir(subfolder_path):
            # Assuming create_object_in_table() is the function to create object in MySQL table
            create_object_in_table(subfolder_name, cursor)

            for file_name in os.listdir(subfolder_path):
                if file_name.endswith(".csv"):  # Assuming you're processing CSV files
                    file_path = os.path.join(subfolder_path, file_name)

                    # Assuming load_data_infile() is the function to load data into MySQL table
                    load_data_infile(file_path, cursor)

    db_connection.commit()

def create_object_in_table(id, cursor):
    # Your code to create an object in MySQL table using the provided id
    pass

def load_data_infile(file_path, cursor):
    # Your code to execute "LOAD DATA INFILE" statement with the provided file_path
    pass

# Example Usage:
connection = mysql.connector.connect(
    host='your_host',
    user='your_user',
    password='your_password',
    database='your_database'
)

folder_path = '/path/to/your/folder'
process_folder(folder_path, connection)

# Don't forget to close the connection when you're done
connection.close()
