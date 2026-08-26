import sys
import time
from datetime import datetime
from packages import PackageHashTable
from locations import DistanceTable
from timeinfo import TimeInfo
from truck import Truck

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
        time_match = TimeInfo.extract_regex_time(unparsed_time)

        if time_match:
            return TimeInfo.regex_to_datetime(time_match)
        return unparsed_time

    def parse_package_ids(self, package_ids: str):
        self.check_quit(package_ids)
        if not package_ids.strip():
            return []
        
        ids = package_ids.split(",")
        id_numbers = []

        for id in ids:
            try:
                id = id.strip()
                id_number = int(id)
                if id_number > len(self.package_hashtable.packages) or id_number < 1:
                    return id
                id_numbers.append(id_number)
            except ValueError:
                return id
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