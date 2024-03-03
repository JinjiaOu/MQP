import json
import os
import math

def is_valid_number(value):
    try:
        return not math.isnan(float(value))
    except (ValueError, TypeError):
        return False

base_input_dir = r"C:\Users\vainglory\IdeaProjects\MQP\json_data"
base_output_dir = r"C:\Users\vainglory\IdeaProjects\MQP\position_total"

# Create the output directory if it doesn't exist
if not os.path.exists(base_output_dir):
    os.makedirs(base_output_dir)

for year in range(2000, 2024):
    input_file_path = os.path.join(base_input_dir, f"{year}.json")
    output_file_path = os.path.join(base_output_dir, f"{year}.json")

    if not os.path.exists(input_file_path):
        print(f"No data file for the year {year}. Skipping...")
        continue

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    round_totals = {}
    round_percentages = {}

    for player in data:
        round_num = player['Rnd']
        position = player['Pos']
        games_played = player.get('Games played')

        # Initialize round if not exists
        if round_num not in round_totals:
            round_totals[round_num] = {
                'positions': {},
                'total_games': 0
            }

        # Initialize position if not exists
        if position not in round_totals[round_num]['positions']:
            round_totals[round_num]['positions'][position] = 0

        # Add games played to the total for the position, ignoring NaN values
        if games_played is not None and is_valid_number(games_played):
            round_totals[round_num]['positions'][position] += games_played
            round_totals[round_num]['total_games'] += games_played

    # Calculate the percentage of games played for each position in each round
    for round_num, round_data in round_totals.items():
        total_games_in_round = round_data['total_games']
        round_percentages[round_num] = {
            position: (games / total_games_in_round) * 100
            for position, games in round_data['positions'].items()
        }

    output_data = {
        "Year": str(year),
        "Type": "Total Games Played by Position per Round with Percentages",
        "Data": round_totals,
        "Round Percentages": round_percentages
    }

    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Data for the year {year} written to '{output_file_path}'")
