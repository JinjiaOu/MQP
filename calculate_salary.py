import json

def process_nfl_data(input_path, output_path):
    # Read the JSON file
    with open(input_path, 'r') as file:
        data = json.load(file)

    # Initialize variables
    round_totals = {}
    overall_total_value = 0

    # Calculate the total 'Total Value' for each round and for all rounds
    for entry in data:
        round_number = entry['Round']
        total_value = entry['Total Value']
        overall_total_value += total_value
        round_totals[round_number] = round_totals.get(round_number, 0) + total_value

    # Calculate the average 'Total Value' for each round
    round_averages = {round_number: total / sum(1 for d in data if d['Round'] == round_number)
                      for round_number, total in round_totals.items()}

    # Calculate the percentage 'Total Value' for each round
    round_percentages = {round_number: (total / overall_total_value) * 100
                         for round_number, total in round_totals.items()}

    # Combine all calculations
    final_data = {
        'Overall Total Value': overall_total_value,
        'Total Value by Round': round_totals,
        'Average Total Value by Round': round_averages,
        'Percentage Total Value by Round': round_percentages,
    }

    # Write the results to the output file
    with open(output_path, 'w') as file:
        json.dump(final_data, file, indent=4)

# File paths
input_path = 'E:\\IdeaProjects\\MQP\\other_json\\NFL Salary chart.json'
output_path = 'E:\\IdeaProjects\\MQP\\chart\\NFL Salary Calculations.json'

# Run the process
process_nfl_data(input_path, output_path)
