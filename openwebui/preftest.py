"""
Tulokset:

(hei nao)

Jessen palvelin: avg=2.89s, min=2.36s, max=3.11s
Kpedun palvelin: avg=0.90s, min=0.81s, max=1.02s
Kpedun palvelin on 1.99s nopeampi

(Hei nao, kerro kuka on suomen presidentti, yhdysvaltojen presidentti ja kuka on salattujen elämien Ismo. Kerro kaikki niin lyhysesti kuin voit.)

Jessen palvelin: avg=5.78s, min=5.68s, max=5.99s
Kpedun palvelin: avg=2.02s, min=1.94s, max=2.15s
Kpedun palvelin on 3.76s nopeampi
"""

import requests
import time
import statistics

MESSAGE = ""
MODEL = ""
TIMES = 5

# Malli 1
MALLI1_URL = ""
MALLI1_API_KEY = ""
MALLI1_NAME = "Jesse"

# Malli 2
MALLI2_URL = ""
MALLI2_API_KEY = ""
MALLI2_NAME = ""

def test1():
    url = MALLI1_URL
    api_key = MALLI1_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    times = []
    for i in range(TIMES):
        start = time.time()
        response = requests.post(
            f"{url}/api/chat/completions",
            headers=headers,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": MESSAGE,
                    }
                ]
            }
        )
        end = time.time()
        times.append(end - start)
        
    return {
        "server": MALLI1_NAME,
        "avg": statistics.mean(times),
        "min": min(times),
        "max": max(times)
    }

def test2():
    url = MALLI2_URL
    api_key = MALLI2_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    times = []
    
    for i in range(TIMES):
        start = time.time()
        response = requests.post(
            f"{url}/api/chat/completions",
            headers=headers,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": MESSAGE,
                    }
                ]
            }
        )
        end = time.time()
        times.append(end - start)
        
        requests.post(f"{url}/chat/clear")
        
    return {
        "server": MALLI2_NAME,
        "avg": statistics.mean(times),
        "min": min(times),
        "max": max(times)
    }

def main():
    print(f"Viesti: {MESSAGE}")
    print(f"Malli: {MODEL}")
    print(f"Toistot: {TIMES}")
    print(f"Jessen palvelin: {MALLI1_URL}")
    print(f"Kpedun palvelin: {MALLI2_URL}")

    test1_results = test1()
    test2_results = test2()
    
    print(f"\nJessen palvelin: avg={test1_results['avg']:.2f}s, min={test1_results['min']:.2f}s, max={test1_results['max']:.2f}s")
    print(f"Kpedun palvelin: avg={test2_results['avg']:.2f}s, min={test2_results['min']:.2f}s, max={test2_results['max']:.2f}s")
    
    if test1_results['avg'] < test2_results['avg']:
        print(f"Jessen palvelin on {test2_results['avg'] - test1_results['avg']:.2f}s nopeampi")
    else:
        print(f"Kpedun palvelin on {test1_results['avg'] - test2_results['avg']:.2f}s nopeampi")

if __name__ == "__main__":
    main()