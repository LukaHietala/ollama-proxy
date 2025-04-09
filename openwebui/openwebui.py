import os
from dotenv import load_dotenv

class OpenWebUIClient:
    def __init__(self, base_url=None, api_key=None, model=None):
        load_dotenv()
        
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

    def send_message(self, message):
        pass


def main():
    base_url = os.getenv("OPENWEBUI_BASE_URL")
    api_key = os.getenv("OPENWEBUI_API_KEY")
    model = os.getenv("OPENWEBUI_MODEL")

    client = OpenWebUIClient(base_url, api_key, model)
