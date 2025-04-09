import requests

# Ollama proxy address 🦙
url = 'http://127.0.0.1:4321'

# 91m = red
# 92m = green
# 93m = yellow

def clear_history():
    try:
        requests.post(url + "/delete", json = {})
        print("\033[93mConversation history cleared\033[0m")
    except Exception as e:
        print(f"\033[91mFailed to clear history: {e}\033[0m") 

while True:
    try:
        usr_input = input("\033[94mQuestion: \033[0m") 
        
        if usr_input.lower() in ['/exit', '/quit']:
            print("\033[91mExiting...\033[0m") 
            break
        elif usr_input.lower() in ['/clear', '/reset']:
            clear_history()
            continue

        content_obj = {"content": usr_input}

        x = requests.post(url + "/api", json = content_obj, timeout=60)
        res = x.json()

        print("\033[92m" + res["message"]["content"] + "\033[0m")
    except KeyboardInterrupt:
        print("\033[91mExiting...\033[0m") 
        break
    except requests.exceptions.Timeout:
        print("\033[91mLaama taitaa nukkua\033[0m")
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")

try:
    if input("\033[93mClear conversation history? (y/n): \033[0m").lower() == 'y':
        clear_history()
except:
    pass