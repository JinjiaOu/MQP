import pandas as pd

# Base file path
base_folder_path = r'C:\Users\vainglory\IdeaProjects\MQP\json_data'

# Columns of interest
columns_of_interest = [
    'Player', 'Pos', 'Rnd', 'Pick', 'Team','To', 
    'Weighted Career Approximate Value', 'Games played', 'Number of years as primary starter for his team at his position'
]

for year in range(2000, 2024):
    # Construct file paths
    json_file_path = f'{base_folder_path}\\{year}.json'
    excel_output_path = f'C:\\Users\\vainglory\\IdeaProjects\\MQP\\analyise_data_AV\\{year}.xlsx'

    df = pd.read_json(json_file_path)

    # Filter the DataFrame to the columns of interest
    df_filtered = df[columns_of_interest]

    # Group by the 'Rnd' column (Round)
    grouped = df_filtered.groupby('Rnd')

    with pd.ExcelWriter(excel_output_path) as writer:
        round_value_summary = {}  # To store total value per round
        round_position_value_summary = {}  # To store value per position per round

        for round_number, group in grouped:
            # Sort each group by position, then by pick within the round
            group_sorted = group.sort_values(by=['Pos', 'Pick'])
            # Write each sorted group to a separate sheet
            sheet_name = f'Round_{round_number}'
            group_sorted.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Calculate total value per position in the round
            position_value = group_sorted.groupby('Pos')['Weighted Career Approximate Value'].sum()
            round_position_value_summary[round_number] = position_value

            # Calculate and accumulate total value of the round
            total_round_value = position_value.sum()
            round_value_summary[round_number] = total_round_value

        # Write the round value summary to another sheet in the same Excel file
        summary_sheet_name = 'Round_Value_Summary'
        pd.DataFrame.from_dict(round_value_summary, orient='index', columns=['Total Value']).to_excel(writer, sheet_name=summary_sheet_name, index_label='Round')
        
        # Write the position value summary for each round to another sheet
        for round_number, position_value in round_position_value_summary.items():
            pos_value_sheet_name = f'Round_{round_number}_Pos_Value'
            position_value.to_frame(name='Total Value').to_excel(writer, sheet_name=pos_value_sheet_name, index_label='Position')

    print(f"Data for {year} successfully saved to {excel_output_path}")