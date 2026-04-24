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
