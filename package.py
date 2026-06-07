#!/usr/bin/env python3

# Package class to simplify data access
class Package:
    def __init__(self, pkg_id, **pkgdict):
        self.id = pkg_id
        self.weight = pkgdict.get("package_weight")
        self.address = pkgdict.get("delivery_address")
        self.city = pkgdict.get("delivery_city")
        self.state = pkgdict.get("delivery_state")
        self.zip_code = pkgdict.get("delivery_zip_code")
        self.deadline = pkgdict.get("delivery_deadline")
        self.status = pkgdict.get("delivery_status")
        self.notes = pkgdict.get("special_notes")
