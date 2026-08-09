import re
import csv
from pathlib import Path
from datetime import datetime
from delivery import Truck, TimeInfo


# Helper class to represent a given package
class Package:
    def __init__(self, package_id, **package_data):
        self.id = int(package_id)
        self.address = package_data.get("delivery_address")
        self.city = package_data.get("delivery_city")
        self.weight = package_data.get("package_weight")
        self.state = package_data.get("delivery_state")
        self.zip_code = package_data.get("delivery_zip_code")
        self.deadline = package_data.get("delivery_deadline")
        self.notes = package_data.get("special_notes")
        self.status = package_data.get("delivery_status")

    def update_status(self, status_update: str, update_time: datetime):
        status_update = status_update.strip().lower()
        if status_update not in ("delayed", "at the hub", "en route", "delivered"):
            raise ValueError(f"Invalid status: {status_update}")
        # Don't update package already delivered
        if "delivered" in self.status:
            return
        self.status = f"{status_update} - {TimeInfo.timestamp(update_time)}"

### Hash Table data structure with tasks A & B ###
class PackageHashTable:
    def __init__(self, size=40):
        self.packages = [None] * size
        self.package_groups = [] # Package groups to be delivered together

    # Helper class to convert deadlines to datetime objects
    def convert_to_datetime(self, deadline: str):
        if deadline == "EOD":
            return TimeInfo.day_end_time()
        time_match = TimeInfo.extract_regex_time(deadline)
        return TimeInfo.regex_to_datetime(time_match)
    
    def update_package_status(self, package: Package, status: str, update_time: datetime):
        package.update_status(status, update_time)

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

    # Check a package for delivery constraints
    def is_deliverable(self, package: Package, truck: "Truck", group_check=True):
        # At the hub?
        if "at the hub" not in package.status:
            return False
        # Truck 2 only?
        if "Can only be on truck 2" in package.notes and truck.id != 2:
            return False
        # Wrong address listed?
        if "Wrong address listed" in package.notes:
            available_time = TimeInfo.time_today(hour=10, minute=20)
            # Truck time must be later than package available time
            if truck.time < available_time:
                return False
        # Package in a package group?
        if group_check:
            for package_group in self.package_groups:
                if package in package_group:
                    # All packages in package group must be deliverable
                    if not all(self.is_deliverable(pkg, truck, group_check=False) for pkg in package_group):
                        return False
        # All checks passed
        return True

    # Get deliverable packages for truck
    def get_deliverable_packages(self, truck: "Truck"):
        deliverable_packages = []
        for package in self.packages:
            if self.is_deliverable(package, truck):
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
        id_groups = []
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
                update_time = TimeInfo.day_start_time()
                if "Delayed" in special_notes:
                    delivery_status = "delayed"
                else:
                    delivery_status = "at the hub"

                # Track package ids to be grouped
                if "Must be delivered with" in special_notes:
                    group = []
                    for id in re.findall(r'\d+', special_notes) + [package_id]:
                        group.append(int(id))
                    id_groups.append(group)

                # Add package using index from header row
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

        # Merge package groups with overlapping packages
        merged_groups = []
        for id_group in id_groups:
            package_group = set([self.get_package(id) for id in id_group])

            # Any group in merged groups that has intersecting elements with the current package group
            overlapping_groups = [group for group in merged_groups if group & package_group]

            for group in overlapping_groups:
                merged_groups.remove(group)
                package_group = package_group | group
            merged_groups.append(package_group)
        # Set package groups that must be delivered together
        self.package_groups = merged_groups
