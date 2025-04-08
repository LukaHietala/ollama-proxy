import requests


url = 'http://127.0.0.1:4321'
while True:
    try:
        usr_input = input("Kysymys: ")

        content_obj = {}

        content_obj["content"] = usr_input

        x = requests.post(url + "/api", json = content_obj)
        res = x.json()

        file = open("asdf.txt", "a")
        file.write(res["message"]["content"] + "\n")
        file.close()

        print(res["message"]["content"])
    except KeyboardInterrupt:
        print("Exiting...")
        requests.post(url + "/delete", json = {})
        file.close()
        break
    except Exception as e:
        print(f"An error occurred: {e}")