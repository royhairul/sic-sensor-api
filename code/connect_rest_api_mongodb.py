import machine
import dht
import time
import ssd1306
import network
import urequests
import json
from umqtt.simple import MQTTClient

# Konfigurasi WiFi
SSID = "Rumampuk"
PASSWORD = "terserah"

# Konfigurasi MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_CLIENT_ID = "ESP32"
MQTT_USER = "mqttx_421768f3"
MQTT_PASSWORD = ""
MQTT_TOPIC = "samsung/"
MQTT_TOPIC_LED = "samsung/led/"


# Konfigurasi API MongoDB
API_URL = "https://reasonably-more-haddock.ngrok-free.app/create"


# Koneksi ke WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Terhubung ke WiFi")

connect_wifi()

# Inisialisasi LED MQTT
pin_led_merah = machine.Pin(5, machine.Pin.OUT)
led_status = 0 

# Callback untuk menerima pesan MQTT
def on_message(topic, msg):
    global led_status
    message = msg.decode("utf-8")
    topic = topic.decode("utf-8")
    print("Pesan diterima: {} dari topik {}".format(message, topic))
    
    if topic == MQTT_TOPIC_LED:
        if message == "ON" and led_status == 0:
            pin_led_merah.value(1)
            led_status = 1
            print("LED dinyalakan!")
        elif message == "OFF" and led_status == 1:
            pin_led_merah.value(0)
            led_status = 0
            print("LED dimatikan!")

# Koneksi ke MQTT
def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(MQTT_TOPIC_LED)
    print("Terhubung ke MQTT Broker dan berlangganan ke topik", MQTT_TOPIC_LED)
    return client

mqtt_client = connect_mqtt()

# Inisialisasi sensor DHT11
pin_dht = machine.Pin(4)
sensor_dht = dht.DHT11(pin_dht)

# Inisialisasi sensor PIR
pin_pir = machine.Pin(16, machine.Pin.IN)

# Inisialisasi LED
pin_led = machine.Pin(17, machine.Pin.OUT)

# Inisialisasi OLED
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def send_data_to_api(suhu, kelembaban, gerakan):
    payload = json.dumps({
        "temperature": suhu,
        "humidity": kelembaban,
        "motion": gerakan
    })
    try:
        headers = {"Content-Type": "application/json"}
        response = urequests.post(API_URL, data=payload, headers=headers)
        
        print("Response Code:", response.status_code)
        print("Response:", response.text)
        
        response.close()
    except Exception as e:
        print("Gagal mengirim data ke API:", e)

while True:
    try:
        # Membaca sensor DHT11
        sensor_dht.measure()
        suhu = sensor_dht.temperature()
        kelembaban = sensor_dht.humidity()
        gerakan = 1 if pin_pir.value() else 0
        
        print("Suhu: {}°C".format(suhu))
        print("Kelembaban: {}%".format(kelembaban))
        
        # Menampilkan data di OLED
        oled.fill(0)
        oled.text("Suhu: {}C".format(suhu), 0, 0)
        oled.text("Kelembaban: {}%".format(kelembaban), 0, 10)
        
        # Mengirim data ke MQTT
        mqtt_client.publish(MQTT_TOPIC, str(suhu))
        mqtt_client.publish(MQTT_TOPIC, str(kelembaban))
        
        # Membaca sensor PIR dan mengontrol LED
        if pin_pir.value():
            print("Gerakan terdeteksi!")
            pin_led.value(1)
            oled.text("Gerakan: IYA", 0, 20)
            mqtt_client.publish(MQTT_TOPIC, "Terdeteksi")
        else:
            print("Tidak ada gerakan")
            pin_led.value(0)
            oled.text("Gerakan: TIDAK", 0, 20)
            mqtt_client.publish(MQTT_TOPIC, "Tidak Terdeteksi")
        
        oled.show()
        
        # Kirim data ke API MongoDB
        send_data_to_api(suhu, kelembaban, gerakan)
        
    except Exception as e:
        print("Gagal membaca sensor DHT11:", e)
        
    # Mengecek pesan MQTT setiap loop
    mqtt_client.check_msg()
    time.sleep(3)
