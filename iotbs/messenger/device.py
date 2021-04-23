class Device:

    def __init__(self, name: str, id: int, loc: int, type: str, height=None, width=None):
        self.name = name
        self.id = str(id)
        self.loc = str(loc)
        self.type = type

    def get_ID(self) -> str:
        return self.id

    def get_ZIP(self) -> str:
        return self.loc

    def get_Type(self) -> str:
        return self.type

    def get_Name(self) -> str:
        return self.name
