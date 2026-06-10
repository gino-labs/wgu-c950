#!/usr/bin/env python3
from package import Package

class HashTable:
    def __init__(self, size=40):
        self.hashtable = [None] * size

    # Requirement A
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
        index = package % len(self.hashtable)
        self.hashtable[index] = package

    # Requirement B
    def get_package(self, package_id: int) -> Package:
        # Return Package object at index
        index = package_id % len(self.hashtable)
        return self.hashtable[index]
        