import matplotlib.pyplot as plt
import json

# Assuming the JSON file paths are defined
json_file_path = 'E:\\IdeaProjects\\MQP\\chart\\cumulative_round_data_with_undrafted.json'
draft_value_file_path = 'E:\\IdeaProjects\\MQP\\chart\\Draft Value.json'
salary_file_path = 'E:\\IdeaProjects\\MQP\\chart\\NFL Salary Calculations.json'
output_folder_path = 'E:\\IdeaProjects\\MQP\\new_chart\\'

# Read data from the existing JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)['Cumulative Round Data']

# Read data from the Draft Value file
with open(draft_value_file_path, 'r') as file:
    draft_value_data = json.load(file)

# Read data from the Salary Calculations file
with open(salary_file_path, 'r') as file:
    salary_data = json.load(file)

# Extract "Round Percentages" for draft value and salary
draft_value_percentage = list(draft_value_data["Round Percentages"].values())
salary_percentage = list(salary_data["Percentage Total Value by Round"].values())

# Adjust lengths if necessary
if len(draft_value_percentage) < len(data.keys()):
    draft_value_percentage.append(0)  # Assuming no data for 'Undrafted'
if len(salary_percentage) < len(data.keys()):
    salary_percentage.append(0)  # Assuming no data for 'Undrafted'

# Existing data extraction for charts
rounds = list(data.keys())[:-1]  # Rounds without 'Undrafted'
undrafted_included_rounds = list(data.keys())  # Rounds with 'Undrafted'

average_av = [data[round]['average_av'] for round in rounds]
av_percentage = [data[round]['av_percentage'] for round in rounds]
average_games = [data[round]['total_games'] / data[round]['total_players'] for round in rounds]
games_percentage = [data[round]['games_percentage'] for round in rounds]

total_av = [data[round]['total_av'] for round in undrafted_included_rounds]
total_av_percentage = [data[round]['av_percentage'] for round in undrafted_included_rounds]
total_games = [data[round]['total_games'] for round in undrafted_included_rounds]
total_games_percentage = [data[round]['games_percentage'] for round in undrafted_included_rounds]

# Function to create and save bar charts
def create_and_save_bar_chart(data, title, xlabel, ylabel, edge_color, alpha, label, rounds, output_filename):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar chart with white fill and colored edge
    bars = ax.bar(rounds, data, color='white', edgecolor=edge_color, linewidth=1.5, alpha=alpha, label=label)
    
    # Data values on bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title)
    plt.legend()

    plt.savefig(output_folder_path + output_filename)
    plt.close()

# Function to create and save line charts for percentages
def create_and_save_line_chart(percentages, draft_value_percent, salary_percent, title, ylabel, line_color, draft_value_line_color, salary_line_color, rounds, output_filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Connective line for original percentages
    ax.plot(rounds, percentages, color=line_color, label='Percentage', marker='o')
    # Connective line for draft value percentage
    ax.plot(rounds, draft_value_percent, color=draft_value_line_color, label='Draft Value Percentage', marker='x')
    # Connective line for salary percentage
    ax.plot(rounds, salary_percent, color=salary_line_color, label='Salary Percentage', marker='^')

    # Annotations and labels
    for i, txt in enumerate(percentages):
        ax.annotate(f"{txt:.2f}%", (rounds[i], percentages[i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(draft_value_percent):
        ax.annotate(f"{txt:.2f}%", (rounds[i], draft_value_percent[i]), textcoords="offset points", xytext=(0,-15), ha='center')
    for i, txt in enumerate(salary_percent):
        ax.annotate(f"{txt:.2f}%", (rounds[i], salary_percent[i]), textcoords="offset points", xytext=(0,-30), ha='center')

    ax.set_ylabel(ylabel)
    plt.title(title)
    plt.legend()

    plt.savefig(output_folder_path + output_filename)
    plt.close()

# Creating and saving bar charts
create_and_save_bar_chart(average_av, 'Average AV per Round', 'Draft Round', 'Average AV', 'black', 0.6, 'Average AV', rounds, 'average_av_per_round.png')
create_and_save_bar_chart(average_games, 'Average Games Played per Round', 'Draft Round', 'Average Games Played', 'black', 0.6, 'Average Games Played', rounds, 'average_games_per_round.png')
create_and_save_bar_chart(total_av, 'Total AV per Round (Including Undrafted)', 'Draft Round', 'Total AV', 'black', 0.6, 'Total AV', undrafted_included_rounds, 'total_av_including_undrafted.png')
create_and_save_bar_chart(total_games, 'Total Games Played per Round (Including Undrafted)', 'Draft Round', 'Total Games Played', 'black', 0.6, 'Total Games Played', undrafted_included_rounds, 'total_games_including_undrafted.png')

# Creating and saving line charts for percentages
create_and_save_line_chart(av_percentage, draft_value_percentage[:len(rounds)], salary_percentage[:len(rounds)], 'Percentage of Average AV per Round', 'Percentage (%)', 'red', 'green', 'orange', rounds, 'av_percentage_per_round.png')
create_and_save_line_chart(games_percentage, draft_value_percentage[:len(rounds)], salary_percentage[:len(rounds)], 'Percentage of Average Games Played per Round', 'Percentage (%)', 'red', 'green', 'orange', rounds, 'games_percentage_per_round.png')
create_and_save_line_chart(total_av_percentage, draft_value_percentage, salary_percentage, 'Percentage of Total AV per Round (Including Undrafted)', 'Percentage (%)', 'red', 'green', 'orange', undrafted_included_rounds, 'total_av_percentage_including_undrafted.png')
create_and_save_line_chart(total_games_percentage, draft_value_percentage, salary_percentage, 'Percentage of Total Games Played per Round (Including Undrafted)', 'Percentage (%)', 'red', 'green', 'orange', undrafted_included_rounds, 'total_games_percentage_including_undrafted.png')
