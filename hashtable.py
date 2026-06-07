#!/usr/bin/env python3

class HashTable:
    def __init__(self):
        self.hashtable = {}

    # Requirement A
    def add_package(self, pkg_id, pkg_weight=None, d_address=None, d_state=None, d_city=None, d_zip_code=None, d_deadline=None, d_status=None, special_notes=None):
        # Convert to string
        pkg_id = str(pkg_id)

        # Insert information into hashtable/dictionary
        self.hashtable[pkg_id] = {
            "package_weight": pkg_weight,
            "delivery_address": d_address,
            "delivery_city": d_city,
            "delivery_state": d_state,
            "delivery_zip_code": d_zip_code,
            "delivery_deadline": d_deadline,
            "delivery_status": d_status,
            "special_notes": special_notes
        }

    # Requirement B
    def get_package(self, pkg_id):
        # Convert to string
        pkg_id = str(pkg_id)

        # Return package data or None
        return self.hashtable.get(pkg_id)
        