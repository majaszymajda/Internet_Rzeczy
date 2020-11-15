import time
import requests
import paho.mqtt.client as mqtt

TOPIC = 'MajaAndMarta/time'


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.connect("test.mosquitto.org", 1883, 60)

    while True:
        r = requests.get('http://127.0.0.1:2323/time?tz=+2')
        print(r.text)
        mqtt_client.publish(TOPIC, payload=r.text)
        time.sleep(5)


if __name__ == "__main__":
    main()