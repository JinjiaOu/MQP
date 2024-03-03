import json
import math
import os

# Directories for input and output data
base_input_dir = r"E:\IdeaProjects\MQP\json_data"
undrafted_input_dir = r"E:\IdeaProjects\MQP\new_drafted"
base_output_dir = r"E:\IdeaProjects\MQP\ss"

cumulative_data = {}
draft_pick_data = {}

total_av_undrafted = 0
total_games_undrafted = 0

for year in range(2000, 2024):
    input_file_path = os.path.join(base_input_dir, f"{year}.json")
    undrafted_file_path = os.path.join(undrafted_input_dir, f"{year}.json")
    output_file_path = os.path.join(base_output_dir, f"{year}.json")

    if not os.path.exists(input_file_path):
        print(f"No data file for the year {year}. Skipping...")
        continue

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    round_totals = {}
    round_player_count = {}
    total_games_for_year = 0
    total_av_for_year = 0
    total_av_undrafted_year = 0
    total_games_undrafted_year = 0
    total_av_drafted_year = 0
    total_games_drafted_year = 0

    for player in data:
        av = player.get('Weighted Career Approximate Value')
        games_played = player.get('Games played')
        draft_pick = player.get('Pick')

        if all(math.isnan(x) if isinstance(x, float) else False for x in [av, games_played]):
            continue

        round_num = player['Rnd']
        if round_num not in round_totals:
            round_totals[round_num] = {'total_av': 0, 'total_games': 0}
        if round_num not in round_player_count:
            round_player_count[round_num] = 0
        round_player_count[round_num] += 1
        if av is not None and not math.isnan(av):
            round_totals[round_num]['total_av'] += av
            total_av_drafted_year += av
            total_av_for_year += av
        if games_played is not None and not math.isnan(games_played):
            round_totals[round_num]['total_games'] += games_played
            total_games_drafted_year += games_played
            total_games_for_year += games_played

        if draft_pick is not None:
            if draft_pick not in draft_pick_data:
                draft_pick_data[draft_pick] = {'total_av': 0, 'total_games': 0, 'count': 0}
            if av is not None and not math.isnan(av):
                draft_pick_data[draft_pick]['total_av'] += av
            if games_played is not None and not math.isnan(games_played):
                draft_pick_data[draft_pick]['total_games'] += games_played
            draft_pick_data[draft_pick]['count'] += 1

    if os.path.exists(undrafted_file_path):
        with open(undrafted_file_path, 'r') as undrafted_file:
            undrafted_data = json.load(undrafted_file)

        for player in undrafted_data:
            g = player.get('G')
            av = player.get('AV')

            if g is not None and not math.isnan(g):
                total_games_undrafted_year += g
                total_games_undrafted += g
            if av is not None and not math.isnan(av):
                total_av_undrafted_year += av
                total_av_undrafted += av

        total_games_for_year += total_games_undrafted_year
        total_av_for_year += total_av_undrafted_year

    undrafted_percentage_data = {
        'games_percentage': (total_games_undrafted_year / total_games_for_year) * 100 if total_games_for_year > 0 else 0,
        'av_percentage': (total_av_undrafted_year / total_av_for_year) * 100 if total_av_for_year > 0 else 0
    }
    round_totals['Undrafted Percentages'] = undrafted_percentage_data

    for round_num in round_totals:
        if not isinstance(round_num, int):  # Skip non-integer round numbers
            continue

        round_av = round_totals[round_num]['total_av']
        round_games = round_totals[round_num]['total_games']
        round_totals[round_num]['av_percentage'] = (round_av / total_av_for_year) * 100 if total_av_for_year > 0 else 0
        round_totals[round_num]['games_percentage'] = (round_games / total_games_for_year) * 100 if total_games_for_year > 0 else 0

    output_data = {
        "Year": str(year),
        "Type": "Total AV and Games Played per Round with Percentages",
        "Round Data": round_totals,
        "Total Games Played for the Year": total_games_for_year,
        "Total AV for the Year": total_av_for_year,
        "Total Games Played by Drafted Players": total_games_drafted_year,
        "Total AV for Drafted Players": total_av_drafted_year,
        "Total Games Played by Undrafted Players": total_games_undrafted_year,
        "Total AV for Undrafted Players": total_av_undrafted_year
    }

    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    for round_num, data in round_totals.items():
        if not isinstance(round_num, int):  # Skip non-integer round numbers
            continue

        if round_num not in cumulative_data:
            cumulative_data[round_num] = {'total_av': 0, 'total_games': 0, 'total_players': 0}
        cumulative_data[round_num]['total_av'] += data['total_av']
        cumulative_data[round_num]['total_games'] += data['total_games']
        cumulative_data[round_num]['total_players'] += round_player_count.get(round_num, 0)

for pick, data in draft_pick_data.items():
    count = data['count']
    data['average_av'] = data['total_av'] / count if count > 0 else 0
    data['average_games'] = data['total_games'] / count if count > 0 else 0

# Calculate overall totals before using them
total_av_all = sum(d['total_av'] for d in cumulative_data.values()) + total_av_undrafted
total_games_all = sum(d['total_games'] for d in cumulative_data.values()) + total_games_undrafted

cumulative_undrafted_data = {
    'total_av': total_av_undrafted,
    'total_games': total_games_undrafted,
    'av_percentage': (total_av_undrafted / total_av_all) * 100 if total_av_all > 0 else 0,
    'games_percentage': (total_games_undrafted / total_games_all) * 100 if total_games_all > 0 else 0
}
cumulative_data['Undrafted'] = cumulative_undrafted_data

for round_num, data in cumulative_data.items():
    if not isinstance(round_num, int):  # Skip non-integer round numbers
        continue

    if data['total_players'] > 0:
        data['average_av'] = data['total_av'] / data['total_players']
    else:
        data['average_av'] = 0

    data['av_percentage'] = (data['total_av'] / total_av_all) * 100 if total_av_all > 0 else 0
    data['games_percentage'] = (data['total_games'] / total_games_all) * 100 if total_games_all > 0 else 0

cumulative_round_output_data = {
    "Type": "Cumulative Round Data with Percentages",
    "Cumulative Round Data": cumulative_data,
    "Overall Total AV": total_av_all,
    "Overall Total Games Played": total_games_all
}

cumulative_round_output_path = os.path.join(base_output_dir, "cumulative_round_data_with_undrafted.json")
with open(cumulative_round_output_path, 'w') as round_outfile:
    json.dump(cumulative_round_output_data, round_outfile, indent=4)

print(f"Cumulative round data with undrafted players written to '{cumulative_round_output_path}'")
