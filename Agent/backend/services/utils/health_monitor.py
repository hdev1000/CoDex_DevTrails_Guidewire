import requests
import time

def monitor_loop():
    while True:
        try:
            response = requests.get("http://localhost:8080/health").json()
            status = response["status"]
            print(f"[HEALTH] {time.ctime()} — Status: {status}")
        except Exception as e:
            print(f"[HEALTH ERROR] {e}")

        time.sleep(30)