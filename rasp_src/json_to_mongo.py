import os
import json
from pymongo import MongoClient
from datetime import datetime

# --- Configuration MongoDB ---
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_sensors"]
collection = db["sensor_data"]

# --- Dossier contenant les fichiers JSON ---
json_folder = "received_json"

# --- Parcourir tous les fichiers JSON ---
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(json_folder, filename)
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            # Vérifie si déjà inséré (évite doublons si tu relances le script)
            if collection.count_documents({"timestamp": data.get("timestamp", "")}, limit=1) == 0:
                collection.insert_one(data)
                print(f"✅ Inséré : {filename}")
            else:
                print(f"⚠ Déjà présent : {filename}")

        except Exception as e:
            print(f"❌ Erreur avec {filename}: {e}")

# --- Nettoyage ---
mongo_client.close()
print("🏁 Terminé.")
