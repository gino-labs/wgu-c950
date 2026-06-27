from data_structures import DistanceTable, PackageHashTable, Package

class Truck:
    def __init__(self, truck_number: int):
        self.truck_number = truck_number
        self.miles_driven = 0
        self.capacity = 16
        self.trip_counter = 1
        self.current_location_name = "Western Governors University"
        self.current_location_address = ""

    # Greedy Neighbor Algorithm Route
    def generate_delivery_route(self, packages_to_deliver: list[Package], distance_table: DistanceTable):
        current_location = self.current_location_name
        delivery_route = []
        while len(delivery_route) != len(packages_to_deliver) + 1:

            

    def load_truck(self, distance_table: DistanceTable, hashtable: PackageHashTable):
        '''
        Load 8 packages, then 16 on second truck, then first truck returns for remaining 16.
        '''
        
        # Truck 1, trip 1
        if self.truck_number == 1 and self.trip_counter == 1:
            pass
        # Truck 2
        elif self.truck_number == 2:
            pass
        # Truck 1, trip 2
        else:
            pass

        # Exclude packages not at the hub
        excluded_packages = []
        for package in hashtable.packages:
            if package.status != "At the hub":
                excluded_packages.append(package)



dt = DistanceTable()
ht = PackageHashTable()
ht.load_packages_from_csv()

truck1 = Truck(1)
truck1.load_truck(dt, ht)

for i, loc in enumerate(dt.locations, start=1):
    print(f"{i}: {loc.name}: {loc.address}")