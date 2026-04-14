from flask import Blueprint, jsonify, request
from app import socketio
from .auction_controller import start_auction_in_memory

truck_bp = Blueprint('truck', __name__)

# Multi-truck fleet data with live simulated positions
FLEET = {
    "T-1001": {
        "truck_id": "T-1001",
        "driver": "Ramesh Kumar",
        "status": "In Transit",
        "current_temperature": -18,
        "humidity": 62,
        "remaining_shelf_life_hours": 48,
        "destination": "Durgapur Central Hub",
        "origin": "Kolkata Cold Storage",
        "distance_left_km": 87,
        "eta_hours": 3,
        "speed_kmh": 62,
        "lat": 23.374,
        "lng": 87.101,
        "cargo_type": "Frozen Goods",
        "cargo_image": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&q=80",
        "alert_level": "normal",
        "green_credits_earned": 12
    },
    "T-1002": {
        "truck_id": "T-1002",
        "driver": "Suresh Patel",
        "status": "In Transit",
        "current_temperature": 4,
        "humidity": 78,
        "remaining_shelf_life_hours": 18,
        "destination": "Asansol Market Yard",
        "origin": "Burdwan Farm Gate",
        "distance_left_km": 34,
        "eta_hours": 1,
        "speed_kmh": 55,
        "lat": 23.523,
        "lng": 87.198,
        "cargo_type": "Fresh Vegetables",
        "cargo_image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&q=80",
        "alert_level": "warning",
        "green_credits_earned": 8
    },
    "T-1003": {
        "truck_id": "T-1003",
        "driver": "Priya Singh",
        "status": "Loading",
        "current_temperature": 6,
        "humidity": 55,
        "remaining_shelf_life_hours": 72,
        "destination": "Dhanbad Retail Hub",
        "origin": "Ranchi Dairy Co-op",
        "distance_left_km": 142,
        "eta_hours": 5,
        "speed_kmh": 0,
        "lat": 23.661,
        "lng": 87.421,
        "cargo_type": "Dairy & Eggs",
        "cargo_image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&q=80",
        "alert_level": "normal",
        "green_credits_earned": 5
    }
}

@truck_bp.route('/fleet', methods=['GET'])
def get_fleet():
    return jsonify(list(FLEET.values())), 200

@truck_bp.route('/status', methods=['GET'])
def get_truck_status():
    return jsonify(FLEET["T-1001"]), 200

@truck_bp.route('/status/<truck_id>', methods=['GET'])
def get_single_truck(truck_id):
    truck = FLEET.get(truck_id)
    if not truck:
        return jsonify({"error": "Truck not found"}), 404
    return jsonify(truck), 200

@truck_bp.route('/sensor-update', methods=['POST'])
def receive_sensor_data():
    data = request.json
    truck_id = data.get("truck_id")
    batch_id = data.get("batch_id")
    batch_name = data.get("batch_name")
    current_temp = data.get("temp")

    print(f"📡 [SERVER] IoT Ping from {truck_id} | Batch: {batch_id} | Temp: {current_temp}°C")

    # Update in-memory fleet position/temp
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
            base_price=50
        )
        return jsonify({"status": "Anomaly Detected", "action": "Auction Triggered"}), 200

    return jsonify({"status": "Normal", "action": "None"}), 200
