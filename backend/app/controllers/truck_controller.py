from flask import Blueprint, jsonify, request
from app import socketio, db
from .auction_controller import start_auction_in_memory
import jwt
import os

truck_bp = Blueprint('truck', __name__)

FLEET = {
    "T-1001": {
        "truck_id": "T-1001", "driver": "Ramesh Kumar", "status": "In Transit",
        "current_temperature": -18, "humidity": 62, "remaining_shelf_life_hours": 48,
        "destination": "Durgapur Central Hub", "origin": "Kolkata Cold Storage",
        "distance_left_km": 87, "eta_hours": 3, "speed_kmh": 62,
        "lat": 23.374, "lng": 87.101,
        "cargo_type": "Frozen Goods",
        "cargo_image": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&q=80",
        "alert_level": "normal", "green_credits_earned": 12
    },
    "T-1002": {
        "truck_id": "T-1002", "driver": "Suresh Patel", "status": "In Transit",
        "current_temperature": 4, "humidity": 78, "remaining_shelf_life_hours": 18,
        "destination": "Asansol Market Yard", "origin": "Burdwan Farm Gate",
        "distance_left_km": 34, "eta_hours": 1, "speed_kmh": 55,
        "lat": 23.523, "lng": 87.198,
        "cargo_type": "Fresh Vegetables",
        "cargo_image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&q=80",
        "alert_level": "warning", "green_credits_earned": 8
    },
    "T-1003": {
        "truck_id": "T-1003", "driver": "Priya Singh", "status": "Loading",
        "current_temperature": 6, "humidity": 55, "remaining_shelf_life_hours": 72,
        "destination": "Dhanbad Retail Hub", "origin": "Ranchi Dairy Co-op",
        "distance_left_km": 142, "eta_hours": 5, "speed_kmh": 0,
        "lat": 23.661, "lng": 87.421,
        "cargo_type": "Dairy & Eggs",
        "cargo_image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&q=80",
        "alert_level": "normal", "green_credits_earned": 5
    }
}

# Product image map — matches catalogue product_ids to Unsplash images
PRODUCT_IMAGES = {
    "PRD-001": "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=200&q=80",
    "PRD-002": "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=200&q=80",
    "PRD-003": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=200&q=80",
    "PRD-004": "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=200&q=80",
    "PRD-005": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=200&q=80",
    "PRD-006": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=200&q=80",
    "PRD-007": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=200&q=80",
    "PRD-008": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=200&q=80",
    "PRD-009": "https://images.unsplash.com/photo-1598974542316-24e03bc29c0f?w=200&q=80",
    "PRD-010": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200&q=80",
    "PRD-011": "https://images.unsplash.com/photo-1599940824399-b87987ceb72a?w=200&q=80",
    "PRD-012": "https://images.unsplash.com/photo-1506976785307-8732e854ad02?w=200&q=80",
    "PRD-013": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=200&q=80",
    "PRD-014": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=200&q=80",
    "PRD-015": "https://images.unsplash.com/photo-1559181567-c3190ca9be46?w=200&q=80",
}

def get_shop_from_token():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ')[1]
    try:
        secret = os.getenv('JWT_SECRET', 'fallback_secret')
        return jwt.decode(token, secret, algorithms=['HS256'])
    except Exception:
        return None


@truck_bp.route('/fleet', methods=['GET'])
def get_fleet():
    """
    Returns only the trucks that have orders from this shop.
    If no orders yet, returns an EMPTY array.
    """
    shop = get_shop_from_token()
    if not shop:
        return jsonify([]), 200 # <-- FIXED: Return empty

    # Find all truck IDs assigned to this shop's orders
    shop_orders = list(db.orders.find(
        {"shop_id": shop['shop_id'], "assigned_truck": {"$exists": True}},
        {"assigned_truck": 1}
    ))
    assigned_truck_ids = list(set(o['assigned_truck'] for o in shop_orders if o.get('assigned_truck')))

    if not assigned_truck_ids:
        # No orders yet — return empty array!
        return jsonify([]), 200 # <-- FIXED: Return empty

    # Return only trucks this shop has orders on
    shop_fleet = [FLEET[tid] for tid in assigned_truck_ids if tid in FLEET]
    return jsonify(shop_fleet), 200


