import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # For polynomial regression
import os

# Paths
json_file_path = 'E:\\IdeaProjects\\MQP\\pick_data\\aggregated_pick_data.json'
draft_value_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\Draft Value chart.json'
nfl_salary_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\NFL Salary chart.json'
output_directory = 'E:\\IdeaProjects\\MQP\\new_chart'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Load the JSON data for aggregated pick data
with open(json_file_path, 'r') as file:
    data = json.load(file)['pick_data']

# Load Draft Value Chart
with open(draft_value_file_path, 'r') as file:
    draft_value_data = json.load(file)

# Load NFL Salary Chart
with open(nfl_salary_file_path, 'r') as file:
    nfl_salary_data = json.load(file)

# Convert the data to DataFrames
df = pd.DataFrame(data).T  # Transpose to have picks as rows
df_draft_value = pd.DataFrame(draft_value_data)
df_nfl_salary = pd.DataFrame(nfl_salary_data)

# Process the main DataFrame
df['Pick'] = df.index.astype(int)  # Convert index to integer for sorting
df.sort_values('Pick', inplace=True)

# Polynomial Regression for Total AV and Total Games Played
degree_av = 3
coeffs_av = np.polyfit(df['Pick'], df['total_av'], degree_av)
poly_av = np.poly1d(coeffs_av)

degree_games = 3
coeffs_games = np.polyfit(df['Pick'], df['total_games'], degree_games)
poly_games = np.poly1d(coeffs_games)

x_line = np.linspace(min(df['Pick']), max(df['Pick']), num=1000)
y_line_av = poly_av(x_line)
y_line_games = poly_games(x_line)

# Plot Draft Value Chart with Total AV Regression on secondary y-axis
fig, ax1 = plt.subplots(figsize=(14, 7))
color = 'tab:blue'
ax1.set_xlabel('Pick')
ax1.set_ylabel('Draft Value', color=color)
ax1.plot(df_draft_value['Pick'], df_draft_value['Value'], color=color, label='Draft Value')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Total AV', color=color)
ax2.plot(x_line, y_line_av, color=color, linestyle='--', label='Regression Curve for Total AV')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Draft Value and Total AV Regression by Pick')
plt.savefig(os.path.join(output_directory, 'Draft_Value_and_Total_AV_Regression_by_Pick.png'))
plt.close()

# Plot NFL Salary Chart with Total Games Played Regression on secondary y-axis
fig, ax1 = plt.subplots(figsize=(14, 7))
color = 'tab:green'
ax1.set_xlabel('Pick')
ax1.set_ylabel('Total Value', color=color)
ax1.plot(df_nfl_salary['Pick'], df_nfl_salary['Total Value'], color=color, label='Total Value')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:purple'
ax2.set_ylabel('Total Games Played', color=color)
ax2.plot(x_line, y_line_games, color=color, linestyle='--', label='Regression Curve for Total Games Played')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('NFL Salary Total Value and Total Games Regression by Pick')
plt.savefig(os.path.join(output_directory, 'NFL_Salary_Total_Value_and_Games_Regression_by_Pick.png'))
plt.close()

# Plot NFL Salary Chart with Total AV Regression on secondary y-axis
fig, ax1 = plt.subplots(figsize=(14, 7))
color = 'tab:green'
ax1.set_xlabel('Pick')
ax1.set_ylabel('Total Value', color=color)
ax1.plot(df_nfl_salary['Pick'], df_nfl_salary['Total Value'], color=color, label='Total Value')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Total AV', color=color)
ax2.plot(x_line, y_line_av, color=color, linestyle='--', label='Regression Curve for Total AV')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('NFL Salary Total Value and Total AV Regression by Pick')
plt.savefig(os.path.join(output_directory, 'NFL_Salary_Total_Value_and_Total_AV_Regression_by_Pick.png'))
plt.close()

# Plot Draft Value Chart with Total Games Played Regression on secondary y-axis
fig, ax1 = plt.subplots(figsize=(14, 7))
color = 'tab:blue'
ax1.set_xlabel('Pick')
ax1.set_ylabel('Draft Value', color=color)
ax1.plot(df_draft_value['Pick'], df_draft_value['Value'], color=color, label='Draft Value')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:purple'
ax2.set_ylabel('Total Games Played', color=color)
ax2.plot(x_line, y_line_games, color=color, linestyle='--', label='Regression Curve for Total Games Played')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Draft Value and Total Games Regression by Pick')
plt.savefig(os.path.join(output_directory, 'Draft_Value_and_Total_Games_Regression_by_Pick.png'))
plt.close()
