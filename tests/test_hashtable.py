#!/usr/bin/env python3
from hashtable import HashTable

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

def test_hashtable():
    ht = HashTable()
    
    pkg_id = 99
    ht.add_package(
        pkg_id,
        package_weight=3,
        delivery_address="123 Main St",
        delivery_city="Salt Lake City",
        delivery_state="UT",
        delivery_zip_code=12345,
        delivery_deadline="EOD",
        delivery_status="en route",
        special_notes="Can only be on truck 2"
    )
    assert ht.hashtable != {}
    pkg = ht.get_package(pkg_id)
    assert int(pkg.id) == pkg_id
    assert pkg.weight is not None
    assert pkg.address is not None
    assert pkg.city is not None
    assert pkg.state is not None
    assert pkg.zip_code is not None
    assert pkg.deadline is not None
    assert pkg.status is not None
    assert pkg.notes is not None

