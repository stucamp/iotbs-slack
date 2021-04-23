def message(event):
    reply = (
        f"Event Type: {event.type}\n"
        f"Sub Type: {event.subtype}\n"
        f"Channel ID: {event.channel_id}\n"
        f"Channel Name: <#{event.channel_id}>\n"
        f"User ID: {event.user_id}\n"
        f"Message: {event.text}\n"
        f"Timestamp: {event.ts}"
    )
    return reply


def app_mention(event):
    reply = (
        f"Event Type: {event.type}\n"
        f"User ID: {event.user_id}\n"
        f"Message: {event.text}\n"
        f"Timestamp: {event.ts}\n"
        f"Channel ID: {event.channel_id}\n"
        f"Event TS: {event.event_ts}"
    )
    return reply
