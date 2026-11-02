import json
import paho.mqtt.client as mqtt
import requests

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz42t-I6nLxOJtG0Tj1SKZuCGi7vFW1fQaBfx05nMz4NCGzE6tX0Tx4242I4U-qGgx0/exec"

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "school/register"


def on_message(client, userdata, msg):
  try:
    payload = msg.payload.decode("utf-8")
    print(f"\n📩 ได้รับข้อมูลใหม่ผ่าน MQTT: {payload}")

    data = json.loads(payload)

    payload_to_sheets = {
        "fullname": data.get("fullname"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "age": data.get("age"),
        "job_status": data.get("job_status"),
        "education": data.get("education"),
        "course": data.get("course"),
        "address": data.get("address"),
    }

    if payload_to_sheets["fullname"] and payload_to_sheets["email"]:
      response = requests.post(GOOGLE_SCRIPT_URL, json=payload_to_sheets)
      print(f"☁️ บันทึกลง Google Sheets สำเร็จ! Response: {response.text}")
    else:
      print("⚠️ ข้อมูลไม่ครบถ้วน ไม่สามารถบันทึกได้")

  except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")


def on_connect(client, userdata, flags, rc, properties=None):
  if rc == 0:
    print("✅ เชื่อมต่อ MQTT Broker สำเร็จ!")
    client.subscribe(MQTT_TOPIC)
    print(f"🎧 กำลังรอฟังข้อมูลจาก Topic: '{MQTT_TOPIC}'...")
  else:
    print(f"❌ เชื่อมต่อ MQTT Broker ไม่สำเร็จ Code: {rc}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to MQTT Broker: {MQTT_BROKER}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()
