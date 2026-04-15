import time
import requests
import random
import sys

WEBHOOK_URL = "http://127.0.0.1:5000/api/truck/sensor-update"

TRUCKS = {
    "T-1001": {
        "truck_id":   "T-1001",
        "batch_id":   "FRZ-C1",
        "batch_name": "Frozen Chicken Breasts",
        "safe_range": (-20, -15),
        "truck_lat":  23.374,
        "truck_lng":  87.101,
    },
    "T-1002": {
        "truck_id":   "T-1002",
        "batch_id":   "VEG-T1",
        "batch_name": "Tomatoes Grade A (10kg crates)",
        "safe_range": (8, 14),
        "truck_lat":  23.523,
        "truck_lng":  87.198,
    },
    "T-1003": {
        "truck_id":   "T-1003",
        "batch_id":   "DRY-M1",
        "batch_name": "Full Cream Milk (1L pouches)",
        "safe_range": (2, 5),
        "truck_lat":  23.661,
        "truck_lng":  87.421,
    },
}


def simulate(truck_id="T-1001"):
    truck = TRUCKS.get(truck_id)
    if not truck:
        print(f"Unknown truck: {truck_id}. Choose from: {list(TRUCKS.keys())}")
        return

    lo, hi = truck["safe_range"]
    print(f"\n🚛 IoT stream for {truck_id} | Batch: {truck['batch_name']}")
    print("─" * 55)

    batch_data = {
        "truck_id":  truck["truck_id"],
        "batch_id":  truck["batch_id"],
        "batch_name": truck["batch_name"],
        "truck_lat": truck["truck_lat"],
        "truck_lng": truck["truck_lng"],
        "temp":      lo,
    }

    try:
        print("\n📡 Phase 1: Normal operation...\n")
        for i in range(5):
            batch_data["temp"] = round(random.uniform(lo, hi), 1)
            print(f"  [✅ NORMAL] Ping {i+1}/5 — Temp: {batch_data['temp']}°C")
            requests.post(WEBHOOK_URL, json=batch_data)
            time.sleep(2)

        print(f"\n⚡ Phase 2: Simulating hardware failure...\n")
        time.sleep(1)

        # THE FIX: Force the temperatures to cross 0°C so Flask catches it!
        spike_temps = [-5.2, 2.1, 15.4]

        for spike in spike_temps:
            batch_data["temp"] = spike
            label = "🚨 CRITICAL" if spike > 0 else "⚠️  WARNING"
            print(f"  [{label}] Temp: {spike}°C — sending alert...")
            requests.post(WEBHOOK_URL, json=batch_data)
            time.sleep(2)

        print("\n✅ Simulation complete — auction should have triggered!\n")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask. Make sure the backend is running.")


if __name__ == "__main__":
    truck_id = sys.argv[1] if len(sys.argv) > 1 else "T-1001"
    simulate(truck_id)
