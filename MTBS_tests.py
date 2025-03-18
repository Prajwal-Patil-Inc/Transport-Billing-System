import pytest 
from datetime import datetime
import csv
import os
from MassTransitBillingSystem import get_zone_fare, process_journeys, write_monthly_totals_to_csv

#Testing the get_zone_fare 
def test_get_zone_fare():
    assert get_zone_fare(1) == 0.80
    assert get_zone_fare(2) == 0.50
    assert get_zone_fare(3) == 0.50
    assert get_zone_fare(4) == 0.30
    assert get_zone_fare(5) == 0.30
    assert get_zone_fare(6) == 0.10
    assert get_zone_fare(7) == 0.10
        
def test_process_journeys():
    #Passing user data 
    user_travel_data = {
        "user1": [
            {"station": "StationA", "direction": "IN", "time": datetime(2025, 1, 1, 8, 0)},
            {"station": "StationB", "direction": "OUT", "time": datetime(2025, 1, 1, 9, 0)},
            {"station": "StationC", "direction": "IN", "time": datetime(2025, 1, 1, 10, 0)},
            {"station": "StationD", "direction": "OUT", "time": datetime(2025, 1, 1, 11, 0)}
        ]
    }
    #Station to zone mapping data
    station_zone_data = {
        "StationA": 1,
        "StationB": 2,
        "StationC": 3,
        "StationD": 4
    }
    
    result = process_journeys(user_travel_data, station_zone_data)
    
    assert "user1" in result
    assert 1 in result["user1"]
    assert round(result["user1"][1], 2) == 6.1 #Fare data for 'user1' in month January (1) and the expected output
    
def test_write_monthly_totals_to_csv():
    user_monthly_totals = {
        "user1": {1: 50.0},
        "user2": {1: 75.0},
        "user3": {1: 100.0} #Monthly cap
    }
    
    output_file = "test_output.csv"
    
    write_monthly_totals_to_csv(user_monthly_totals, output_file)
    
    #Checking if the file is created
    assert os.path.exists(output_file)
 
    #Reading the csv file
    with open(output_file, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
    assert len(rows) == 3
    assert rows[0] == ["user1", "50.0"]
    assert rows[1] == ["user2", "75.0"]
    assert rows[2] == ["user3", "100.0"]
    
    os.remove(output_file)