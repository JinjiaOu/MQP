import json

def process_data(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize variables
    round_totals = {}
    overall_total = 0
    round_1_values = []

    # Calculate total value for each round
    for entry in data:
        round_number = entry['Round']
        value = entry['Value']
        round_totals[round_number] = round_totals.get(round_number, 0) + value
        overall_total += value
        if round_number == 1:
            round_1_values.append(value)

    # Calculate the total for Round 1
    round_1_total = sum(round_1_values)

    # Calculate average and percentage for each round
    round_averages = {round_number: total / sum(1 for d in data if d['Round'] == round_number)
                      for round_number, total in round_totals.items()}
    round_percentages = {round_number: (total / overall_total) * 100
                         for round_number, total in round_totals.items()}

    # Calculate percentage of each value in Round 1 to the overall total
    round_1_value_percentages = [(value / overall_total) * 100 for value in round_1_values]

    # Combine all calculations
    final_data = {
        'Round Totals': round_totals,
        'Round Averages': round_averages,
        'Round Percentages': round_percentages,
        'Round 1 Total': round_1_total,
        'Round 1 Value Percentages to Total Draft': round_1_value_percentages
    }

    return final_data

def write_to_file(output_path, data):
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

# File paths
input_path = 'E:\\IdeaProjects\\MQP\\other_json\\Draft Value chart.json'
output_path = 'E:\\IdeaProjects\\MQP\\chart\\Draft Value.json'

# Process and write data
processed_data = process_data(input_path)
write_to_file(output_path, processed_data)
