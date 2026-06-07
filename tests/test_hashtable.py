#!/usr/bin/env python3
from ..hashtable import HashTable

# TODO Tests to cover
'''Test deadlines - EOD, 9:00 AM, 10:30 AM'''
'''Test special notes
- Can only be on truck 2
- Delayed on flight---will not arrive to depot until 9:05 am
- Wrong address listed
- 94 Must be delivered with 95,99
- 96 Must be delivered with 93,99
- 100 Must be delivered with 93,95
'''

test1_package_id = 99
test1_package_weight = 10
test1_address = "123 E Main St"
test1_city = "Zootopia"
test1_state = "UT"
test1_zip_code = 12345
test1_deadline = "EOD"
test1_status = "En Route"
test1_special_notes = ""
