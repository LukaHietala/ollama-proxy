import requests

# Flask serverin osoite
BASE_URL = "http://localhost:3000/api"

def test_health():
    print("Testataan yhteys tekoälypalvelimeen")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Vastaus: {response.json()}")
    return response.status_code == 200

def test_models():
    print("Testataan mallien haku")
    response = requests.get(f"{BASE_URL}/models")
    print(f"Status: {response.status_code}")
    print(f"Vastaus: {response.json()}")
    return response.status_code == 200

def test_chat(message="Mitä kuuluu?"):
    print(f"Testataan viestintä: '{message}'")
    response = requests.post(f"{BASE_URL}/chat", json={"message": message})
    print(f"Status: {response.status_code}")

    if response.status_code == 200 and "data" in response.json():
        print(f"Vastaus: {response.json()['data']['message']['content'][:100]}...")
        print(f"Koko Vastaus: {response.json()}")
    else:
        print(f"Virhe: {response.json()}")
    return response.status_code == 200

def test_clear():
    print("Testataan historian tyhjennys")
    response = requests.post(f"{BASE_URL}/chat/clear")
    print(f"Status: {response.status_code}")
    print(f"Vastaus: {response.json()}")
    return response.status_code == 200

def suorita_testit():
    tulokset = {
        "Yhteys": test_health(),
        "Mallit": test_models(),
        "Viesti": test_chat(),
        "Jatkokysymys": test_chat("Kuka sinä olet?"),
        "Tyhjennys": test_clear()
    }
    
    print("\nTulokset:")
    for testi, tulos in tulokset.items():
        status = "OK" if tulos else "VIRHE"
        print(f"{testi}: {status}")

if __name__ == "__main__":
    suorita_testit()