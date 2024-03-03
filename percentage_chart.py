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

def read_aggregated_pick_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)["pick_data"]
    av_percentages = [item["av_percentage"] for _, item in data.items()]
    game_percentages = [item["game_percentage"] for _, item in data.items()]
    return av_percentages, game_percentages

def calculate_polynomial_regression(x, y, degree=2):
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    reg = LinearRegression().fit(x_poly, y)
    return reg.predict(x_poly), reg

# File paths and data loading
salary_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\NFL Salary chart_percentage.json'
value_file_path = 'E:\\IdeaProjects\\MQP\\other_json\\Draft Value chart_percentage.json'
pick_data_file_path = 'E:\\IdeaProjects\\MQP\\pick_data\\aggregated_pick_data.json'
output_graph_path_prefix = 'E:\\IdeaProjects\\MQP\\'

salary_percentages = read_percentage_values(salary_file_path)
value_percentages = read_percentage_values(value_file_path)
av_percentages, game_percentages = read_aggregated_pick_data(pick_data_file_path)

# Determine the number of picks to plot
num_picks = min(len(salary_percentages), len(value_percentages), len(av_percentages))
picks = np.arange(1, num_picks + 1)

# Calculate polynomial regression for salary, value, av_percentage, and game_percentage
salary_regression, _ = calculate_polynomial_regression(picks, np.array(salary_percentages)[:num_picks])
value_regression, _ = calculate_polynomial_regression(picks, np.array(value_percentages)[:num_picks])
av_percentage_regression, _ = calculate_polynomial_regression(picks, np.array(av_percentages)[:num_picks])
game_percentage_regression, _ = calculate_polynomial_regression(picks, np.array(game_percentages)[:num_picks])

# Plotting function for AV percentage chart with AV percentage regression
def plot_av_percentage_chart():
    plt.figure(figsize=(12, 8))
    width = 0.25
    plt.bar(picks, av_percentages[:num_picks], width, label='AV Percentage', color='b')
    plt.plot(picks, salary_regression, 'r--', label='Salary Regression')
    plt.plot(picks, value_regression, 'g--', label='Value Regression')
    plt.plot(picks, av_percentage_regression, 'm--', label='AV Percentage Regression')
    plt.title('AV Percentage with Salary, Value, and AV Percentage Polynomial Regression')
    plt.xlabel('Pick')
    plt.ylabel('Percentage')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_graph_path_prefix + 'AV_Percentage_Chart.png')
    plt.show()

# Plotting function for Game percentage chart with Game percentage regression
def plot_game_percentage_chart():
    plt.figure(figsize=(12, 8))
    width = 0.25
    plt.bar(picks, game_percentages[:num_picks], width, label='Game Percentage', color='c')
    plt.plot(picks, salary_regression, 'r--', label='Salary Regression')
    plt.plot(picks, value_regression, 'g--', label='Value Regression')
    plt.plot(picks, game_percentage_regression, 'y--', label='Game Percentage Regression')
    plt.title('Game Percentage with Salary, Value, and Game Percentage Polynomial Regression')
    plt.xlabel('Pick')
    plt.ylabel('Percentage')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_graph_path_prefix + 'Game_Percentage_Chart.png')
    plt.show()

# Generate the charts
plot_av_percentage_chart()
plot_game_percentage_chart()
