import json
import math
import os

base_input_dir = r"C:\Users\vainglory\IdeaProjects\MQP\not_empty"
output_file_path = r"C:\Users\vainglory\IdeaProjects\MQP\percentages_data_with_noEmpty\total.json"

total_games_per_round = {}

for year in range(2000, 2024):
    input_file_path = os.path.join(base_input_dir, f"{year}.json")

    if not os.path.exists(input_file_path):
        print(f"No data file for the year {year}. Skipping...")
        continue

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    for player in data:
        round_num = player['Rnd']
        games_played = player.get('Games played')

        if round_num not in total_games_per_round:
            total_games_per_round[round_num] = 0

        if games_played is not None and not (isinstance(games_played, float) and math.isnan(games_played)):
            total_games_per_round[round_num] += games_played

# Calculate the total games played across all rounds and years
total_games_played = sum(total_games_per_round.values())

# Calculate and store the percentage of games played for each round
for round_num in total_games_per_round:
    games_in_round = total_games_per_round[round_num]
    percentage = (games_in_round / total_games_played) * 100 if total_games_played > 0 else 0
    total_games_per_round[round_num] = {
        'total_games': games_in_round,
        'percentage_of_total': percentage
    }

# Add the total games played to the output
total_games_per_round['total_games_played'] = total_games_played

# Write the total games per round across all years to a single file
with open(output_file_path, 'w') as outfile:
    json.dump(total_games_per_round, outfile, indent=4)

print(f"Total games played per round across all years, including the overall total and percentages, written to '{output_file_path}'")
