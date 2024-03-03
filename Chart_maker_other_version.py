import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # For polynomial regression
import os

# Paths
aggregated_pick_data_path = 'E:\\IdeaProjects\\MQP\\pick_data\\aggregated_pick_data.json'
draft_value_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\Draft Value chart.json'
nfl_salary_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\NFL Salary chart.json'
output_directory = 'E:\\IdeaProjects\\MQP\\new_chart'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to load data from a JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load and prepare aggregated pick data
pick_data = load_data(aggregated_pick_data_path)['pick_data']
df_pick = pd.DataFrame(pick_data).T  # Transpose to have picks as rows
df_pick['Pick'] = df_pick.index.astype(int)  # Convert index to integer for sorting
df_pick.sort_values('Pick', inplace=True)

# Load and prepare draft value and NFL salary data
df_draft_value = pd.DataFrame(load_data(draft_value_file_path))
df_nfl_salary = pd.DataFrame(load_data(nfl_salary_file_path))

# Function for polynomial regression
def get_regression_line(df, x_col, y_col, degree=3):
    coeffs = np.polyfit(df[x_col], df[y_col], degree)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(min(df[x_col]), max(df[x_col]), 1000)
    y_line = poly(x_line)
    return x_line, y_line

# Function to plot line curve and regression lines
def plot_line_and_regressions(df, df_pick, value_col, title, ylabel, output_filename, line_color='blue', regression_colors=('red', 'green')):
    x_line_value, y_line_value = get_regression_line(df, 'Pick', value_col)
    x_line_av, y_line_av = get_regression_line(df_pick, 'Pick', 'total_av')
    x_line_games, y_line_games = get_regression_line(df_pick, 'Pick', 'total_games')

    plt.figure(figsize=(14, 7))
    plt.plot(df['Pick'], df[value_col], color=line_color, label=value_col, marker='o', linestyle='-')
    plt.plot(x_line_av, y_line_av, color=regression_colors[0], label='Regression Curve for Total AV')
    plt.plot(x_line_games, y_line_games, color=regression_colors[1], label='Regression Curve for Total Games Played')
    plt.title(title)
    plt.xlabel('Pick')
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, output_filename))
    plt.close()

# Plot line curves and regression lines for Draft Value and NFL Salary Total Value
plot_line_and_regressions(df_draft_value, df_pick, 'Value', 'Draft Value by Pick with Regression Lines', 'Value', 'Draft_Value_with_Regressions.png', line_color='blue', regression_colors=('red', 'green'))
plot_line_and_regressions(df_nfl_salary, df_pick, 'Total Value', 'NFL Salary Total Value by Pick with Regression Lines', 'Total Value ($)', 'NFL_Salary_Total_Value_with_Regressions.png', line_color='green', regression_colors=('red', 'green'))
