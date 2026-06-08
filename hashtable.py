#!/usr/bin/env python3
from package import Package

class HashTable:
    def __init__(self):
        self.hashtable = {}

    # Requirement A
    def add_package(self, package_id, package_weight=None, delivery_address=None, delivery_state=None, delivery_city=None, delivery_zip_code=None, delivery_deadline=None, delivery_status=None, special_notes=None):
        # Convert to string
        package_id = str(package_id)

        # Insert information into hashtable/dictionary
        self.hashtable[package_id] = {
            "package_weight": package_weight,
            "delivery_address": delivery_address,
            "delivery_city": delivery_city,
            "delivery_state": delivery_state,
            "delivery_zip_code": delivery_zip_code,
            "delivery_deadline": delivery_deadline,
            "delivery_status": delivery_status,
            "special_notes": special_notes
        }

    # Requirement B
    def get_package(self, package_id):
        # Convert to string
        package_id = str(package_id)
        package_data = self.hashtable.get(package_id)
        # Return package object
        return Package(package_id, package_data)
        