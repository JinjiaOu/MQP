import matplotlib.pyplot as plt
import json

# The path to the JSON file in your environment
json_file_path = 'E:\\IdeaProjects\\MQP\\chart\\cumulative_round_data_with_undrafted.json'

# The path to the folder where charts will be saved
output_folder_path = 'E:\\IdeaProjects\\MQP\\new_chart\\'

# Reading the JSON data from the file
with open(json_file_path, 'r') as file:
    data = json.load(file)['Cumulative Round Data']

# Extracting data for the charts
rounds = list(data.keys())[:-1]  # Excluding 'Undrafted' for first two charts
undrafted_included_rounds = list(data.keys())  # Including 'Undrafted' for last two charts

# Data for Chart 1 and 2 (Excluding Undrafted)
average_av = [data[round]['average_av'] for round in rounds]
av_percentage = [data[round]['av_percentage'] for round in rounds]
average_games = [data[round]['total_games'] / data[round]['total_players'] for round in rounds]
games_percentage = [data[round]['games_percentage'] for round in rounds]

# Data for Chart 3 and 4 (Including Undrafted)
total_av = [data[round]['total_av'] for round in undrafted_included_rounds]
total_av_percentage = [data[round]['av_percentage'] for round in undrafted_included_rounds]
total_games = [data[round]['total_games'] for round in undrafted_included_rounds]
total_games_percentage = [data[round]['games_percentage'] for round in undrafted_included_rounds]

# Function to create and save a chart with connective lines for percentages and data values on bars
def create_and_save_chart_with_line_and_values(data, percentages, title, xlabel, ylabel, bar_color, line_color, alpha, label, rounds, output_filename):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar chart
    bars = ax1.bar(rounds, data, color=bar_color, alpha=alpha, label=label)
    
    # Adding data values on each bar
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    # Connective line for percentages
    ax2 = ax1.twinx()
    ax2.plot(rounds, percentages, color=line_color, label='Percentage', marker='o')
    for i, txt in enumerate(percentages):
        ax2.annotate(f"{txt:.2f}%", (rounds[i], percentages[i]), textcoords="offset points", xytext=(0,-15), ha='center', va='top')

    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax2.set_ylabel('Percentage (%)')
    plt.title(title)
    
    # Repositioning the legends using bbox_to_anchor
    ax1.legend(loc='upper left', bbox_to_anchor=(0.4, 1.0))
    ax2.legend(loc='upper left', bbox_to_anchor=(0.4, 0.9))

    plt.savefig(output_folder_path + output_filename)
    plt.close()

# Creating and saving each chart with connective line and data values on bars
create_and_save_chart_with_line_and_values(average_av, av_percentage, 'Average AV per Round', 'Draft Round', 'Average AV', 'blue', 'red', 0.6, 'Average AV', rounds, 'average_av_per_round.png')
create_and_save_chart_with_line_and_values(average_games, games_percentage, 'Average Games Played per Round', 'Draft Round', 'Average Games Played', 'green', 'red', 0.6, 'Average Games Played', rounds, 'average_games_per_round.png')
create_and_save_chart_with_line_and_values(total_av, total_av_percentage, 'Total AV per Round (Including Undrafted)', 'Draft Round', 'Total AV', 'red', 'blue', 0.6, 'Total AV', undrafted_included_rounds, 'total_av_including_undrafted.png')
create_and_save_chart_with_line_and_values(total_games, total_games_percentage, 'Total Games Played per Round (Including Undrafted)', 'Draft Round', 'Total Games Played', 'purple', 'blue', 0.6, 'Total Games Played', undrafted_included_rounds, 'total_games_including_undrafted.png')
