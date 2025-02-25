import network
import time
import dht
import machine
from umqtt.simple import MQTTClient
import json

# WiF
SSID = ""  
PASSWORD = "" 

# MQTT
MQTT_BROKER_EMQX = "broker.emqx.io"
MQTT_PORT_EMQX = 1883
MQTT_TOPIC_SUHU = "samsung_batch/data/dht11/suhu"
MQTT_TOPIC_KELEMBABAN = "samsung_batch/data/dht11/kelembaban"
MQTT_TOPIC_PIR = "samsung_batch/data/pir"

# Ubidots
UBIDOTS_BROKER = "industrial.api.ubidots.com"
UBIDOTS_TOKEN = "BBUS-d6THSvnu8BvabNE8vvEcG74t5dBe24"  # Ganti dengan Ubidots Token Anda
UBIDOTS_DEVICE = "Stage2"
UBIDOTS_TOPIC = f"/v1.6/devices/{UBIDOTS_DEVICE}"
UBIDOTS_TOPIC_LED = f"/v1.6/devices/{UBIDOTS_DEVICE}/led/lv"

dht_sensor = dht.DHT11(machine.Pin(4))
pir_sensor = machine.Pin(16, machine.Pin.IN)
led = machine.Pin(17, machine.Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Menghubungkan ke WiFi...", end="")
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(0.5)
        timeout -= 1
    if wlan.isconnected():
        print("\nWiFi Terhubung!")
        print("Alamat IP:", wlan.ifconfig()[0])
        return True
    print("\nGagal terhubung ke WiFi.")
    return False

def ubidots_callback(topic, msg):
    print(f"Pesan diterima dari {topic}: {msg}")
    try:
        if msg == b'1.0': 
            led.value(1)
            print("LED ON")
        elif msg == b'0.0': 
            led.value(0)
            print("LED OFF")
    except Exception as e:
        print("Error dalam callback MQTT:", e)

def connect_mqtt(broker, client_id, username=None, password=None, subscribe_topic=None, callback=None):
    client = MQTTClient(client_id, broker, user=username, password=password)
    try:
        client.connect()
        print(f"Terhubung ke MQTT Broker: {broker}")
        if subscribe_topic and callback:
            client.set_callback(callback)
            client.subscribe(subscribe_topic)
            print(f"Berlangganan ke topic: {subscribe_topic}")
        return client
    except Exception as e:
        print(f"Gagal terhubung ke MQTT {broker}: {e}")
        return None

def main():
    if not connect_wifi():
        return

    mqtt_client_emqx = connect_mqtt(MQTT_BROKER_EMQX, "esp32_client_emqx")
    mqtt_client_ubidots = connect_mqtt(UBIDOTS_BROKER, "esp32_client_ubidots", UBIDOTS_TOKEN, "", UBIDOTS_TOPIC_LED, ubidots_callback)
    
    if not mqtt_client_emqx or not mqtt_client_ubidots:
        return

    while True:
        try:
            dht_sensor.measure()
            suhu = dht_sensor.temperature()
            kelembaban = dht_sensor.humidity()
            motion_detected = pir_sensor.value()

            payload_suhu = json.dumps({"suhu": suhu})
            payload_kelembaban = json.dumps({"kelembaban": kelembaban})
            payload_pir = json.dumps({"gerakan": motion_detected})
            payload_ubidots = json.dumps({"suhu": {"value": suhu}, "kelembaban": {"value": kelembaban}, "gerakan": {"value": motion_detected}})

            mqtt_client_emqx.publish(MQTT_TOPIC_SUHU, payload_suhu)
            mqtt_client_emqx.publish(MQTT_TOPIC_KELEMBABAN, payload_kelembaban)
            mqtt_client_emqx.publish(MQTT_TOPIC_PIR, payload_pir)
            print(f"Data dikirim ke EMQX")

            mqtt_client_ubidots.publish(UBIDOTS_TOPIC, payload_ubidots)
            print(f"Data dikirim ke Ubidots: {payload_ubidots}")

            mqtt_client_ubidots.check_msg()
        except Exception as e:
            print("Gagal mengirim data:", e)
            mqtt_client_ubidots = connect_mqtt(UBIDOTS_BROKER, "esp32_client_ubidots", UBIDOTS_TOKEN, "", UBIDOTS_TOPIC_LED, ubidots_callback)
        
        time.sleep(5)

main()

