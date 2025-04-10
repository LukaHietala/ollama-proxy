import os
from dotenv import load_dotenv
import requests

class OpenWebUIClient:
    def __init__(self, base_url=None, api_key=None, model=None):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        
        if not self.base_url:
            raise ValueError("Base URL is required >:(")
        if not self.api_key:
            raise ValueError("API key is required >:(")
        if not self.model:
            raise ValueError("Model is required >:(")
            
        self.api_url = f"{self.base_url}/api"
        
        self.headers = {"Content-Type": "application/json"}
        self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        self.conversation_history = []
    
    def get_models(self):
        url = f"{self.api_url}/models"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
    
    def send_message(self, message):
        url = f"{self.api_url}/chat/completions"

        print(self.conversation_history)
        
        user_message = {"role": "user", "content": message}
        self.conversation_history.append(user_message)
        messages = self.conversation_history.copy()
        
        payload = {
            "model": self.model,
            "messages": messages
        }

        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                response_msg = response_data["choices"][0]["message"]
                self.conversation_history.append(response_msg)
                
            return response_data
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
    
    def clear_history(self):
        self.conversation_history = []
        
    def create_chat(self):
        pass
    


def main():
    load_dotenv()

    base_url = os.getenv("OPENWEBUI_BASE_URL")
    api_key = os.getenv("OPENWEBUI_API_KEY")
    model = os.getenv("OPENWEBUI_MODEL")

    client = OpenWebUIClient(base_url, api_key, model)

if __name__ == "__main__":
    main()