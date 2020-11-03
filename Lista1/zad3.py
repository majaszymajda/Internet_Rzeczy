import requests
import paho.mqtt.client as mqtt

TOPIC = 'MajaAndMarta/time'


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {str(rc)}")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
    payload = {
        "students": [254313, 254292],
        "received_time": str(msg.payload)
        }
    print(payload)
    requests.post('http://127.0.0.1:2121/one_more_time', json=payload)


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("test.mosquitto.org", 1883, 60)

    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
