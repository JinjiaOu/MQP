import json

# Function to calculate and output percentage values for each pick based on Total Value to a specified output file
def calculate_pick_percentages(input_file_path, output_file_path):
    # Step 1: Read the JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    
    # Step 2: Calculate Total Value
    total_value = sum(item["Total Value"] for item in data)
    
    # Step 3: Calculate Percentage for Each Pick and Prepare Output Data
    output_data = []
    for item in data:
        pick_percentage = (item["Total Value"] / total_value) * 100
        output_item = {
            "Round": item["Round"],
            "Pick": item["Pick"],
            "Total Value": item["Total Value"],
            "Percentage": f"{pick_percentage:.2f}%"
        }
        output_data.append(output_item)
    
    # Step 4: Write the results to the output file in JSON format
    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

# Example usage
input_file_path = r'E:\IdeaProjects\MQP\other_json\NFL Salary chart.json'
output_file_path = r'E:\IdeaProjects\MQP\other_json\NFL Salary chart_percentage.json'
calculate_pick_percentages(input_file_path, output_file_path)
