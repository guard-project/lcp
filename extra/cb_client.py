import enum


class ToContextBrokerMessages(enum.Enum):
    AddExecEnvironment = 1


class CBClient:
    def __init__(self, message_type: ToContextBrokerMessages, data):
        self.message_type = message_type
        self.data = data

    def QueryExecEnvironments(self):
        pass
