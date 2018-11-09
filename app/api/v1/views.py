from flask import jsonify, abort, make_response, request, Blueprint
from .models import parcels

NOT_FOUND = 'data NOT found'
BAD_REQUEST = 'Bad request'

v1_blueprint = Blueprint(
    'v1', __name__
)


def _get_order(id):
    return [parcel for parcel in parcels if parcel['id'] == id]


def _entry_exists_for_delivery_order(item_name):
    return [parcel for parcel in parcels if parcel["item_name"] == item_name]


@v1_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@v1_blueprint.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@v1_blueprint.route('/api/v1')
def index():
    return jsonify({"welcome": "crackers ni wale wase"})


@v1_blueprint.route('/api/v1/parcels', methods=['POST'])
def post_delivery_order():
    item_id = 0
    if not request.json or 'item_name' not in request.json:
        abort(400)
    orders = parcels
    if len(orders) == 0:
        item_id = 1
    else:
        item_id = parcels[-1].get("id") + 1

    owner_id = request.json.get('owner_id')
    item_name = request.json.get('item_name')
    origin = request.json.get('origin')
    pickup_location = request.json.get('pickup_location')
    price = request.json.get('price')
    status = request.json.get('status')

    if _entry_exists_for_delivery_order(item_name):
        return jsonify({'message': "entry exists"})
    parcel = {
        "id": item_id,
        "owner_id": owner_id,
        "item_name": item_name,
        "origin": origin,
        "pickup_location": pickup_location,
        "price": price,
        "status": status
    }
    parcels.append(parcel)
    return jsonify({'parcel': parcel}), 201


@v1_blueprint.route('/api/v1/parcels', methods=['GET'])
def get_all_parcel_orders():
    orders = parcels
    if len(orders) == 0:
        return jsonify({'message': 'no orders have been posted'})
    return jsonify({'all orders': parcels})


# get a particular parcel delivery order
@v1_blueprint.route('/api/v1/parcels/<int:id>', methods=['GET'])
def get_particular_parcel_order(id):
    order = _get_order(id)
    if not order:
        abort(404)
    return jsonify({'order': order})


# get parcel orders belonging to a particular user
@v1_blueprint.route('/api/v1/users/<int:id>/parcels', methods=['GET'])
def get_user_parcel_delivery_orders(id):
    parcel = [parcel for parcel in parcels if parcel['owner_id'] == id]
    if not parcel:
        abort(404)
    return jsonify({"parcels": parcel})


@v1_blueprint.route('/api/v1/parcels/<int:id>/cancel', methods=['PUT'])
def cancel_delivery_order(id):
    if not request.json:
        abort(400)
    orders = _get_order(id)
    if not orders:
        abort(404)
    elif orders[0]['status'] == "delivered":
        return jsonify({"error": "order has already been delivered!!"})
    elif orders[0]['status'] == "cancelled":
        return jsonify({"error": "order has already been cancelled!!"})
    orders[0]['status'] = "cancelled"
    return jsonify({'delivery order': orders})
