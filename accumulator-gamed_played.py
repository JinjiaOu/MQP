import json
import math
import os

base_input_dir = r"C:\Users\vainglory\IdeaProjects\MQP\json_data"
base_output_dir = r"C:\Users\vainglory\IdeaProjects\MQP\accumulation_data"

for year in range(2000, 2024):
    input_file_path = os.path.join(base_input_dir, f"{year}.json")
    output_file_path = os.path.join(base_output_dir, f"{year}.json")

    if not os.path.exists(input_file_path):
        print(f"No data file for the year {year}. Skipping...")
        continue

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    round_totals = {}

    for player in data:
        round_num = player['Rnd']
        av = player.get('Weighted Career Approximate Value')
        games_played = player.get('Games played')

        if round_num not in round_totals:
            round_totals[round_num] = {'total_av': 0, 'total_games': 0}

        # Accumulate AV
        if av is not None and not (isinstance(av, float) and math.isnan(av)):
            round_totals[round_num]['total_av'] += av

        # Accumulate games played
        if games_played is not None and not (isinstance(games_played, float) and math.isnan(games_played)):
            round_totals[round_num]['total_games'] += games_played

    output_data = {
        "Year": str(year),
        "Type": "Total AV and Games Played per Round",
        "Data": round_totals
    }

    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Total AV and games played per round for the year {year} written to '{output_file_path}'")