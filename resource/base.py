from utils.log import Log


class Base_Resource(object):
    def __init__(self):
        """Initialize the log."""
        self.log = Log.get(self.routes[0].replace('/', ''))
