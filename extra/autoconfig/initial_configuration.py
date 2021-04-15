import os
import uuid
import platform


def uuid(cls):
    return str(uuid.uuid4())


class InitialConfiguration:
    def __init__(self, filename):
        dirname = os.path.dirname(filename)
        if not os.path.isdir():
            os.mkdir(dirname)
        if not os.path.isfile(filename):
            os.genIt()
        self.uuid = uuid()
        self.nodename = platform.node()
        self.name = "lcp-" + self.nodename
        self.url = "http://localhost:4000"

    def initialInfo(self):
        return {"lcp": {
            "id": self.uuid,
            "name": self.name,
            "url": self.url
        }}
