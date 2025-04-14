import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify
from functools import wraps

# Nao sanoo "message" kohdan jos se on täytetty, tietyissä tapauksissa Nao voi sanoa datan
def success_response(data=None, message=None):
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return response

# Nao kertoo että virhe on tullut, mutta ei kerro sitä vaan printtaa konsoliin sen
def error_response(error_message):
    return {
        "success": False,
        "error": error_message
    }

# Kaikki api funktiot jotka voivat heittää virheitä käsitellään tässä
# https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
def handle_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify(error_response(str(e))), 500
    return decorated

# Kommunikaatio OpenWebUI:n kanssa
class OpenWebUIClient:
    def __init__(self, base_url=None, api_key=None, model=None):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        
        if not self.base_url:
            raise ValueError("Base URL is required")
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.model:
            raise ValueError("Model is required")
            
        self.api_url = f"{self.base_url}/api"
        
        self.headers = {"Content-Type": "application/json"}
        self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Pitää keskusteluhistorian ohjelman muistissa väliaikaisesti
        self.conversation_history = []
    
    def get_models(self):
        url = f"{self.api_url}/models"
        response = requests.get(url, headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
    
    def send_message(self, message):
        if not message or not isinstance(message, str):
            raise ValueError("Message cannot be empty and must be a string")
            
        url = f"{self.api_url}/chat/completions"
        
        user_message = {"role": "user", "content": message}
        self.conversation_history.append(user_message)
        messages = self.conversation_history.copy()
        
        payload = {
            "model": self.model,
            "messages": messages
        }

        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        
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


# Custom API endpointit
def create_app(client):
    app = Flask(__name__)
    
    # Ehkä hauska lisäys Naolle, mutta ei pakollinen
    @app.route('/api/models', methods=['GET'])
    @handle_errors
    def get_models():
        models = client.get_models()
        # models palauttaa myös "data" keyn, joten napataaan se pois
        if isinstance(models, dict) and "data" in models:
            return jsonify(success_response(data=models["data"]))
        # Jos dataa ei ole, niin palautetaan koko response
        return jsonify(success_response(data=models))
    
    # Lähetää viestin tekoälylle (historian kanssa)
    @app.route('/api/chat', methods=['POST'])
    @handle_errors
    def chat():
        data = request.json
        if not data or 'message' not in data:
            return jsonify(error_response("Message is required")), 400
        
        response_data = client.send_message(data['message'])
        
        if "usage" in response_data and response_data["usage"]["total_tokens"] > 1500: # konteksti ikkunan koko on 2048, mutta 1500 on turvallinen raja
            client.clear_history()
            return jsonify(success_response(
                # Nao kertoo tämän, niinkuin olisi suoraan tekoälyltä tullut
                data={"message": {"role": "assistant", "content": "Muistini loppui kesken, joten joudun tyhjentämään sen"}}
            ))
        
        if not response_data or "choices" not in response_data or not response_data["choices"]:
            return jsonify(error_response("Invalid response from openwebui API")), 500
        
        print(response_data)
        
        return jsonify(success_response(data={"message": response_data["choices"][0]["message"]}))
    
    # Tyhjentää keskusteluhistorian, onStopped eventissä tai käskyllä(?)
    @app.route('/api/chat/clear', methods=['POST'])
    @handle_errors
    def clear_chat(): 
        client.clear_history()
        return jsonify(success_response(message="Muistin tyhjennys onnistui"))
    
    # Tarkistaa onko tekoäly käytettävissä
    # Jos tekoäly ei vastaa, niin Nao sanoo että tekoäly ei ole käytettävissä
    @app.route('/api/health', methods=['GET'])
    @handle_errors
    def check_health():
        # Oma error handler koska tämä käyttää ulkoista API:a (openwebui)
        try:
            response = requests.get(client.api_url, headers=client.headers, timeout=5)
            if response.status_code == 200:
                return jsonify(success_response(data={"status": "healthy"}))
            else:
                return jsonify(error_response("Service unavailable")), 503
        except requests.RequestException:
            return jsonify(error_response("Connection error")), 503
    
    # Standardit virheet
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error_response("Resource not found")), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(error_response("Method not allowed")), 405
    
    @app.errorhandler(418)
    def teapot_error(error):
        return jsonify(error_response("I'm a teapot")), 418 # rfc2324 :)
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify(error_response("Internal server error")), 500
    
    return app

def main():
    load_dotenv()

    base_url = os.getenv("OPENWEBUI_BASE_URL")
    api_key = os.getenv("OPENWEBUI_API_KEY")
    model = os.getenv("OPENWEBUI_MODEL")
    port = int(os.getenv("PORT", 5000))

    client = OpenWebUIClient(base_url, api_key, model)
    
    app = create_app(client)
    app.run(host="0.0.0.0", port=port, debug=False) # Toimii vain saman verkon sisällä

if __name__ == "__main__":
    main()