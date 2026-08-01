#!/usr/bin/env python3
#####################
### Requirement C ###
#####################
"""
Student ID: 011576592
Student Name: Gino Curtis
WGU C950 Data Structures and Algorithms 2

Task Assumptions:
•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
•  The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.

"""
import re
import csv
import time
from pathlib import Path

class SimulatedTime:
    def __init__(self):
        self.start_time = "8:00am"
        self.current_time = self.start_time

    def update(self, time: str):
        self.current_time = time.lower()

    def stamp(self):
        hours, minutes = self.current_time.split(":")



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
        self.notes = package_data.get("special_notes")
        self.status = None

    def _calculate_time_spent(self, distance_miles: int):
        # Assume constant speed of 18mph
        speed = 18
        time_in_hours = distance_miles * speed
        time_in_minutes = time_in_hours * 60
        h = int(time_in_hours)
        m = int(time_in_minutes)
        return f"{h}:{m}"
        
    def update_status(self, status: str):
        if status.strip().lower() not in ("delayed", "at the hub", "en route", "delivered"):
            raise ValueError(f"Invalid status: {status}")
        self.status == status

### Hash Table data structure with tasks A & B ###
class PackageHashTable:
    def __init__(self, size=40):
        self.packages = [None] * size
        # TODO FIGURE OUT TIME TRACKING 

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
        # Hash Package ID with modulo operator and store at index
        index = package.id % len(self.packages)
        self.packages[index] = package

    #####################
    ### Requirement B ###
    #####################
    def get_package(self, package_id: int) -> Package:
        # Return Package object at index
        index = package_id % len(self.packages)
        return self.packages[index]

    # Update package delivery status to include time.
    def update_package_status(self, package_id: int, status: str):
        package = self.get_package(package_id)
        package.set_status(status)
    
    # Load package data from csv task file
    def load_from_csv(self, csv_file):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
        with open(csv_file, "r", encoding="utf-8") as file:
            rows = list(csv.reader(file))

            start_loading = False
            for row in rows:
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
                    if "delayed" in row[notes_index].lower():
                        delivery_status = "delayed"
                    else:
                        delivery_status = "at the hub"
                    self.add_package(
                        row[package_id_index],
                        package_weight = row[weight_index],
                        delivery_address = row[address_index],
                        delivery_city = row[city_index],
                        delivery_state = row[state_index],
                        delivery_zip_code = row[zip_index],
                        delivery_deadline = row[deadline_index],
                        delivery_status = delivery_status,
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
    def __init__(self):
            # List to hold Location instances
            self.locations = []

    # Parse location string into Location instance
    def _set_locations(self, locations_list: list):
        for location in locations_list:
            location_data = location.split("\n")
            location_name = location_data[0].strip()
            location_address = location_data[1].strip().strip(",")
            self.locations.append(Location(location_name, location_address))

    # Helper function for parsing distance table csv data
    def load_from_csv(self, csv_file):
        csv_file = Path(csv_file)
        if not csv_file.exists:
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        with open(csv_file, "r", encoding="utf-8") as file:
            csv_data = list(csv.reader(file))
  
        locations_table_head = csv_data[7][2:] # Row 7, Column 3+
        self._set_locations(locations_table_head)

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

    # Helper function to show and compare distances between neighbors
    def show_distances(self):
        for location in self.locations:
            for n in range(len(location.name) + 10):
                print("-", end='')
            print(f"\nLocation: {location.name}")
            for neighbor in location.neighbors:
                print(f"  Neighbor ({neighbor.distance} mi): {neighbor.name}")


class Truck:
    def __init__(self, truck_number: int):
        self.truck_number = truck_number
        self.miles_driven = 0
        self.capacity = 16
        self.trip_counter = 1

    def load_truck():
        pass # TODO

#####################
### Requirement D ###
#####################
class UI:
    def __init__(self):
        self.package_table = None
        self.distance_table = None
        self.truck1 = Truck(1)
        self.truck2 = Truck(2)
        self.truck3 = Truck(3) # Unused with only 2 drivers
        print("##################################################")
        print("# WGU - Data Structures and Algorithms II (C950) #")
        print("#             Student ID: 011576592              #")
        print("#           Student name: Gino Curtis            #")
        print("##################################################", end="\n\n")
        self.msg("Welcome to the Program's Interface!", newlines=2, sleep=3)

    def msg(self, message: str, newlines=1, sleep=1):
        end = ""
        for n in range(newlines):
            end += "\n"
        print(message, end=end)
        time.sleep(sleep)

    def prompt(self, message_prompt, choices=[]):
        answer = input(message_prompt)
        # TODO

    def load_package_data(self, packages_csv_file: str):
        self.msg(f"Begin loading package data from {packages_csv_file}")
        self.package_table = PackageHashTable()
        self.package_table.load_from_csv(packages_csv_file)
        self.msg(f"Package data loaded.", newlines=2)

    def load_distance_data(self, distances_csv_file):
        self.msg(f"Begin loading package data from {distances_csv_file}")
        self.distance_table = DistanceTable()
        self.distance_table.load_from_csv(distances_csv_file)
        self.msg(f"Distance data loaded.", newlines=2)

    def run(self):
        while True:
            # TODO
            break


if __name__ == "__main__":
    ui = UI()
    ui.load_package_data("wgups_package_file.csv")
    ui.load_distance_data("wgups_distance_table.csv")
    ui.run()
