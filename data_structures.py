#!/usr/bin/env python3
import csv
from pathlib import Path

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


### Hash Table data structure with tasks A & B
class PackageHashTable:
    def __init__(self, size=40):
        self.packages = [None] * size

    ### Requirement A
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

    ### Requirement B
    def get_package(self, package_id: int) -> Package:
        # Return Package object at index
        index = package_id % len(self.packages)
        return self.packages[index]
    
    # Load package data from csv task files
    def load_packages_from_csv(self, csv_file="wgups_package_file.csv"):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
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
    def __init__(self, name: str, address: str, zip: int):
        self.name = name
        self.address = address
        self.zip = zip
    


class Neighbor:
    def __init__(self, neighbor: Location, distance: float):
        self.neighbor = neighbor
        self.distance = distance

# Class for organizing distance table data
class DistanceTable:
    def __init__(self, csv_file="wgups_distance_table.csv"):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        self.table = self._parse_distance_table()

    # Parse data from table and return 2D list
    def _parse_distance_table(self):
        with open(self.csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            start_loading_data = False
            parsed_table = []

            for row in reader:
                if "DISTANCE BETWEEN HUBS IN MILES" in row:
                    start_loading_data = True

                if start_loading_data:
                    parsed_table.append(row)
        return parsed_table


