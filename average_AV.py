import json
import math
import os

base_input_dir = r"C:\Users\vainglory\IdeaProjects\MQP\json_data"
base_output_dir = r"C:\Users\vainglory\IdeaProjects\MQP\average_AV"

for year in range(2000, 2024):
    input_file_path = os.path.join(base_input_dir, f"{year}.json")
    output_file_path = os.path.join(base_output_dir, f"average_av_per_round_{year}.json")

    if not os.path.exists(input_file_path):
        print(f"No data file for the year {year}. Skipping...")
        continue

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    round_av = {}

    for player in data:
        round_num = player['Rnd']
        av = player.get('Weighted Career Approximate Value')

        # Skip if AV is NaN or missing
        if av is None or (isinstance(av, float) and math.isnan(av)):
            continue

        if round_num not in round_av:
            round_av[round_num] = {'total_av': 0, 'count': 0}

        round_av[round_num]['total_av'] += av
        round_av[round_num]['count'] += 1

    average_av_per_round = {}
    for rnd, round_data in round_av.items():
        count = round_data['count']
        if count > 0:
            average_av_per_round[rnd] = round_data['total_av'] / count
        else:
            average_av_per_round[rnd] = None

    output_data = {
        "Year": str(year),
        "Type": "Average Approximate Value per Round",
        "Data": average_av_per_round
    }

    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Average AV per round for the year {year} written to '{output_file_path}'")
