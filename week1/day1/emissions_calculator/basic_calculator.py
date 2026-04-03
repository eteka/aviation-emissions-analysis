import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin

class EmissionsCalculator:
    def __init__(self):
        # CO2 emissions factor (kg CO2 per kg fuel)
        self.CO2_FACTOR = 3.16
        # Average fuel consumption rate (kg/km) - simplified for demonstration
        self.FUEL_RATE = 12.0
        
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate great circle distance between two points."""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c
    
    def calculate_emissions(self, distance_km):
        """Calculate CO2 emissions for a given distance."""
        fuel_consumed = distance_km * self.FUEL_RATE
        co2_emissions = fuel_consumed * self.CO2_FACTOR
        return {
            'distance_km': distance_km,
            'fuel_consumed_kg': fuel_consumed,
            'co2_emissions_kg': co2_emissions
        }
    
    def calculate_route_emissions(self, origin_lat, origin_lon, dest_lat, dest_lon):
        """Calculate emissions for a route using coordinates."""
        distance = self.haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        return self.calculate_emissions(distance)

def main():
    calculator = EmissionsCalculator()
    
    # Example calculation for LHR to JFK
    lax = (33.9416, -118.4085)  # Los Angeles
    nrt = (35.7720, 140.3929)  # Tokyo Narita
    
    results = calculator.calculate_route_emissions(*lax, *nrt)
    print("Flight Emissions Analysis:")
    for key, value in results.items():
        print(f"{key}: {value:.2f}")

if __name__ == "__main__":
    main()