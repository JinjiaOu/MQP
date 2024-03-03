import os
import json
from collections import defaultdict

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def process_files(directory, new_directory):
    player_first_appearance = defaultdict(str)
    files_to_process = []

    # First pass: Identify first appearance of each player
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                data = read_json_file(file_path)
                for entry in data:
                    player = entry.get("Player")
                    if player and player not in player_first_appearance:
                        player_first_appearance[player] = filename
                files_to_process.append((filename, data))
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Second pass: Remove repeated player entries and write to new directory
    for filename, data in files_to_process:
        modified_data = [entry for entry in data if player_first_appearance[entry.get("Player")] == filename]
        new_file_path = os.path.join(new_directory, filename)
        write_json_file(modified_data, new_file_path)

# Directory paths
input_directory = "E:\\IdeaProjects\\MQP\\undrafted_data_json"
output_directory = "E:\\IdeaProjects\\MQP\\new_drafted"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

process_files(input_directory, output_directory)
print("Processing complete. Modified files are saved in the new directory.")
