# Student ID: 011576592
# Student Name: Gino Curtis
# WGU C950 Data Structures and Algorithms 2

"""
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
import sys
import time
import readline
from pathlib import Path
from datetime import datetime, timedelta

# Clock starts at 8:00am
DAY_START = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

# Search a string for a date time match
def extract_time(_string: str) -> re.Match:
    return re.search(r'\b(1[0-2]|0?[1-9]):([0-5][0-9])\s*([AP]M)\b', _string, re.IGNORECASE)

# Convert regex match to datetime object
def regex_to_datetime(re_match: re.Match) -> datetime:
    hour = re_match.group(1)
    minute = re_match.group(2)
    meridiem = re_match.group(3).upper()
    time_string = datetime.strptime(f"{hour}:{minute} {meridiem}", "%I:%M %p")
    return DAY_START.replace(hour=time_string.hour, minute=time_string.minute)

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
        self.status = package_data.get("delivery_status")
        
    def update_status(self, status: str, timestamp: datetime):
        if status.strip().lower() not in ("delayed", "at the hub", "en route", "delivered"):
            raise ValueError(f"Invalid status: {status}")
        self.status = status.capitalize() + " - " + timestamp.strftime('%I:%M %p')

### Hash Table data structure with tasks A & B ###
class PackageHashTable:
    def __init__(self, size=40):
        self.packages = [None] * size
        self.package_groups = [] # Package groups to be delivered together

    # Helper class to convert deadlines to datetime objects
    def convert_to_datetime(self, deadline: str):
        if deadline == "EOD":
            return DAY_START + timedelta(hours=12)
        time_match = extract_time(deadline)
        return regex_to_datetime(time_match)
        
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
            delivery_deadline = self.convert_to_datetime(delivery_deadline), # Datetime object
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
        package_id = int(package_id)
        if package_id < 1 or package_id > len(self.packages):
            return None
        index = package_id % len(self.packages)
        return self.packages[index]

    def build_package_groups(self):
        package_group = []
        for package in self.packages:
            if "Must be delivered with" in package.notes:
                matches = re.findall(r"\d{1,2}", package.notes)
                for match in matches:
                    id = int(match)
                    package_group.append(self.get_package(id))
                package_group.append(package)
            self.package_groups.append(package_group)
        else:
            for group in self.package_groups:
                pass # TODO
                


    # Check a package for delivery constraints
    def is_deliverable(self, package: Package, truck: Truck):
        def check_package():
            # At the hub?
            if "at the hub" in package.status:
                return False
            
            # Truck 2 only?
            if "Can only be on truck 2" in package.notes and truck.id == 1:
                return False

            # Delayed package?
            if "Delayed" in package.notes:
                time_match = extract_time(package.notes)
                available_time = regex_to_datetime(time_match)
                # Truck time must be later than package available time
                if truck.time < available_time:
                    return False

            # Wrong address listed?
            if "Wrong address listed" in package.notes:
                available_time == DAY_START.replace(hour=10, minute=20)
                # Truck time must be later than package available time
                if truck.time > available_time:
                    return False

        def check_package_group():
            # Every package to be delivered together is deliverable?
            if "Must be delivered with" in package.notes:
                matches = re.findall(r"\d{1,2}", package.notes)
                for match in matches:
                    pass # TODO
            


    # Get deliverable packages for truck
    def get_deliverable_packages(self, truck_id, truck_time):
        deliverable_packages = []
        for package in self.packages:
            if self.is_deliverable(package, truck_id, truck_time):
                deliverable_packages.append(package)
        return deliverable_packages
    
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
                    package_id = row[package_id_index]
                    special_notes = row[notes_index]
                    if "delayed" in special_notes.lower():
                        delivery_status = "delayed - " + DAY_START.strftime("%I:%M %p")
                    else:
                        delivery_status = "at the hub - " + DAY_START.strftime("%I:%M %p")
                    self.add_package(
                        package_id,
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

class Truck:
    def __init__(self, truck_id: int, distance_table: DistanceTable, package_hashtable: PackageHashTable):
        self.id = truck_id
        self.speed = 18
        self.capacity = 16
        self.miles_driven = 0
        self.loaded_packages = []
        self.distance_table = distance_table
        self.package_hashtable = package_hashtable
        self.time = DAY_START
        self.current_location = distance_table.get_location("Western Governors University")

    # Questions when loading packages
    # Is package eligible to be loaded onto truck?
    # Are packages being loaded using Greedy Neighbor Algorithm?
    # Is package part of a larger set of packages?
    def load_packages(self):
        for package in self.package_hashtable.packages:
            pass # TODO

    def deliver_packages(self):
        pass # TODO


#####################
### Requirement D ###
#####################
class UI:
    def __init__(self):
        self.package_hashtable = None
        self.distance_table = None
        self.truck1 = None
        self.truck2 = None
        self.msg("Student ID: 011576592", sleep=0.33)
        self.msg("Student name: Gino Curtis", sleep=0.33)
        self.msg("Data Structures and Algorithms II (C950)", newlines=2, sleep=0.33)
        self.msg("Welcome to the Program's Interface!", sleep=1)
        input("Press the 'return' key to begin...\n")

    def msg(self, message: str, newlines=1, sleep=1):
        end = ""
        time.sleep(sleep)
        for _ in range(newlines):
            end += "\n"
        print(message, end=end)
        
    def load_package_data(self, packages_csv_file: str):
        self.msg(f"  - {packages_csv_file}", sleep=0.33)
        self.package_hashtable = PackageHashTable()
        self.package_hashtable.load_from_csv(packages_csv_file)

    def load_distance_data(self, distances_csv_file):
        self.msg(f"  - {distances_csv_file}", sleep=0.33)
        self.distance_table = DistanceTable()
        self.distance_table.load_from_csv(distances_csv_file)
        
    def initialize_trucks(self):
        if self.distance_table is None or self.package_hashtable is None:
            raise ValueError("Data tables not loaded yet.")
        self.truck1 = Truck(1, self.distance_table, self.package_hashtable)
        self.truck2 = Truck(2, self.distance_table, self.package_hashtable)

    def check_quit(self, response: str):
        if response == "q":
            sys.exit("Quitting program...")
        return
    
    def parse_time(self, unparsed_time: str):
        self.check_quit(unparsed_time)
        time_match = extract_time(unparsed_time)

        if time_match:
            return regex_to_datetime(time_match)
        return unparsed_time

    def parse_package_ids(self, package_ids: str):
        self.check_quit(package_ids)
        if not package_ids.strip():
            return []
        
        ids = package_ids.split(",")
        id_numbers = []

        for id in ids:
            try:
                id_number = int(id.strip())
                if id_number > len(self.package_hashtable.packages) or id_number < 0:
                    return id.strip()
                id_numbers.append(id_number)
            except ValueError:
                return id.strip()
        return id_numbers

    def prompt_for_time_to_check(self):
        prompt = "Enter time in format of HH:MM AM/PM (Enter 'q' to quit):\n"
        answer = self.parse_time(input(prompt))
        while not isinstance(answer, datetime):
            print(f"Invalid time: {answer}")
            answer = self.parse_time(input(prompt))
        time.sleep(0.33)
        return answer

    def prompt_for_packages_to_check(self):
        prompt = "Enter package IDs as comma separated list or leave blank for ALL (Enter 'q' to quit):\n"
        answer = self.parse_package_ids(input(prompt))

        while isinstance(answer, str):
            print(f"Invalid ID: {answer}")
            answer = self.parse_package_ids(input(prompt))
        time.sleep(0.33)
        return answer

    def show_packages(self, query_time: datetime, package_ids: list):
        time_string = query_time.strftime("%I:%M %p")
        if package_ids == []:
            print(f"\nTODO: Show all packages at {time_string}")
        else:
            print(f"\nTODO: Show packages {package_ids} at {time_string}")
            

    def run(self):
        self.msg("\nCSV Files Loaded:", sleep=0.33)
        self.load_package_data("wgups_package_file.csv")
        self.load_distance_data("wgups_distance_table.csv")
        self.msg("", sleep=0.33)
        self.initialize_trucks()

        while True:
            # Need functionality in UI to query packages/trucks with any given time
            package_ids = self.prompt_for_packages_to_check()
            query_time = self.prompt_for_time_to_check()
            self.show_packages(query_time, package_ids)
            break

if __name__ == "__main__":
    try:
        ui = UI()
        ui.run()
    except KeyboardInterrupt:
        sys.exit("\nQuitting program...")
