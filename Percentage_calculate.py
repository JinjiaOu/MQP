import json
import math
import os

base_input_dir = r"C:\Users\vainglory\IdeaProjects\MQP\json_data"
base_output_dir = r"C:\Users\vainglory\IdeaProjects\MQP\cumulative_round_data"
cumulative_data = {}
draft_pick_data = {}

for year in range(2000, 2024):
    input_file_path = os.path.join(base_input_dir, f"{year}.json")
    output_file_path = os.path.join(base_output_dir, f"{year}.json")

    if not os.path.exists(input_file_path):
        print(f"No data file for the year {year}. Skipping...")
        continue

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    round_totals = {}
    total_games_for_year = 0
    total_av_for_year = 0

    for player in data:
        av = player.get('Weighted Career Approximate Value')
        games_played = player.get('Games played')
        draft_pick = player.get('Pick')

        # Skip players who never played
        if all(math.isnan(x) if isinstance(x, float) else False for x in [av, games_played]):
            continue

        # Round data
        round_num = player['Rnd']
        if round_num not in round_totals:
            round_totals[round_num] = {'total_av': 0, 'total_games': 0}
        if av is not None and not math.isnan(av):
            round_totals[round_num]['total_av'] += av
            total_av_for_year += av
        if games_played is not None and not math.isnan(games_played):
            round_totals[round_num]['total_games'] += games_played
            total_games_for_year += games_played

        # Draft pick data
        if draft_pick is not None:
            if draft_pick not in draft_pick_data:
                draft_pick_data[draft_pick] = {'total_av': 0, 'total_games': 0, 'count': 0}
            if av is not None and not math.isnan(av):
                draft_pick_data[draft_pick]['total_av'] += av
            if games_played is not None and not math.isnan(games_played):
                draft_pick_data[draft_pick]['total_games'] += games_played
            draft_pick_data[draft_pick]['count'] += 1

    # Calculating percentages for round data
    for round_num in round_totals:
        round_av = round_totals[round_num]['total_av']
        round_games = round_totals[round_num]['total_games']
        round_totals[round_num]['av_percentage'] = (round_av / total_av_for_year) * 100 if total_av_for_year > 0 else 0
        round_totals[round_num]['games_percentage'] = (round_games / total_games_for_year) * 100 if total_games_for_year > 0 else 0

    # Preparing output data for the year
    output_data = {
        "Year": str(year),
        "Type": "Total AV and Games Played per Round with Percentages",
        "Round Data": round_totals,
        "Total Games Played for the Year": total_games_for_year,
        "Total AV for the Year": total_av_for_year
    }

    # Writing to output file for the year
    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    # Update cumulative data
    for round_num, data in round_totals.items():
        if round_num not in cumulative_data:
            cumulative_data[round_num] = {'total_av': 0, 'total_games': 0}
        cumulative_data[round_num]['total_av'] += data['total_av']
        cumulative_data[round_num]['total_games'] += data['total_games']

# Calculate averages for each draft pick
for pick, data in draft_pick_data.items():
    count = data['count']
    data['average_av'] = data['total_av'] / count if count > 0 else 0
    data['average_games'] = data['total_games'] / count if count > 0 else 0

# Calculating percentages for cumulative round data
for round_num, data in cumulative_data.items():
    total_av = sum(d['total_av'] for d in cumulative_data.values())
    total_games = sum(d['total_games'] for d in cumulative_data.values())
    data['av_percentage'] = (data['total_av'] / total_av) * 100 if total_av > 0 else 0
    data['games_percentage'] = (data['total_games'] / total_games) * 100 if total_games > 0 else 0

# Writing the cumulative round data with percentages
cumulative_round_output_data = {
    "Type": "Cumulative Round Data with Percentages",
    "Cumulative Round Data": cumulative_data
}
cumulative_round_output_path = os.path.join(base_output_dir, "cumulative_round_data.json")
with open(cumulative_round_output_path, 'w') as round_outfile:
    json.dump(cumulative_round_output_data, round_outfile, indent=4)

# Writing the cumulative draft pick data
cumulative_draft_pick_output_data = {
    "Type": "Cumulative Draft Pick Data",
    "Cumulative Draft Pick Data": draft_pick_data
}
cumulative_draft_pick_output_path = os.path.join(base_output_dir, "cumulative_draft_pick_data.json")
with open(cumulative_draft_pick_output_path, 'w') as draft_pick_outfile:
    json.dump(cumulative_draft_pick_output_data, draft_pick_outfile, indent=4)

print(f"Cumulative round data written to '{cumulative_round_output_path}'")
print(f"Cumulative draft pick data written to '{cumulative_draft_pick_output_path}'")
