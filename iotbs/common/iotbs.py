import os
from dotenv import load_dotenv
from iotbs.common.objects import User
from slack import WebClient
from slackeventsapi import SlackEventAdapter


class IoTbs:

    def __init__(self, app):
        load_dotenv()
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET")
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.bot_client = WebClient(token=self.bot_token)
        self.event_adapter = SlackEventAdapter(self.signing_secret, "/", app)

    def getClient(self) -> WebClient:

        return self.bot_client

    def getAdapter(self) -> SlackEventAdapter:

        return self.event_adapter

    def get_user_as_obj(self, user_id: str) -> User:

        return User(self.bot_client.users_info(user=user_id).get("user", {}))
