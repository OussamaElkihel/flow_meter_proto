import time
import json
from pymongo import MongoClient
import paho.mqtt.client as mqtt

# --- Config ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "iot_sensors"
COLLECTION_NAME = "sensor_data"

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_BASE = "farmconnect/data"

# --- Connexion MongoDB ---
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# --- Connexion MQTT ---
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# --- Récupération des 10 derniers documents ---
documents = list(collection.find().sort("timestamp", -1).limit(10))
documents.reverse()  # pour les publier dans l'ordre chronologique

try:
    for doc in documents:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])  # pour éviter problème de sérialisation

        node_id = doc.get("node_id", "unknown")
        topic = f"{MQTT_TOPIC_BASE}/{node_id}"

        values = doc.get("values", [])

        payload = {
            "node_id": node_id,
            "timestamp": doc.get("timestamp")
        }

        if len(values) > 0:
            payload["temperature"] = values[0]
        if len(values) > 1:
            payload["humidity"] = values[1]
        if len(values) > 2:
            payload["soil_moisture"] = values[2]
        if len(values) > 3:
            payload["battery_level"] = values[3]

        json_data = json.dumps(payload)
        mqtt_client.publish(topic, json_data)

        print(f"📡 Reçu données complètes du noeud {node_id}: {payload}")
        time.sleep(5)  # ⏱ délai simulant temps réel

except KeyboardInterrupt:
    print("🛑 Interruption manuelle")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    client.close()
    print("👋 Cleanup terminé.")
