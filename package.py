#!/usr/bin/env python3

# Package class to simplify data access
class Package:
    def __init__(self, package_id, **package_data):
        self.id = package_id
        self.weight = package_data.get("package_weight")
        self.address = package_data.get("delivery_address")
        self.city = package_data.get("delivery_city")
        self.state = package_data.get("delivery_state")
        self.zip_code = package_data.get("delivery_zip_code")
        self.deadline = package_data.get("delivery_deadline")
        self.status = package_data.get("delivery_status")
        self.notes = package_data.get("special_notes")
