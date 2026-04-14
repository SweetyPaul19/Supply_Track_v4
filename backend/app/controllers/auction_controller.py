from flask import Blueprint, jsonify, request
from app import socketio
from flask_socketio import emit
import datetime

auction_bp = Blueprint('auction', __name__)

active_auction_state = {
    "is_active":            False,
    "auction_id":           None,
    "truck_id":             None,
    "batch_item":           None,
    "base_price":           0,
    "current_highest_bid":  0,
    "highest_bidder_id":    None,
    "highest_bidder_name":  None,
    "started_at":           None,
    "bid_history":          []
}


def start_auction_in_memory(auction_id, truck_id, batch_item, base_price,
                             truck_lat=23.574183559967356, truck_lng=87.32041803582375):
    global active_auction_state

    active_auction_state.update({
        "is_active":           True,
        "auction_id":          auction_id,
        "truck_id":            truck_id,
        "batch_item":          batch_item,
        "base_price":          base_price,
        "current_highest_bid": base_price,
        "highest_bidder_id":   None,
        "highest_bidder_name": None,
        "started_at":          datetime.datetime.utcnow().isoformat(),
        "bid_history":         []
    })

    emergency_data = {
        "auction_id":    auction_id,
        "truck_id":      truck_id,
        "batch_item":    batch_item,
        "current_price": base_price,
        "time_limit":    60,
        "truck_lat":     truck_lat,
        "truck_lng":     truck_lng,
    }

    socketio.emit('emergency_auction_started', emergency_data)
    print(f"🔨 [AUCTION] Started: {auction_id} | Item: {batch_item} | Base: ₹{base_price}")


@auction_bp.route('/test-trigger', methods=['GET'])
def test_trigger():
    start_auction_in_memory(
        auction_id="A-DEMO-001",
        truck_id="T-1001",
        batch_item="20kg Frozen Chicken Breasts (Temp Breach: 15°C)",
        base_price=800,
        truck_lat=23.5742,
        truck_lng=87.3203
    )
    return jsonify({"status": "Success", "message": "Demo auction started!"}), 200


@auction_bp.route('/trigger', methods=['POST'])
def trigger_auction():
    data = request.json
    start_auction_in_memory(
        auction_id=data.get('auction_id', 'A-001'),
        truck_id=data.get('truck_id', 'T-1001'),
        batch_item=data.get('batch_item', 'Unknown Batch'),
        base_price=data.get('base_price', 500),
        truck_lat=data.get('truck_lat', 23.5742),
        truck_lng=data.get('truck_lng', 87.3203),
    )
    return jsonify({"status": "Auction triggered"}), 200


@auction_bp.route('/status', methods=['GET'])
def get_auction_status():
    state = dict(active_auction_state)
    state.pop('_id', None)
    return jsonify(state), 200


@auction_bp.route('/history', methods=['GET'])
def get_bid_history():
    return jsonify(active_auction_state.get("bid_history", [])), 200


@socketio.on('submit_bid')
def handle_bid(data):
    global active_auction_state

    new_bid   = data.get('bid_amount', 0)
    shop_id   = data.get('shop_id', 'unknown')
    shop_name = data.get('shop_name', 'Unknown Shop')

    if not active_auction_state["is_active"]:
        emit('bid_rejected', {"reason": "No active auction"})
        return

    if new_bid <= active_auction_state["current_highest_bid"]:
        emit('bid_rejected', {
            "reason": f"Bid must be higher than ₹{active_auction_state['current_highest_bid']}"
        })
        return

    active_auction_state["current_highest_bid"] = new_bid
    active_auction_state["highest_bidder_id"]   = shop_id
    active_auction_state["highest_bidder_name"] = shop_name
    active_auction_state["bid_history"].append({
        "shop_id":   shop_id,
        "shop_name": shop_name,
        "amount":    new_bid,
        "time":      datetime.datetime.utcnow().strftime("%H:%M:%S")
    })

    print(f"💰 [BID] {shop_name} bid ₹{new_bid}")

    emit('price_update', {
        "new_price":   new_bid,
        "bidder_id":   shop_id,
        "bidder_name": shop_name,
        "bid_history": active_auction_state["bid_history"][-5:]
    }, broadcast=True)


@socketio.on('auction_ended')
def handle_auction_end(data):
    global active_auction_state
    winner_id   = active_auction_state["highest_bidder_id"]
    winner_name = active_auction_state["highest_bidder_name"]
    final_price = active_auction_state["current_highest_bid"]

    active_auction_state["is_active"] = False

    socketio.emit('auction_result', {
        "winner_id":   winner_id,
        "winner_name": winner_name,
        "final_price": final_price,
        "auction_id":  active_auction_state["auction_id"],
        "truck_id":    active_auction_state["truck_id"],
    })

    print(f"🏆 [AUCTION ENDED] Winner: {winner_name} | Price: ₹{final_price}")
