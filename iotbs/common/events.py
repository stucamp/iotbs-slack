class MessageEvent:
    def __init__(self, payload):
        self.event = payload.get("event", {})
        self.type = self.event.get("type")
        self.subtype = self.event.get("subtype")
        self.hidden = self.event.get("hidden")
        self.channel_id = self.event.get("channel")
        self.user_id = self.event.get("user")
        self.text = self.event.get("text")
        self.ts = self.event.get("ts")
        self.message = self.event.get("message", {})


class AppMentionEvent:
    def __init__(self, payload):
        self.event = payload.get("event", {})
        self.type = self.event.get("type")
        self.user_id = self.event.get("user")
        self.text = self.event.get("text")
        self.ts = self.event.get("ts")
        self.channel_id = self.event.get("channel")
        self.event_ts = self.event.get("event_ts")
