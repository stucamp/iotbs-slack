import iotbs.modules_admin.debug as debug
import iotbs.common.events as events
import os
from iotbs.parser.parser import Parser
from iotbs.messenger.messenger import Messenger


class Router:

    def __init__(self, theBot, theMQTT):
        self.bot = theBot.getClient()
        self.parser = Parser()
        self.messenger = Messenger(theBot, theMQTT)

        # Import various ID's for filtering via dotenv
        self.bot_id = os.getenv("BOT_ID")
        self.bot_app_id = os.getenv("APP_ID")
        self.home_channel = os.getenv("HOME_CHAN_ID")
        self.debug_chan = os.getenv("DEBUG_CHAN_ID")
        self.stu_user = os.getenv("STU_ID")

    def handle_message(self, payload):

        event = events.MessageEvent(payload)

        if (
            event.channel_id != self.debug_chan
            and event.channel_id != self.home_channel
            and event.subtype != "message_delete"
        ):

            self.messenger.text_sender(chan=self.debug_chan, txt=debug.message(event))

    def handle_app_mention(self, payload):

        event = events.AppMentionEvent(payload)

        if (event.channel_id != self.debug_chan):

            stuff = self.parser.parse_slack(event.text)

            if self.parser.isComplete(stuff):
                reply = (
                    "Topics Received...\n"
                    f"ID = {stuff['device']}\n" +
                    f"TYPE = {stuff['msgtype']}\n" +
                    f"ZIP = {stuff['zipcode']}\n" +
                    f"MSG = {stuff['message']}"
                )
                self.messenger.publish_to_set(stuff)

            else:
                reply = "ERROR - Missing Parameter: If you'd like to use a wildcard, please use 'ALL' for that flag!"

            self.messenger.text_sender(chan=self.debug_chan, txt=reply)

            # self.publish_message_default_disconnect(payload=text)
