from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Caricamento delle configurazioni da un file JSON
CONFIG_FILE = "config_data.json"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

CONFIGS = load_config()

# Endpoint per ottenere la configurazione di un servizio
@app.route("/config/<service_name>", methods=["GET"])
def get_config(service_name):
    api_key = request.headers.get("X-API-KEY")
    
    # Controllo API Key per sicurezza (opzionale)
    if api_key != os.getenv("CONFIG_SERVER_API_KEY", "default_key"):
        return jsonify({"error": "Unauthorized"}), 403

    config = CONFIGS.get(service_name)
    if config:
        return jsonify(config)
    return jsonify({"error": "Service not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
