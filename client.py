import requests

# Ollama proxy
url = 'http://127.0.0.1:4321'

while True:
    try:
        usr_input = input("Question: ")

        content_obj = {}
        content_obj["content"] = usr_input

        x = requests.post(url + "/api", json = content_obj)
        res = x.json()

        print(res["message"]["content"])
    except KeyboardInterrupt:
        print("Exiting...")
        requests.post(url + "/delete", json = {})
        break
    except Exception as e:
        print(f"An error occurred: {e}")