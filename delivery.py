import re
from datetime import datetime, timedelta
from locations import DistanceTable
from packages import PackageHashTable

class TimeInfo:
    def day_start_time() -> datetime:
        return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    def day_end_time() -> datetime:
        return TimeInfo.day_start_time() + timedelta(hours=12)

    def elapsed_time(starting_time, hours=0, minutes=0, seconds=0) -> datetime:
        if seconds < 0:
            seconds = 0
        if minutes < 0:
            minutes = 0
        if hours < 0:
            hours = 0
        elapsed_datetime = TimeInfo.day_start_time() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if elapsed_datetime > TimeInfo.day_end_time():
            raise ValueError("Elapsed time past EOD")
        return elapsed_datetime

    def time_today(hour=0, minute=0):
        point_in_time = TimeInfo.day_start_time().replace(hour=hour, minute=minute)
        if point_in_time < TimeInfo.day_start_time() or point_in_time > TimeInfo.day_end_time():
            raise ValueError("Time specified outside of operating times.")

    def timestamp(datetime_obj: datetime) -> str:
        return datetime_obj.strftime("%I:%M %p")

    # Search a string for a date time match
    def extract_regex_time(_string: str) -> re.Match:
        return re.search(r'\b(1[0-2]|0?[1-9]):([0-5][0-9])\s*([AP]M)\b', _string, re.IGNORECASE)

    # Convert regex match to datetime object
    def regex_to_datetime(time_match: re.Match) -> datetime:
        hour = time_match.group(1)
        minute = time_match.group(2)
        meridiem = time_match.group(3).upper()
        time_string = datetime.strptime(f"{hour}:{minute} {meridiem}", "%I:%M %p")
        return TimeInfo.day_start_time().replace(hour=time_string.hour, minute=time_string.minute)

class Truck:
    def __init__(self, truck_id: int, distance_table: DistanceTable, package_hashtable: PackageHashTable):
        self.id = truck_id
        self.speed = 18
        self.capacity = 16
        self.miles_driven = 0
        self.loaded_packages = []
        self.distance_table = distance_table
        self.package_hashtable = package_hashtable
        self.time = TimeInfo.day_start_time()
        self.current_location = distance_table.get_location("Western Governors University")


    def load_packages(self, return_by_time=None, limit=None):
        if not limit:
            limit = self.capacity
        if isinstance(return_by_time, str):
            time_match = TimeInfo.extract_regex_time(return_by_time)
            return_by_time = TimeInfo.regex_to_datetime(time_match)
        if not return_by_time:
            return_by_time = TimeInfo.day_end_time()
       
        
        deliverable_packages = self.package_hashtable.get_deliverable_packages(self)
        for package in deliverable_packages:
            pass # TODO

    def deliver_packages(self):
        pass # TODO