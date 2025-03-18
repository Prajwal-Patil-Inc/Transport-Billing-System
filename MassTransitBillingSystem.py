import csv
from collections import defaultdict
from datetime import datetime
import sys

# Zone fare data
zone_fares = {
    1: 0.80,
    (2, 3): 0.50,
    (4, 5): 0.30,
    (6, float('inf')): 0.10
}

# Function to get the zone fare based on the zone
def get_zone_fare(zone):
    if zone == 1:
        return 0.80
    elif 2 <= zone <= 3:
        return 0.50
    elif 4 <= zone <= 5:
        return 0.30
    elif zone >= 6:
        return 0.10
    return 0

# Function to process journeys and calculate total fares
def process_journeys(user_travel_data, station_zone_data):
    #user_totals = defaultdict(float)  # Store total fare for each user
    user_daily_totals = defaultdict(lambda: defaultdict(float))  # User -> Date -> Total Fare
    user_monthly_totals = defaultdict(lambda: defaultdict(float))  # User -> Month -> Total Fare
    #Static vars
    DAILY_CAP = 15.0
    MONTHLY_CAP = 100.0
    
    for user, journeys in user_travel_data.items():
        unmatched_in = []  # Stack to store unmatched 'IN' journeys
        
        for journey in journeys:
            direction = journey['direction']
            station = journey['station']
            timestamp = journey['time']
            date = timestamp.date()
            month = timestamp.month
            
            # If it's an 'IN' journey
            if direction == 'IN':
                # Append the station, timestamp, and zone in the unmatched_in list
                entry_zone = station_zone_data.get(station, 1)
                unmatched_in.append((station, entry_zone, timestamp))
            
            # If it's an 'OUT' journey
            elif direction == 'OUT':
                if unmatched_in: #checks if the stack is not empty
                    # Match with the most recent 'IN'
                    entry_station, entry_zone, entry_time = unmatched_in.pop()
                    exit_zone = station_zone_data.get(station, 1)

                    # Calculate fare based on zones
                    fare = 2.00 + get_zone_fare(entry_zone) + get_zone_fare(exit_zone)
                    # Apply daily cap if needed
                    if user_daily_totals[user][date] + fare > DAILY_CAP:
                        fare = DAILY_CAP - user_daily_totals[user][date]
                    user_daily_totals[user][date] += fare

                        # Apply monthly cap if needed
                    if user_monthly_totals[user][month] + fare > MONTHLY_CAP:
                        fare = MONTHLY_CAP - user_monthly_totals[user][month]
                    user_monthly_totals[user][month] += fare

                # else:
                #     # Apply penalty for unmatched 'OUT'
                #     #print(f"Error: 'OUT' journey without a preceding 'IN' for user {user}. Penalty applied.")
                #     user_daily_totals[user][date] += 5.0
                #     user_monthly_totals[user][month] += 5.0

        # Apply penalty for any remaining unmatched 'IN' journeys
        for unmatched in unmatched_in:
            # print(f"Error: 'IN' journey without a corresponding 'OUT' for user {user}. Penalty applied.")
            user_daily_totals[user][date] += 5.0
            user_monthly_totals[user][month] += 5.0

    # Return user_monthly_totals
    return user_monthly_totals

# Function to write monthly totals to CSV
def write_monthly_totals_to_csv(user_monthly_totals, output_file):
    # Open the output CSV file and write the monthly totals
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
       # Sort user IDs in alphanumeric increasing order
        sorted_user_ids = sorted(user_monthly_totals.keys())
        
        for user in sorted_user_ids:
            monthly_data = user_monthly_totals[user]
            # Calculate the total for the month
            monthly_total = min(sum(monthly_data.values()), 100.0)  # Apply monthly cap
            writer.writerow([user, round(monthly_total, 2)]) #Rounds the monthly total value to 2 decimal places

# Function to process the CSV files and calculate fares
def process_files(journey_file, zone_file, output_file):
    user_data = defaultdict(list)
    station_zone_data = {}
    
    # Read the station-zone mapping file
    with open(zone_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            station_zone_data[row['station']] = int(row['zone'])
    
    # Read the journey data file
    with open(journey_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            user_id = row['user_id']
            station = row['station']
            direction = row['direction']
            time_str = row['time']
            
            time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")  # Correct date parsing
            
            user_data[user_id].append({
                "station": station,
                "direction": direction,
                "time": time
            })
    
    # Process the user data and calculate fares
    user_monthly_totals = process_journeys(user_data, station_zone_data)
    
    # Write the monthly totals to the specified output CSV file
    write_monthly_totals_to_csv(user_monthly_totals, output_file)

    print(f"Monthly totals have been written to {output_file}")

# Main function to handle command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python solution.py <journey_data_file> <zone_data_file> <output_file>")
        sys.exit(1)
    
    journey_file = sys.argv[1]
    zone_file = sys.argv[2]
    output_file = sys.argv[3]
    
    process_files(journey_file, zone_file, output_file)