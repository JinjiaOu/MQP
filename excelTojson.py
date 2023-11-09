import os
import pandas as pd
import json

# Your Excel file path
excel_file_path = r'C:\Users\vainglory\IdeaProjects\MQP\draftdata\2023.xlsx'

# Read the excel file
df = pd.read_excel(excel_file_path)

# Convert the DataFrame to a list of dictionaries
records = df.to_dict(orient='records')

# The directory you want to save the JSON files in
json_folder_path = r'C:\Users\vainglory\IdeaProjects\MQP\json_data'

# Create the directory if it does not exist
os.makedirs(json_folder_path, exist_ok=True)

# The base name of your Excel file, without the extension
base_name = os.path.splitext(os.path.basename(excel_file_path))[0]

# The full path for the new JSON file
json_file_path = os.path.join(json_folder_path, base_name + '.json')

# Save the records to a JSON file
with open(json_file_path, 'w') as f:
    json.dump(records, f, indent=4)

print(f"JSON data has been saved to {json_file_path}")