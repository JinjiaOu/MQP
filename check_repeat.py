import os
import json
from collections import defaultdict

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def find_repeated_players(directory):
    player_files = defaultdict(set)

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                data = read_json_file(file_path)
                for entry in data:
                    player = entry.get("Player")
                    if player:
                        player_files[player].add(filename)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return {player: files for player, files in player_files.items() if len(files) > 1}

# Replace this with the path to your directory
directory_path = "E:\\IdeaProjects\\MQP\\undrafted_data_json"

repeated_players = find_repeated_players(directory_path)
print("Players who appear more than once and their corresponding files:")
for player, files in repeated_players.items():
    print(f"{player}: {', '.join(files)}")
