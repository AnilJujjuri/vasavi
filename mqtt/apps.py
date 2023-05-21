from fastapi import FastAPI
import paho.mqtt.client as mqtt
import random

apps = FastAPI()

brokerAddress = "broker.hivemq.com"
userName = "vasavi"
passWord = "Chinnu@123"
topic = "Sensor/Temperature/TMP36"

min_temp = 10
max_temp = 25

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic)
    else:
        print("Connect returned result code: " + str(rc))

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8884)

# Start the MQTT client loop in a background thread
client.loop_start()

@apps.get("/")
def read_root():
    return {"Hello": "MQTT FastAPI"}


@apps.post("/publish")
def publish_temperature():
    while True:
        data = random.randint(min_temp, max_temp)
        client.publish(topic, data)
        return f"Published temperature data: {data}"

@apps.get("/subscribe")
def subscribe_topic():
    client.subscribe(topic)
    return f"Subscribed to topic: {topic}"



# FastAPI will handle the MQTT messages in the background
# The on_message callback will be executed for each received message

