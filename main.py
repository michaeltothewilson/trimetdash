#######################################################################################
# Title: Trimet Ticker
# Author: Mike Wilson - mmw23@pdx.edu
# Description: A Little App for keeping track of Public Transit
# Date: 12-17-25
#######################################################################################
import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import datetime

# Load ID
load_dotenv()
APP_ID = os.getenv("TRIMET_APP_ID")


ARRIVALS_URL = "https://developer.trimet.org/ws/v2/arrivals"
NUMBER_OF_ARRIVALS = 2
LOCATION_ID = 10753

## Street Car Class ##
class StreetCar:
    # Constructor
    def __init__(self, location, direction, sign, estimated_time_arrival):
        self.location = location
        self.direction = direction
        self.sign = sign
        estimated_time_arrival_seconds = estimated_time_arrival / 1000
        self.estimated_time_arrival = datetime.fromtimestamp(estimated_time_arrival_seconds)
    
    # Converts the Estimated Time from Seconds to Minutes
    def get_minutes_away(self):
        # Get Current Time
        time_now = datetime.now()
        
        # Subtract (Arrival Time - Current Time)
        time_delta = self.estimated_time_arrival - time_now
        
        # Convert to Total Minutes
        minutes_away = time_delta.total_seconds() / 60
        
        # Round Minutes
        minutes_away = round(minutes_away)
        
        return minutes_away
        
    # Output Fast and Easy Data on Street Car    
    def report(self):
        minutes_away = self.get_minutes_away()
        
        print(f"{self.sign}\n" +
              f"Location: {self.location}\n"+
              f"Direction: {self.direction}\n" +
              f"ETA: {minutes_away} minute(s)")

 
def trimet_request_response(url, params):
    results = {}
    
    response = requests.get(ARRIVALS_URL, params=params)

    # Get Repsonse
    if response.status_code == 200:
        data = response.json()
        
        results["arrivals"] = data["resultSet"]["arrival"]
        results["location"] = data["resultSet"]["location"][0]
        results["time"] = data["resultSet"]["queryTime"]
        
    else:
        print(f"Error: {response.status_code}")
    
    return results
                  
def print_transportation_reports(transportation_list):
    for vehicle in transportation_list:
        vehicle.report()
        print("\n\n")

def build_transportation_list(transit_results):
    transit_vehicle_list = []
    
    for transit_vehicle in api_results:
        # Get the relevant variables assigned
        sign = transit_results["shortSign"]
        estimated_time_arrival = transit_results["estimated"]
        location = transit_results["location"]["desc"]
        direction = transit_results["location"]["dir"]
        
        # Build Street Car
        vehicle = StreetCar(location, direction, sign, estimated_time_arrival)
        
        # Add to the List
        transit_vehicle_list.append(vehicle)
        
    return transit_vehicle_list
        
## Main ##
def main():
    # Variable Starter Pack
    streetcar_list = []
    results = {}
    params = {
        "locIDs": LOCATION_ID,
        "appID": APP_ID,
        "json": "true",
        "arrivals": NUMBER_OF_ARRIVALS,
    }
    
    # Get API Response
    #response = requests.get(ARRIVALS_URL, params=params)
    results = trimet_request_response(ARRIVALS_URL, params)
    
    # Build List of Street Cars
    for streetcar in results["arrivals"]:
        # Get the relevant variables assigned
        sign = streetcar["shortSign"]
        estimated_time_arrival = streetcar["estimated"]
        location = results["location"]["desc"]
        direction = results["location"]["dir"]
        
        # Build Street Car
        car = StreetCar(location, direction, sign, estimated_time_arrival)
        
        # Add to the List
        streetcar_list.append(car)
        
    # View Output    
    print_transportation_reports(streetcar_list)
        
                
if __name__ == "__main__":
    main()