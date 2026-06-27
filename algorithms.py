from data_structures import DistanceTable, PackageHashTable, Package

class Truck:
    def __init__(self, truck_number: int):
        self.truck_number = truck_number
        self.miles_driven = 0
        self.capacity = 16
        self.trip_counter = 1

    def load_truck(self, distance_table: DistanceTable, hashtable: PackageHashTable):
        '''
        Load 8 packages
        '''
        excluded_packages = []
        for package in hashtable.packages:
            
            print(package.notes)

dt = DistanceTable()
ht = PackageHashTable()
ht.load_packages_from_csv()

truck1 = Truck(1)
truck1.load_truck(dt, ht)