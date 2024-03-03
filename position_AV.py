import pandas as pd
import json

base_folder_path = r'C:\Users\vainglory\IdeaProjects\MQP\json_data'

# Columns of interest
columns_of_interest = [
    'Player', 'Pos', 'Rnd', 'Pick', 'Team', 'To', 
    'Weighted Career Approximate Value', 'Games played', 'Number of years as primary starter for his team at his position'
]

for year in range(2000, 2024):
    json_file_path = f'{base_folder_path}\\{year}.json'
    json_output_path = f'C:\\Users\\vainglory\\IdeaProjects\\MQP\\position_AV\\{year}.json'

    df = pd.read_json(json_file_path)

    df_filtered = df[columns_of_interest]

    grouped = df_filtered.groupby('Rnd')

    round_data = {}

    for round_number, group in grouped:
        group_sorted = group.sort_values(by=['Pos', 'Pick'])
        
        # Calculate total value per position in the round
        position_value = group_sorted.groupby('Pos')['Weighted Career Approximate Value'].sum()
        round_data[round_number] = position_value.to_dict()

    year_data = {year: round_data} 

    with open(json_output_path, 'w') as f:
        json.dump(year_data, f, indent=4)

    print(f"Data for {year} successfully saved to {json_output_path}")