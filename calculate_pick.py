import json
import os
import math  # Import for NaN checking

# Input and output directories
input_directory = "E:\\IdeaProjects\\MQP\\json_data"
output_directory = "E:\\IdeaProjects\\MQP\\pick_data"
output_file_path = os.path.join(output_directory, "aggregated_pick_data.json")

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Initialize a dictionary to store totals for each pick
totals = {}

# Loop through each year
for year in range(2000, 2024):
    file_path = os.path.join(input_directory, f"{year}.json")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File for {year} does not exist, skipping.")
        continue
    
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        # Process each player's data
        for player in data:
            pick = str(player["Pick"])  # Ensure pick is a string for key consistency
            
            # Initialize the pick in the totals dictionary if not already present
            if pick not in totals:
                totals[pick] = {"total_av": 0, "total_games": 0}
            
            # Aggregate AV and games, checking for NaN
            av = player.get("Weighted Career Approximate Value", 0)
            games = player.get("Games played", 0)
            av = 0 if av is None or math.isnan(av) else av
            games = 0 if games is None or math.isnan(games) else games
            
            totals[pick]["total_av"] += av
            totals[pick]["total_games"] += games

# Now that all totals are aggregated, calculate the overall totals
total_av_all_picks = sum(pick_data["total_av"] for pick_data in totals.values())
total_games_all_picks = sum(pick_data["total_games"] for pick_data in totals.values())

# With overall totals calculated, now calculate percentages for each pick
for pick, data in totals.items():
    data["av_percentage"] = (data["total_av"] / total_av_all_picks) * 100 if total_av_all_picks > 0 else 0
    data["game_percentage"] = (data["total_games"] / total_games_all_picks) * 100 if total_games_all_picks > 0 else 0

# Prepare the final data including the overall totals
final_data = {
    "pick_data": totals,
    "overall_totals": {
        "total_av": total_av_all_picks,
        "total_games": total_games_all_picks
    }
}

# Save the aggregated data along with overall totals to a JSON file in the output directory
with open(output_file_path, 'w') as outfile:
    json.dump(final_data, outfile, indent=4)

print(f"Aggregated pick data along with overall totals saved to {output_file_path}")
