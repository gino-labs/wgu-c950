#!/usr/bin/env python3

class HashTable:
    def __init__(self):
        self.hashtable = {}

    # Requirement A
    def add_package(self, pkg_id, pkg_weight=None, d_address=None, d_deadline=None, d_city=None, d_zip_code=None, d_status=None):
        # Convert to string
        pkg_id = str(pkg_id)

        # Insert information into hashtable/dictionary
        self.hashtable[pkg_id] = {
            "package_weight": pkg_weight,
            "delivery_address": d_address,
            "delivery_city": d_city,
            "delivery_zip_code": d_zip_code,
            "delivery_deadline": d_deadline,
            "delivery_status": d_status
        }

    def get_package(self):
        pass