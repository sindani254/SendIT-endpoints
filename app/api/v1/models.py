parcels = [
    {
        'id': 1,
        'owner_id': 1,
        'item_name': 'Geforce GTX 1060 iGame',
        'origin': 'nairobi cbd',
        'pickup_location': 'zimmerman base',
        'price': 45000,
        'status': 'delivered'
    },
    {
        'id': 2,
        'owner_id': 2,
        'item_name': 'Geforce GTX 1080 ti',
        'origin': 'nairobi cbd',
        'pickup_location': 'zimmerman base',
        'price': 105000,
        'status': 'in transit'
    },
    {
        'id': 3,
        'owner_id': 1,
        'item_name': 'Geforce GTX 1050 ti',
        'origin': 'nairobi cbd',
        'pickup_location': 'base',
        'price': 85000,
        'status': 'cancelled'
    }
]


class Parcel():

    def __init__(self, item_name, origin, owner_id, pickup_location, price, status):
        self.item_name = item_name
        self.origin = origin
        self.owner_id = owner_id
        self.pickup_location = pickup_location
        self.price = price
        self.status = status
