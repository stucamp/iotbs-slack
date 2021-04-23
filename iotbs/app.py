from iotbs.common.iotbs import IoTbs
from iotbs.common.routing import Router
from iotbs.mqtt.mqtt_handler import MQTT_Handler
from flask import Flask


# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Initialize a Web API client, Router and Slack Events adapter
theBot = IoTbs(app)
theMQTT = MQTT_Handler()
theMQTT.setup_client()
slack_events_adapter = theBot.getAdapter()
router = Router(theBot, theMQTT)


# ============== Message Events ============= #


@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """

    router.handle_message(payload)


# ============== App Mention Events ============= #


@slack_events_adapter.on("app_mention")
def mention(payload):
    """
    Triggers handler for when the bot received an @ mention event..
    """

    router.handle_app_mention(payload)


if __name__ == "__main__":

    app.run(port=5000)
