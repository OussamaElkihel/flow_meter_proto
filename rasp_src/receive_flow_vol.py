import time
import json
import os
from datetime import datetime
import pigpio
import struct
from nrf24 import NRF24, RF24_DATA_RATE

# --- Configuration ---
CE_PIN = 22
ADDRESS = b'\x66\x55\x55\x55\x66'

# --- Init pigpio ---
pi = pigpio.pi()
if not pi.connected:
    print("-- pigpio not connected")
    exit(1)

# --- Init NRF24 ---
radio = NRF24(
    pi,
    ce=CE_PIN,
    payload_size=8,  # we send two floats = 8 bytes
    channel=76,
    data_rate=RF24_DATA_RATE.RATE_250KBPS
)
radio.set_address_bytes(len(ADDRESS))
radio.open_reading_pipe(1, ADDRESS)

# Enable receiving mode
pi.set_mode(CE_PIN, pigpio.OUTPUT)
pi.write(CE_PIN, 1)

radio.show_registers()

# --- Create output folder ---
os.makedirs("received_json", exist_ok=True)

# --- Convert 4 bytes -> float (little-endian IEEE 754) ---
def bytes_to_float(byte_array):
    return struct.unpack('<f', byte_array)[0]

# --- Save parsed data to JSON ---
def save_json(node_id, water_flow, water_volume):
    data = {
        "node_id": node_id,
        "timestamp": datetime.now().isoformat(),
        "water_flow": water_flow,
        "water_volume": water_volume
    }
    filename = f"received_json/data_{int(time.time())}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"-- JSON saved: {filename}")

# --- Main loop ---
try:
    print("-- Listening for NRF24 float packets...")
    node_id = "water_node_1"  # Set a static node_id or adapt as needed
    water_flow = None
    water_volume = None

    while True:
        if radio.data_ready():
            packet = radio.get_payload()
            print("-- Raw packet:", " ".join(f"{b:02X}" for b in packet))

            if len(packet) == 8:
                try:
                    water_flow = bytes_to_float(packet[:4])
                    water_volume = bytes_to_float(packet[4:])
                    print(f"-- Received water_flow: {water_flow:.4f}, water_volume: {water_volume:.4f}")
                    save_json(node_id, water_flow, water_volume)
                except Exception as e:
                    print(f"-- Error decoding floats: {e}")
            else:
                print(f"-- Invalid packet size: expected 8 bytes, got {len(packet)}")

        # time.sleep(0.01)

except KeyboardInterrupt:
    print("-- Interrupted by user")

finally:
    pi.write(CE_PIN, 0)
    pi.stop()
    print("-- Cleanup done. Goodbye!")
