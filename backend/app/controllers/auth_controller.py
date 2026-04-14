from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
import uuid
from app import db

auth_bp = Blueprint('auth', __name__)


def generate_token(shop):
    payload = {
        'shop_id':   shop['shop_id'],
        'shop_name': shop['shop_name'],
        'lat':       shop.get('lat', 0),
        'lng':       shop.get('lng', 0),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    secret = os.getenv('JWT_SECRET', 'fallback_secret')
    return jwt.encode(payload, secret, algorithm='HS256')


@auth_bp.route('/register', methods=['POST'])
def register():
    data      = request.json
    shop_name = data.get('shop_name')
    email     = data.get('email')
    password  = data.get('password')
    address   = data.get('address')
    lat       = data.get('lat')
    lng       = data.get('lng')

    if not all([shop_name, email, password, address, lat, lng]):
        return jsonify({"error": "Missing required fields or GPS coordinates"}), 400

    if db.shops.find_one({"email": email}):
        return jsonify({"error": "Shop with this email already exists"}), 409

    shop_id = f"SHOP-{str(uuid.uuid4())[:6].upper()}"

    new_shop = {
        "shop_id":       shop_id,
        "shop_name":     shop_name,
        "email":         email,
        "password":      generate_password_hash(password),
        "address":       address,
        "lat":           float(lat),
        "lng":           float(lng),
        "green_credits": 0,
        "total_orders":  0,
        "total_spent":   0,
    }
    db.shops.insert_one(new_shop)

    token = generate_token(new_shop)
    return jsonify({
        "message": "Registration successful",
        "token": token,
        "shop": {
            "shop_id":       shop_id,
            "shop_name":     shop_name,
            "lat":           float(lat),
            "lng":           float(lng),
            "green_credits": 0,
            "total_orders":  0,
            "total_spent":   0,
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data     = request.json
    email    = data.get('email')
    password = data.get('password')

    shop = db.shops.find_one({"email": email})
    if not shop or not check_password_hash(shop['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(shop)
    return jsonify({
        "message": "Login successful",
        "token": token,
        "shop": {
            "shop_id":       shop['shop_id'],
            "shop_name":     shop['shop_name'],
            "lat":           shop.get('lat'),
            "lng":           shop.get('lng'),
            "green_credits": shop.get('green_credits', 0),
            "total_orders":  shop.get('total_orders', 0),
            "total_spent":   shop.get('total_spent', 0),
        }
    }), 200


@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Returns fresh shop data including latest green_credits."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    token = auth_header.split(' ')[1]
    try:
        secret  = os.getenv('JWT_SECRET', 'fallback_secret')
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    shop = db.shops.find_one({"shop_id": payload['shop_id']}, {'_id': 0, 'password': 0})
    if not shop:
        return jsonify({"error": "Shop not found"}), 404
    return jsonify(shop), 200
