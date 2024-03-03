from pymongo import MongoClient
import json
import os

# Your MongoDB client here, which you've already connected
client = MongoClient('mongodb+srv://admin:admin@mqp-database.3yyl9tm.mongodb.net/')

# Choose your database
db = client['NFL']

# Choose the collection to which you want to insert the data
collection = db['cumulative_round_data_with_undrafted']

# Base directory where your JSON files are stored
base_directory = r'C:\Users\vainglory\IdeaProjects\MQP\cumulative_round_data_with_undrafted'

# File name for the specific JSON file
json_file_name = 'cumulative_round_data_with_undrafted.json'
json_file_path = os.path.join(base_directory, json_file_name)

# Check if the file exists before trying to open it
if os.path.exists(json_file_path):
    # Load your JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Insert the data into the collection
    # If 'data' is a list of records, use `insert_many`
    if isinstance(data, list):
        collection.insert_many(data)
    # If 'data' is a single document, use `insert_one`
    else:
        collection.insert_one(data)
    
    print(f"Data from {json_file_name} has been uploaded to MongoDB.")
else:
    print(f"File {json_file_name} does not exist.")
