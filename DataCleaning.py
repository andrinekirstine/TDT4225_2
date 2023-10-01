import os
from pathlib import Path
import shutil

# Read file, reads from line 6 then write it without the 6 first lines
def remove_lines(output_file_path: Path, remove_line: int):
    with open(output_file_path, 'r') as file:
        lines = file.readlines()[remove_line:]
    with open(output_file_path, 'w') as file:
        file.writelines(lines)


# Read file, split it into lines, then by coulmn. Delete field 5 then 3 for every line
def remove_columns(output_file_path: Path):        
    with open(output_file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []

    for line in lines:
        coulmn = line.strip().split(',')
        
        # Delete 5 first bc else index moves
        del coulmn[5]  
        del coulmn[3]
        
        modified_line = ','.join(coulmn)
        modified_lines.append(modified_line)

    with open(output_file_path, 'w') as file:
        file.writelines('\n'.join(modified_lines))


# Read file, split it into lines, then by coulmn. Merge field 3 and 4 (old 6&7) then delete 4 (old 7)
def column_merger(output_file_path: Path):
    with open(output_file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []

    for line in lines:
        coulmn = line.strip().split(',')
        
        coulmn[3] = coulmn[3] + " " + coulmn[4]
        del coulmn[4]
        
        modified_line = ','.join(coulmn)
        modified_lines.append(modified_line)

    with open(output_file_path, 'w') as file:
        file.writelines('\n'.join(modified_lines))


# Check how many lines a file has and returns the length
def check_length(output_file_path: Path) -> int:
    with open(output_file_path, 'r') as file:
        lines = file.readlines()    
    
    return len(lines)

# Delete a file 
def delete_file(output_file_path: Path):
    output_file_path.unlink()
    print(output_file_path," files is deleted")


# Function to process a single file, if a file has more than 2500 lines it will be deleted
def process_file(input_file_path: Path, output_file_path: Path):
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_file_path, output_file_path)
    
    remove_lines(output_file_path, 6)
    if check_length(output_file_path) > 2500:
        return delete_file(output_file_path)
    remove_columns(output_file_path)
    column_merger(output_file_path)


# Function to process all files in a folder
def process_folder(input_folder: Path, output_folder: Path):
    os.makedirs(output_folder, exist_ok=True)
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_file_path = Path(os.path.join(root, file))
            output_file_path = Path(os.path.join(output_folder, input_file_path.parent.parent.name, file))
            process_file(input_file_path, output_file_path)

process_folder(Path("dataset/in/Data"), Path("dataset/out/Data"))