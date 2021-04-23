import json
import os
from dotenv import load_dotenv
from iotbs.messenger.device import Device


class Messenger:

    def __init__(self, theBot, theMQTT):
        load_dotenv()
        self.url = os.getenv("MQTT_URL")
        self.port = int(os.getenv("MQTT_PORT"))
        self.bot = theBot.getClient()
        self.mqtt = theMQTT.getClient()
        self.debug_chan = os.getenv("DEBUG_CHAN_ID")
        self.tosend = {}
        self.devs = []

    def text_sender(self, chan, txt):

        response = self.bot.chat_postMessage(channel=chan, text=txt)
        assert response["ok"]

    def publish_message_default_disconnect(self, payload=None, retain=False, topic="signs/", qos=1):
        self.mqtt.connect(
            host=self.url,
            port=self.port,
            keepalive=5)
        self.mqtt.publish(
            topic=topic,
            payload=payload,
            qos=qos,
            retain=retain,)
        self.mqtt.disconnect()

    def _load_devices(self):

        f = open('iotbs/messenger/devices.json')
        devices = json.load(f)
        for key, val in devices.items():
            self.devs.append(Device(key, val['id'], val['location'], val['type'], val['height'], val['width']))
        f.close()

    def publish_to_set(self, flags: dict):
        self.devs = []
        self._load_devices()
        self._make_set(flags)

        for dev in self.tosend:
            topics = f"signs/{dev.get_ZIP()}/{dev.get_Type()}/{dev.get_ID()}"
            self.text_sender(chan=self.debug_chan, txt=f"Sending to: {topics}")
            self.publish_message_default_disconnect(payload=flags['message'], retain=False, topic=topics, qos=1)

    def _print_list_to_chat(self):
        self.text_sender(
            chan=self.debug_chan,
            txt="====Current List===="
        )
        for dev in self.devs:
            name = dev.get_Name()
            id = dev.get_ID()
            msgtype = dev.get_Type()
            zip = dev.get_ZIP()
            self.text_sender(
                chan=self.debug_chan,
                txt=(
                    f"Name: {name}\n" +
                    f"ID: {id}\n" +
                    f"Type: {msgtype}\n" +
                    f"ZIP: {zip}"
                )
            )

    def _print_set_to_chat(self):
        self.text_sender(
            chan=self.debug_chan,
            txt="====Current Set===="
        )
        for dev in self.tosend:
            name = dev.get_Name()
            id = dev.get_ID()
            msgtype = dev.get_Type()
            zip = dev.get_ZIP()
            self.text_sender(
                chan=self.debug_chan,
                txt=(
                    f"Name: {name}\n" +
                    f"ID: {id}\n" +
                    f"Type: {msgtype}\n" +
                    f"ZIP: {zip}"
                )
            )

    def _make_set(self, flags: dict):
        self.tosend = set()
        if (
            flags['device'] == "ALL"
            and flags['zipcode'] != "ALL"
            and flags['msgtype'] != "ALL"
        ):
            self.text_sender(chan='C01TTAF8CP9', txt="Zip: Specific...  Dev: ALL...  Type: Specific...")
            self._add_only_zip_type(flags['zipcode'], flags['msgtype'])
        elif (
            flags['zipcode'] == "ALL"
            and flags['device'] == "ALL"
            and flags['msgtype'] != "ALL"
        ):
            self.text_sender(chan='C01TTAF8CP9', txt="Zip: ALL...  Dev: ALL...  Type: Specific...")
            self._add_all_in_type(flags['msgtype'])
        elif (
            flags['device'] == "ALL"
            and flags['msgtype'] == "ALL"
            and flags['zipcode'] != "ALL"
        ):
            self.text_sender(chan='C01TTAF8CP9', txt="Zip: Specific...  Dev: ALL...  Type: ALL...")
            self._add_all_in_zip(flags['zipcode'])
        elif (
            flags['msgtype'] == "ALL"
            and flags['zipcode'] == "ALL"
            and flags['device'] == "ALL"
        ):
            self.text_sender(chan='C01TTAF8CP9', txt="All Devices")
            self._add_all_ids()
        else:
            self.text_sender(chan='C01TTAF8CP9', txt="Single Device")
            self._add_one_dev(flags)

# Specific Device
    def _add_one_dev(self, flags: dict):
        for dev in self.devs:
            if (
                dev.get_ID() == flags['device']
            ):
                self.tosend.add(dev)

# ALL devices in a ZIP AND type
    def _add_only_zip_type(self, zip: str, msg: str):
        for dev in self.devs:
            if dev.get_ZIP() == zip and dev.get_Type() == msg:
                self.tosend.add(dev)

# ALL devices in a ZIP
    def _add_all_in_zip(self, zip: str):
        for dev in self.devs:
            if dev.get_ZIP() == zip:
                self.tosend.add(dev)

# ALL devices of a type
    def _add_all_in_type(self, msg: str):
        for dev in self.devs:
            if dev.get_Type() == msg:
                self.tosend.add(dev)

# ALL devices
    def _add_all_ids(self):
        for dev in self.devs:
            self.tosend.add(dev)
