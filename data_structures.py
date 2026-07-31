#!/usr/bin/env python3
import re
import csv
from pathlib import Path
'''Imported python modules/packages to assist with 
parsing provided CSV files for this task'''

# Helper class to represent a given package
class Package:
    def __init__(self, package_id, **package_data):
        self.id = int(package_id)
        self.weight = package_data.get("package_weight")
        self.address = package_data.get("delivery_address")
        self.city = package_data.get("delivery_city")
        self.state = package_data.get("delivery_state")
        self.zip_code = package_data.get("delivery_zip_code")
        self.deadline = package_data.get("delivery_deadline")
        self.status = package_data.get("delivery_status")
        self.notes = package_data.get("special_notes")

    # Add support for direct modulo operations
    def __mod__(self, other):
        return self.id % other


### Hash Table data structure with tasks A & B ###
class PackageHashTable:
    def __init__(self, size=40):
        self.packages = [None] * size

    #####################
    ### Requirement A ###
    #####################
    def add_package(self, package_id, package_weight=None, delivery_address=None, delivery_city=None, delivery_state=None, delivery_zip_code=None, delivery_deadline=None, delivery_status=None, special_notes=None):
        package = Package(
            package_id,
            package_weight = package_weight,
            delivery_address = delivery_address,
            delivery_city = delivery_city, 
            delivery_state = delivery_state, 
            delivery_zip_code = delivery_zip_code,
            delivery_deadline = delivery_deadline,
            delivery_status = delivery_status,
            special_notes = special_notes
        )
        # Modulo hash and assign Package to hashtable index
        index = package % len(self.packages)
        self.packages[index] = package

    #####################
    ### Requirement B ###
    #####################
    def get_package(self, package_id: int) -> Package:
        # Return Package object at index
        index = package_id % len(self.packages)
        return self.packages[index]

    def timestamp(self):
        pass # TODO
    
    # Load package data from csv task files
    def load_packages_from_csv(self, csv_file="wgups_package_file.csv"):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
        # Read data from prvided CSV file
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            start_loading = False
            for row in reader:
                if "Package" in row[0] and "ID" in row[0]:
                    for i, header in enumerate(row):
                        row[i] = header.replace("\n", " ").strip()

                    package_id_index = row.index("Package ID")
                    address_index = row.index("Address")
                    city_index = row.index("City")
                    state_index = row.index("State")
                    zip_index = row.index("Zip")
                    deadline_index = row.index("Delivery Deadline")
                    weight_index = row.index("Weight KILO")
                    notes_index = row.index("page 1 of 1PageSpecial Notes")
                    start_loading = True
                    continue
                
                # Load packages after the header row is parsed
                if start_loading:
                    self.add_package(
                        row[package_id_index],
                        package_weight = row[weight_index],
                        delivery_address = row[address_index],
                        delivery_city = row[city_index],
                        delivery_state = row[state_index],
                        delivery_zip_code = row[zip_index],
                        delivery_deadline = row[deadline_index],
                        special_notes = row[notes_index]
                    )


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
    def __init__(self, csv_file="wgups_distance_table.csv"):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        else:
            # List of Location Object Instances
            self.locations = []
            self._parse_csv()

    # Parse location string into Location instance
    def _set_locations(self, locations_list: list):
        for location in locations_list:
            location_data = location.split("\n")
            location_name = location_data[0].strip()
            location_address = location_data[1].strip().strip(",")
            self.locations.append(Location(location_name, location_address))

    # Helper function for parsing distance table csv data
    def _parse_csv(self):
        with open(self.csv_file, "r", encoding="utf-8") as file:
            csv_data = list(csv.reader(file))
  
        locations_table_head = csv_data[7][2:]
        self._set_locations(locations_table_head)

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

    # Helper function to show and compare distances between neighbors
    def show_distances(self):
        for location in self.locations:
            for n in range(len(location.name) + 10):
                print("-", end='')
            print(f"\nLocation: {location.name}")
            for neighbor in location.neighbors:
                print(f"  Neighbor ({neighbor.distance} mi): {neighbor.name}")

# TODO                
class Timeclock:
    def __init__(self):
        pass

class Truck:
    def __init__(self, truck_number: int):
        self.truck_number = truck_number
        self.miles_driven = 0
        self.capacity = 16
        self.trip_counter = 1

if __name__ == "__main__":
    pass
# TESTING
# dt = DistanceTable()
# pt = PackageHashTable()
# pt.load_packages_from_csv()
