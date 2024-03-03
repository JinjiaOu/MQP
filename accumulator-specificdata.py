import json
import math
import os

base_input_dir = r"C:\Users\vainglory\IdeaProjects\MQP\json_data"
base_output_dir = r"C:\Users\vainglory\IdeaProjects\MQP\accumulation_specific_data"

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

    for player in data:
        round_num = player['Rnd']
        position = player['Pos']
        av = player.get('Weighted Career Approximate Value')
        games_played = player.get('Games played')
        
        # Other stats
        stats = {
            'Passes completed': player.get('Passes completed'),
            'Passes attempted': player.get('Passes attempted'),
            'Yards Gained by Passing': player.get('Yards Gained by Passing'),
            'Passing Touchdowns': player.get('Passing Touchdowns'),
            'Interceptions thrown': player.get('Interceptions thrown'),
            'Rushing Attempts': player.get('Rushing Attempts'),
            'Rushing Yards Gained': player.get('Rushing Yards Gained'),
            'Rushing Touchdowns': player.get('Rushing Touchdowns'),
            'Receptions': player.get('Receptions'),
            'Receiving Yards': player.get('Receiving Yards'),
            'Receiving Touchdowns': player.get('Receiving Touchdowns')
        }

        # Initialize round if not exists
        if round_num not in round_totals:
            round_totals[round_num] = {
                'positions': {},
                'total_round_stats': {'total_av': 0, 'total_games': 0, 'position_counts': {}}
            }

        # Initialize position if not exists
        if position not in round_totals[round_num]['positions']:
            round_totals[round_num]['positions'][position] = {stat: 0 for stat in stats}
            # Initialize position count
            round_totals[round_num]['total_round_stats']['position_counts'][position] = 0

        # Increment position count
        round_totals[round_num]['total_round_stats']['position_counts'][position] += 1

        # Accumulate total round stats for AV and games played
        if av is not None and not (isinstance(av, float) and math.isnan(av)):
            round_totals[round_num]['total_round_stats']['total_av'] += av

        if games_played is not None and not (isinstance(games_played, float) and math.isnan(games_played)):
            round_totals[round_num]['total_round_stats']['total_games'] += games_played

        # Accumulate statistics for each position
        for stat, value in stats.items():
            if value is not None and not (isinstance(value, float) and math.isnan(value)):
                round_totals[round_num]['positions'][position][stat] += value

    output_data = {
        "Year": str(year),
        "Type": "Total AV, Games Played, Number of Each Position per Round, Detailed Stats per Position",
        "Data": round_totals
    }

    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Total AV, games played, number of each position per round, detailed stats per position for the year {year} written to '{output_file_path}'")