import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def read_percentage_values(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    percentages = [float(item["Percentage"].rstrip('%')) for item in data]
    return percentages

def read_total_values(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)["pick_data"]
    total_avs = [item["total_av"] for _, item in data.items()]
    total_games = [item["total_games"] for _, item in data.items()]
    return total_avs, total_games

def calculate_polynomial_regression(x, y, degree=2):
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    reg = LinearRegression().fit(x_poly, y)
    return reg.predict(x_poly), reg

# File paths
salary_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\NFL Salary chart_percentage.json'
value_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\Draft Value chart_percentage.json'
pick_data_file_path = 'E:\\IdeaProjects\\MQP\\pick_data\\aggregated_pick_data.json'
output_graph_path_prefix = 'E:\\IdeaProjects\\MQP\\'

# Read salary and value percentages
salary_percentages = read_percentage_values(salary_file_path)
value_percentages = read_percentage_values(value_file_path)

# Read total AV and total games played
total_avs, total_games = read_total_values(pick_data_file_path)

# Determine the number of picks
num_picks = min(len(salary_percentages), len(value_percentages), len(total_avs), len(total_games))
picks = np.arange(1, num_picks + 1)

# Calculate polynomial regression for all datasets
salary_regression, _ = calculate_polynomial_regression(picks, np.array(salary_percentages)[:num_picks])
value_regression, _ = calculate_polynomial_regression(picks, np.array(value_percentages)[:num_picks])
av_regression, _ = calculate_polynomial_regression(picks, np.array(total_avs)[:num_picks])
game_regression, _ = calculate_polynomial_regression(picks, np.array(total_games)[:num_picks])

def plot_chart_with_dual_axes_and_regression(x, total_values, total_regression, salary_regression, value_regression, title, ylabel_left, ylabel_right, filename):
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Bar chart for total values and regression line for total values
    color = 'tab:blue'
    ax1.set_xlabel('Pick Number')
    ax1.set_ylabel(ylabel_left, color=color)
    ax1.bar(x, total_values[:num_picks], color=color, width=0.4, label=ylabel_left + ' Total')
    ax1.plot(x, total_regression, 'b-', label=ylabel_left + ' Regression', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Instantiate a second axes that shares the same x-axis for percentage regressions
    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel(ylabel_right, color=color)
    ax2.plot(x, salary_regression, 'r--', label='Salary Value Regression', linewidth=2)
    ax2.plot(x, value_regression, 'g--', label='Draft Value Regression', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Title and combined legend for all lines
    plt.title(title)
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper right')
    
    fig.tight_layout()
    plt.savefig(output_graph_path_prefix + filename + '.png')
    plt.show()

# Generate the charts for Total AV and Total Games with Dual Axes and Regression Lines
plot_chart_with_dual_axes_and_regression(picks, total_avs, av_regression, salary_regression, value_regression, 'Total AV with Regressions', 'Total AV', 'Percentage', 'Total_AV_Chart')
plot_chart_with_dual_axes_and_regression(picks, total_games, game_regression, salary_regression, value_regression, 'Total Games Played with Regressions', 'Total Games Played', 'Percentage', 'Total_Games_Chart')
