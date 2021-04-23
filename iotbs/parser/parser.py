import re


class Parser:

    def __init__(self):
        self.compiled_regexes = [
            re.compile(r"-m \"{1}.+\"{1}"),     # regex for message
            re.compile(r"-z \w{3,5}"),          # regex for zip code topic
            re.compile(r"-t \w{1,5}"),          # regex for type topic
            re.compile(r"-i \w{3,5}"),          # regex for id topic
        ]

    def parse_slack(self, message: str) -> dict:

        text = re.search(self.compiled_regexes[0], message)
        if text is not None:
            strText = text.group().split(' ', 1)[1].strip("\"")
        else:
            strText = ""

        zip = re.search(self.compiled_regexes[1], message)
        if zip is not None:
            strZip = zip.group().split(' ')[1]
            if strZip.lower() == "all":
                strZip = "ALL"
        else:
            strZip = ""

        msgtype = re.search(self.compiled_regexes[2], message)
        if msgtype is not None:
            strType = msgtype.group().split(' ')[1]
            if strType.lower() == "all":
                strType = "ALL"
        else:
            strType = ""

        device = re.search(self.compiled_regexes[3], message)
        if device is not None:
            strDevID = device.group().split(' ')[1]
            if strDevID.lower() == "all":
                strDevID = "ALL"
        else:
            strDevID = ""

        msg = {
            "message": strText,
            "zipcode": strZip,
            "msgtype": strType,
            "device": strDevID,
        }

        return msg

    def isComplete(self, msg_params: dict) -> bool:

        isGood = True

        for val in msg_params.values():
            if val == "":
                return False

        return isGood
