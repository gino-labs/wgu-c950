import re
import csv
from pathlib import Path

# Helper class for containing data for a delivery location
class Location:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.zip_code = None
        self.neighbors = []
    
    # Helper method for using Location class with python 'in' syntax
    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return self.name == other.name

    def set_zip_code(self, first_two_address_strings: list):
        match = re.search(r'841\d{2}', first_two_address_strings[0])
        if not match:
            match = re.search(r'841\d{2}', first_two_address_strings[1])
        self.zip_code = match.group()

    def add_neighbor(self, neighbor_location: "Location", neighbor_distance: float):
        neighbor = Neighbor(neighbor_location, neighbor_distance)
        self.neighbors.append(neighbor)

# Object Containing Neighbor Details for a given location
class Neighbor:
    def __init__(self, neighbor: Location, distance: float):
        self.name = neighbor.name
        self.address = neighbor.address
        self.zip_code = neighbor.zip_code
        self.neighbors = neighbor.neighbors
        self.distance = distance

# Class for organizing distance table data
class DistanceTable:
    def __init__(self):
            # List to hold Location instances
            self.locations = []

    # Parse location string into Location instance
    def set_locations(self, locations_list: list):
        for location in locations_list:
            location_data = location.split("\n")
            location_name = location_data[0].strip()
            location_address = location_data[1].strip().strip(",")
            self.locations.append(Location(location_name, location_address))

    def get_location(self, location_name: str):
        for location in self.locations:
            if location.name.lower() == location_name.lower():
                return location
        raise ValueError(f"Location not found: {location_name}")

    # Helper function for parsing distance table csv data
    def load_from_csv(self, csv_file):
        csv_file = Path(csv_file)
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        with open(csv_file, "r", encoding="utf-8") as file:
            csv_data = list(csv.reader(file))
  
        locations_table_head = csv_data[7][2:] # Row 7, Column 3+
        self.set_locations(locations_table_head)

        # Parse data beginning at row 8
        rows = csv_data[8:]
        for i, row in enumerate(rows):
            self.locations[i].set_zip_code(row[:2])
            for j, col in enumerate(row[2:]):
                try:
                    distance = float(col)
                except ValueError:
                    inverse_row = rows[j][2:]
                    distance = float(inverse_row[i])
                self.locations[i].add_neighbor(self.locations[j], distance)
