import os
import paho.mqtt.client as paho
import ssl
from dotenv import load_dotenv


class MQTT_Handler:

    def __init__(self):
        load_dotenv()
        self.user = os.getenv("MQTT_USER")
        self.pswd = os.getenv("MQTT_PSWD")
        self.client = paho.Client()

    def setup_client(self):
        self.client.username_pw_set(self.user, password=self.pswd)
        self.client.tls_set(certfile='iotbs/mqtt/certs/client/client.crt',
                            keyfile='iotbs/mqtt/certs/client/client.key',
                            cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log

    def on_message(self, client, userdata, message):
        print("received message =", str(message.payload.decode("utf-8")))

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def on_connect(self, client, userdata, flags, rc):
        print("Connecting ")
        client.publish("connection/bridge", payload="Connected", qos=1, retain=False)

    def on_disconnect(self, client, userdata, flags):
        print("Disconnecting ")
        client.publish("connection/bridge", payload="Disconnected", qos=1, retain=False)

    def getClient(self) -> paho.Client:

        return self.client
