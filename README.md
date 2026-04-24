# Supply Track

![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB) ![Flask + Socket.IO](https://img.shields.io/badge/Backend-Flask%20%2B%20Socket.IO-000000) ![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2) ![MongoDB](https://img.shields.io/badge/Database-MongoDB-FFCA28) ![GitHub Repo stars](https://img.shields.io/github/stars/Aritrajit-Guha/Supply_Track_v4?style=social)

LiveTrack is an AI-powered smart supply chain web application built for monitoring wholesale orders, cold-chain fleet movement, spoilage risk, and flash-auction based inventory recovery. It combines real-time truck visibility, order automation, and Gemini-powered assistance to make supply chain operations more practical and interactive than a static demo.

## Features

- Wholesale ordering flow with cart, invoice, and order history
- Shop authentication with JWT-based sessions
- Live fleet dashboard with truck routes, ETA, and cargo diagnostics
- Automated truck progression and delivery stage updates
- Rule-based spoilage risk scoring for cargo batches
- Gemini-powered AI Copilot chatbot for fleet and shop workflows
- AI shipment insights for fleet-level operational summaries
- Flash auction system with bid handling and live Socket.IO updates
- MongoDB-backed persistence for shops, orders, trucks, auctions, and bids
- Green credits and sustainability-focused order experience

## Tech Stack

- Frontend: React, Vite, React Router, Axios, Leaflet, Socket.IO Client
- Backend: Flask, Flask-SocketIO, Flask-CORS, PyJWT, PyMongo
- Database: MongoDB
- AI: Google Gemini API
- Deployment: Firebase Hosting for frontend, external backend hosting such as Render

## Project Structure

```text
Supply_Track_v4/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── __init__.py
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   └── services/
│   ├── .env.production.example
│   └── package.json
├── firebase.json
├── FIREBASE_DEPLOY.md
└── README.md
```

## Core Modules

- `frontend/src/pages/ShopDashboard.jsx`: catalogue, cart, orders, invoice, restock recommendations
- `frontend/src/pages/AdminDashboard.jsx`: fleet dashboard, map view, shipment insights, auction notifications
- `frontend/src/components/TruckView.jsx`: IoT-style truck cargo diagnostics and auction trigger flow
- `backend/app/controllers/auth_controller.py`: registration, login, profile APIs
- `backend/app/controllers/shop_controller.py`: catalogue, order creation, recommendations
- `backend/app/controllers/truck_controller.py`: fleet, truck status, cargo diagnostics, sensor handling
- `backend/app/controllers/auction_controller.py`: auction lifecycle, bids, active/history state
- `backend/app/controllers/ai_controller.py`: AI chatbot and shipment insights APIs
- `backend/app/services/`: Gemini integration, risk logic, fleet automation, auction persistence, recommendations

## AI Capabilities

LiveTrack uses Gemini as a backend-only intelligence layer. AI features are grounded in real application data and paired with rule-based fallbacks so the system still works when Gemini is unavailable.

- AI Copilot chatbot for shop and fleet dashboards
- Shipment Insights summary panel for live fleet operations
- Restock recommendation assistance based on order history
- Risk-aware supply chain reasoning layered on top of deterministic spoilage scoring

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Aritrajit-Guha/Supply_Track_v4.git
cd Supply_Track_v4
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env` from `backend/.env.example` and fill in your values:

```env
MONGO_URI=mongodb://localhost:27017/livetrack_db
BACKEND_URL=http://127.0.0.1:5000
FRONTEND_URL=http://localhost:5173
JWT_SECRET=your-jwt-secret
GEMINI_API_KEY=your-gemini-api-key
```

Run the backend:

```bash
py run.py
```

### 3. Frontend setup

```bash
cd ../frontend
npm install
```

Create `frontend/.env` for local development:

```env
VITE_BACKEND_URL=http://127.0.0.1:5000
VITE_FRONTEND_URL=http://localhost:5173
```

Run the frontend:

```bash
npm run dev
```

The app should open at `http://localhost:5173`.

## Environment Files

Tracked templates:

- `backend/.env.example`
- `frontend/.env.production.example`

Local-only files:

- `backend/.env`
- `backend/.env.production`
- `frontend/.env`
- `frontend/.env.production`

Do not commit real secrets such as:

- `MONGO_URI`
- `JWT_SECRET`
- `GEMINI_API_KEY`

## Deployment

### Frontend

The frontend is prepared for Firebase Hosting.

1. Create `frontend/.env.production`
2. Set the production backend URL
3. Build the frontend
4. Deploy with Firebase

Example production frontend env:

```env
VITE_BACKEND_URL=https://your-render-backend.onrender.com
VITE_FRONTEND_URL=https://your-firebase-site.web.app
```

Build and deploy:

```bash
cd frontend
npm run build
cd ..
firebase login
firebase use --add
firebase deploy
```

### Backend

The backend should be deployed separately on a Python-compatible host such as Render. Production backend env values should come from `backend/.env.production` or your hosting provider’s environment variable settings.

## Real-Time Flow

1. A shop registers and logs in
2. The shop places a wholesale order
3. A truck is assigned and tracked in the fleet dashboard
4. Fleet automation advances the delivery state over time
5. Cargo diagnostics evaluate spoilage risk
6. Flash auctions can be triggered for at-risk inventory
7. Nearby eligible shops receive live auction notifications
8. AI copilots summarize, explain, and recommend actions

## Notes

- Gemini is used sparingly and only through the backend
- Hot fleet and cargo APIs rely on rule-based logic for responsiveness
- Firebase Hosting serves only the frontend in the current deployment setup
- MongoDB remains the system of record for app data

## Future Improvements

- Stronger production-grade routing and dispatch logic
- Dedicated winner-side inventory transfer flow after auction completion
- Better analytics for demand prediction and sustainability insights
- CI/CD automation for Firebase and backend hosting

## License

This project is built as an academic/product demo project. Add a formal license here if you plan to open-source it publicly.
# SupplyTrack — Live-Track Smart Supply Chain

> **Google Solution Challenge Hackathon Project**
> Perishable goods tracking with real-time IoT monitoring, AI-powered shelf life prediction, and emergency auction system for at-risk cargo.

---

## What It Does

SupplyTrack moves beyond "where is my truck?" to **"what is the condition of the food inside?"**

Shop owners (supermarkets, convenience stores) use a web dashboard to restock inventory. Once an order is placed, IoT sensors inside the delivery truck continuously monitor temperature and humidity. If conditions deteriorate and cargo is at risk of spoiling, the system automatically triggers a **flash auction** — broadcasting to all nearby shops so the goods can be sold at a discount rather than wasted.

A Gemini AI layer sits across the entire flow: predicting shelf life from raw sensor readings, writing emergency auction listings, generating plain-English spoilage alerts, and advising shop owners on when to reorder after a delivery.

---

## Features

### Shop Owner Dashboard
- **Marketplace catalogue** — 15 wholesale products across Fruits, Vegetables, Dairy, Frozen, Grains, Oils and Poultry categories
- **Cart and checkout** — place bulk orders with automatic truck assignment
- **Order tracking** — live delivery stage progress (Confirmed → Loading → In Transit → Delivered)
- **Invoice view** — full invoice with line items, GST breakdown, and payment status
- **Green Credits** — earned on every order, bonus credits for buying near-expiry auction items
- **AI Reorder Advisor** — Gemini analyses a delivered invoice and tells you when to reorder each product

### Live Fleet Dashboard
- **Real-time map** — all trucks plotted on OpenStreetMap with colour-coded alert levels (green / amber / red)
- **Per-truck cargo view** — see every batch inside a truck, its current temperature, humidity, and health status
- **IoT sensor stream** — live sensor pings update cargo health in real time

### AI Features (Gemini 1.5 Flash)
- **Shelf Life Predictor** — replaces hard-coded logic with Gemini reasoning over sensor data to return `remaining_shelf_life_hours`, spoilage risk level, and recommended action
- **Spoilage Alert Summary** — plain-English 2-sentence alert with a clear action tag (`[ACTION: WAIT]`, `[ACTION: EXPEDITE]`, or `[ACTION: BID_AT_AUCTION]`)
- **AI Auction Description** — Gemini writes a compelling, factual emergency listing when an auction triggers
- **AI Reorder Advisor** — analyses delivered invoices and returns a per-product reorder schedule with reasons
- **SupplyTrack AI Chatbot** — floating chat widget in the shop dashboard, powered by Gemini with live shop context (orders, fleet status, low-stock items)
- **Route Optimiser** — Gemini recommends truck rerouting when an auction winner is assigned, with plain-English driver instructions

### Emergency Auction System
- Triggered automatically when IoT sensors detect a temperature breach
- Real-time Socket.IO broadcast to all connected shops
- Live bidding with price updates pushed to all clients
- 60-second countdown timer
- Winner receives rerouted truck delivery

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, React Router, Axios |
| Maps | Leaflet, React-Leaflet, OpenStreetMap |
| Real-time | Socket.IO client |
| Backend | Python, Flask, Flask-SocketIO, Flask-CORS |
| AI | Google Gemini 1.5 Flash (`google-generativeai`) |
| Database | MongoDB (Firestore migration path included) |
| Auth | JWT (`PyJWT`), bcrypt password hashing |
| IoT Simulation | Python script (`iot_simulator.py`) |
| Hosting | Firebase Hosting (frontend), Render/Railway (backend) |

---

## Project Structure

```
Supply_Track/
├── frontend/                        # Vite + React
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ShopDashboard.jsx    # Main shop owner interface
│   │   │   ├── AdminDashboard.jsx   # Fleet overview with live map
│   │   │   └── AuthPage.jsx         # Login / register
│   │   ├── components/
│   │   │   ├── TruckView.jsx        # Per-truck IoT cargo view
│   │   │   ├── AuctionModal.jsx     # Real-time bidding UI
│   │   │   └── AIChatWidget.jsx     # Gemini chatbot (floating)
│   │   ├── services/
│   │   │   ├── api.js               # Axios instance with JWT interceptor
│   │   │   └── socket.js            # Socket.IO client
│   │   └── context/
│   │       └── AuthContext.jsx      # Auth state provider
│   └── package.json
│
└── backend/                         # Flask
    ├── app/
    │   ├── __init__.py              # App factory, DB init, blueprint registration
    │   ├── controllers/
    │   │   ├── auth_controller.py   # Register, login, profile
    │   │   ├── shop_controller.py   # Catalogue, orders, invoices, green credits
    │   │   ├── truck_controller.py  # Fleet data, sensor webhook, cargo health
    │   │   ├── auction_controller.py# Socket auction logic, bidding
    │   │   └── ai_controller.py     # Gemini chat endpoint
    │   ├── services/
    │   │   ├── gemini_service.py    # All Gemini API functions
    │   │   ├── shelf_life_ml.py     # AI shelf life predictor
    │   │   └── routing_service.py   # AI route optimiser
    │   └── utils/
    │       └── iot_simulator.py     # Simulates IoT sensor pings
    ├── requirements.txt
    └── .env
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (free tier works) or local MongoDB
- Google Gemini API key — get one free at [aistudio.google.com](https://aistudio.google.com)

---

### Backend Setup

```bash
cd Supply_Track/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install google-generativeai  # AI feature
```

Create a `.env` file in the `backend/` folder:

```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/supplytrack
JWT_SECRET=your_super_secret_key_here
FRONTEND_URL=http://localhost:5173
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the server:

```bash
python run.py
# Flask runs on http://localhost:5000
```

---

### Frontend Setup

```bash
cd Supply_Track/frontend
npm install
```

Create a `.env` file in the `frontend/` folder:

```env
VITE_BACKEND_URL=http://localhost:5000
```

Start the dev server:

```bash
npm run dev
# React runs on http://localhost:5173
```

---

### Running the IoT Simulator

With both servers running, open a third terminal to simulate sensor data:

```bash
cd Supply_Track/backend
source venv/bin/activate

# Simulate normal → breach sequence for a specific truck
python -m app.utils.iot_simulator T-1001   # Frozen Chicken
python -m app.utils.iot_simulator T-1002   # Tomatoes
python -m app.utils.iot_simulator T-1003   # Milk
```

The simulator runs through two phases:
1. **Normal operation** — 5 pings with temperatures in the safe range
2. **Hardware failure** — 3 pings with rising temperatures that cross the breach threshold

Once the breach is detected, the backend automatically triggers a flash auction and broadcasts it to all connected shop dashboards via Socket.IO.

---

## API Reference

### Auth — `/api/auth`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/register` | Register a new shop with GPS coordinates |
| `POST` | `/login` | Login, receive JWT token |
| `GET` | `/profile` | Get current shop profile (requires token) |

### Shop — `/api/shop`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/catalogue` | Get all 15 products (seeds DB if empty) |
| `POST` | `/orders` | Place a new order from cart |
| `GET` | `/orders` | Get all orders for authenticated shop |
| `GET` | `/orders/<order_id>` | Get single order detail |
| `GET` | `/orders/<order_id>/reorder-advice` | AI reorder schedule for delivered order |

### Truck — `/api/truck`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/fleet` | Get all trucks with live location and alert level |
| `GET` | `/cargo/<truck_id>` | Get cargo batches for a specific truck |
| `POST` | `/sensor-update` | Receive IoT sensor ping (used by simulator) |

### Auction — `/api/auction`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/trigger` | Manually trigger an auction |
| `GET` | `/test-trigger` | Quick demo trigger (no auth required) |
| `GET` | `/status` | Get current active auction state |
| `GET` | `/history` | Get bid history for active auction |

### AI — `/api/ai`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat` | Send message to SupplyTrack AI chatbot |
| `POST` | `/alert-summary` | Generate plain-English spoilage alert |
| `POST` | `/reorder-advice` | Get AI reorder schedule from invoice items |

### Socket.IO Events

| Event | Direction | Description |
|---|---|---|
| `emergency_auction_started` | Server → Client | Auction triggered, opens modal on all shops |
| `price_update` | Server → Client | New bid placed, updates all clients |
| `auction_result` | Server → Client | Auction ended, announces winner |
| `submit_bid` | Client → Server | Shop places a bid |
| `auction_ended` | Client → Server | Timer expired, finalise auction |
| `new_order_assigned` | Server → Client | New order assigned to a truck |
| `ai_alert` | Server → Client | Gemini spoilage alert for a truck |

---

## Firebase Deployment

### Frontend → Firebase Hosting

```bash
npm install -g firebase-tools
firebase login
firebase init hosting   # set public dir to "dist", single-page app: yes

npm run build
firebase deploy
```

Update `VITE_BACKEND_URL` in your `.env` to point to your deployed backend URL before building.

### Database → Firestore Migration

Replace `pymongo` calls in `__init__.py` with `firebase-admin`:

```python
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
```

Then replace collection calls throughout the controllers:

```python
# MongoDB                              # Firestore
db.orders.insert_one(doc)         →   db.collection('orders').add(doc)
db.orders.find({...}, {'_id': 0}) →   db.collection('orders').where(...).stream()
db.orders.find_one({...})         →   db.collection('orders').where(...).limit(1)
```

Keep the Flask backend hosted separately (Render, Railway, or Cloud Run free tier) — Firebase Functions cannot run long-lived Socket.IO connections.

---

## Environment Variables Summary

### Backend `.env`

| Variable | Description |
|---|---|
| `MONGO_URI` | MongoDB Atlas connection string |
| `JWT_SECRET` | Secret key for signing JWT tokens |
| `FRONTEND_URL` | Allowed CORS origin (e.g. `http://localhost:5173`) |
| `GEMINI_API_KEY` | Google Gemini API key |

### Frontend `.env`

| Variable | Description |
|---|---|
| `VITE_BACKEND_URL` | Flask backend URL (e.g. `http://localhost:5000`) |

---

## How the Emergency Auction Works

```
IoT Sensor Ping
      │
      ▼
Flask /api/truck/sensor-update
      │
      ├── Temperature in safe range? → Update cargo health, continue
      │
      └── Temperature breached?
            │
            ├── Gemini generates AI alert summary
            ├── Socket emits ai_alert to truck's shop dashboard
            ├── Gemini writes auction listing description
            └── Socket emits emergency_auction_started to ALL shops
                      │
                      ▼
              AuctionModal opens on every connected shop dashboard
                      │
                      ├── Shops submit bids via socket
                      ├── price_update broadcast to all clients
                      └── Timer expires → auction_result broadcast
                                │
                                └── Gemini recommends truck reroute to winner
```

---

## Green Credits System

Shops earn credits on every order:

- **Base credits** — `₹1 credit per ₹500 spent`
- **Short shelf life bonus** — `+5 credits` if any item has ≤ 10 days shelf life
- **Bulk order bonus** — `+3 credits` if any item quantity ≥ 20 units
- **Minimum** — always at least 1 credit per order

Credits are tracked on the shop profile and displayed in the dashboard. Intended to incentivise buying near-expiry auction items over letting them waste.

---

## SDG Alignment

This project addresses **UN Sustainable Development Goal 2 (Zero Hunger)** and **SDG 12 (Responsible Consumption and Production)** by:

- Reducing food waste in the perishable goods supply chain
- Enabling small grocery shops and kirana stores to access wholesale supply chains digitally
- Turning potential food waste into discounted stock that reaches consumers
- Giving farmers and suppliers (Kisan Direct Co., Fresh Farms Pvt Ltd) better visibility into delivery conditions

---

## Team

Built for the **Google Solution Challenge** hackathon.

---

## License

MIT