@truck_bp.route('/status', methods=['GET'])
def get_truck_status():
    return jsonify(FLEET["T-1001"]), 200


@truck_bp.route('/status/<truck_id>', methods=['GET'])
def get_single_truck(truck_id):
    truck = FLEET.get(truck_id)
    if not truck:
        return jsonify({"error": "Truck not found"}), 404
    return jsonify(truck), 200


@truck_bp.route('/cargo/<truck_id>', methods=['GET'])
def get_truck_cargo(truck_id):
    """
    Returns the real cargo batches for a truck — built from
    the authenticated shop's actual order items for that truck.
    """
    shop = get_shop_from_token()
    if not shop:
        return jsonify({"error": "Unauthorized"}), 401

    truck = FLEET.get(truck_id)
    if not truck:
        return jsonify({"error": "Truck not found"}), 404

    # Find all confirmed orders from this shop on this truck
    orders = list(db.orders.find(
        {"shop_id": shop['shop_id'], "assigned_truck": truck_id},
        {"_id": 0, "order_id": 1, "items": 1, "status": 1}
    ))

    cargo_batches = []
    for order in orders:
        for item in order.get('items', []):
            temp = truck['current_temperature']
            # Check if temp is out of range for this item
            storage = item.get('storage_temp', '')
            is_spoiling = False
            if '-18' in storage and temp > -10:
                is_spoiling = True
            elif '2-4' in storage and temp > 8:
                is_spoiling = True
            elif '4-8' in storage and temp > 12:
                is_spoiling = True
            elif '12' in storage and temp > 20:
                is_spoiling = True

            shelf = item.get('shelf_life_days', 30)
            if shelf <= 3:
                health = 'Critical'
            elif shelf <= 7:
                health = 'Warning'
            elif shelf <= 14:
                health = 'Good'
            else:
                health = 'Excellent'

            cargo_batches.append({
                "id":         f"{item['product_id']}-{order['order_id'][-4:]}",
                "product_id": item['product_id'],
                "name":       item['name'],
                "quantity":   item['quantity'],
                "unit":       item['unit'],
                "temp":       temp,
                "health":     health,
                "expiry":     f"{shelf} days",
                "storage_temp": item.get('storage_temp', 'N/A'),
                "supplier":   item.get('supplier', ''),
                "order_id":   order['order_id'],
                "image":      PRODUCT_IMAGES.get(item['product_id'],
                              "https://images.unsplash.com/photo-1542838132-92c53300491e?w=200&q=80"),
                "isSpoiling": is_spoiling,
                "spanRow":    1,
                "spanCol":    1,
            })

    return jsonify({
        "truck":   truck,
        "cargo":   cargo_batches,
        "shop_id": shop['shop_id'],
    }), 200


@truck_bp.route('/sensor-update', methods=['POST'])
def receive_sensor_data():
    data       = request.json
    truck_id   = data.get("truck_id")
    batch_id   = data.get("batch_id")
    batch_name = data.get("batch_name")
    current_temp = data.get("temp")
    truck_lat  = data.get("truck_lat", 23.5742)
    truck_lng  = data.get("truck_lng", 87.3203)

    print(f"📡 [SERVER] IoT Ping from {truck_id} | Batch: {batch_id} | Temp: {current_temp}°C")

    if truck_id in FLEET:
        FLEET[truck_id]["current_temperature"] = current_temp
        if current_temp > 0 and FLEET[truck_id].get("cargo_type") == "Frozen Goods":
            FLEET[truck_id]["alert_level"] = "critical"
        elif current_temp > 8:
            FLEET[truck_id]["alert_level"] = "warning"

    if current_temp > 0:
        print(f"🚨 CRITICAL TEMP in {batch_id}! Triggering Auction...")
        start_auction_in_memory(
            auction_id=f"A-{batch_id}",
            truck_id=truck_id,
            batch_item=f"URGENT: {batch_name} (Temp Breach: {current_temp}°C)",
            base_price=800,
            truck_lat=truck_lat,
            truck_lng=truck_lng,
        )
        return jsonify({"status": "Anomaly Detected", "action": "Auction Triggered"}), 200

    return jsonify({"status": "Normal", "action": "None"}), 200