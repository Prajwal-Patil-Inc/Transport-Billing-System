# Transport-Billing-System

## Description:
This python script calculates the monthly fare totals for users of a mass transit system based on their journey data. It processes user journeys, determines the fare for each journey (based on entry and exit zones), and applies daily and monthly caps. This script reads journey and zone data from the CSV files and writes the monthly fare totals for each user to a specified output CSV file.

## Requirements:
1. Python
2. pytest (for running test cases) -
Install pytest using:
```python
pip install pytest
```

## How to build/run:
1. For Windows Operating System users, simply run the batch file MassTransitBillingSystem.bat
2. Or open a terminal/cmd shell and execute this command:
```python
python MassTransitBillingSystem.py <JourneyDataFile.csv> <ZoneDataFile.csv> <OutputFile.csv>
```
3. Run Test cases using this command: "pytest MTBS_tests.py"

## Assumptions:
1. Once the user's daily fare cap is reached, no additional charges will apply for any journeys on the same day.
2. Once a user's monthly fare cap is reached, no additional charges will apply for the remainder of the month.
2. The output consists of the total monthly fares for all users. 

## Expected Output:
The output CSV file will contain:
1. User id of each user
2. Month fare total of each user rounded to two decimal places.

Users will be listed in alphanumeric increasing order of their user IDs.
