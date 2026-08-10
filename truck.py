from timeinfo import TimeInfo

class Truck:
    def __init__(self, truck_id: int, distance_table, package_hashtable):
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