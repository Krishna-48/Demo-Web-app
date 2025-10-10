
import requests, time, random

API_BASE = 'http://127.0.0.1:8000'
while True:
    try:
        # Refresh sample data on backend
        requests.post(f'{API_BASE}/api/devices/refresh', timeout=5)
        print('Refreshed backend sample data')
    except Exception as e:
        print('Could not reach backend:', e)
    time.sleep(60)  # every 60 seconds (demo)
