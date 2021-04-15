from extra.lcp_config import LCPConfig

class ContextBrokerThread(object):
    class __ContextBrokerThread:
        def __init__(self):
            self.cfg = LCPConfig()

        def is_registered(self):
            pass

        def post_register(self):
            pass


    instance = None

    def __new__(cls, *args, **kwargs):
        if ContextBrokerThread.instance is None:
            ContextBrokerThread.instance = ContextBrokerThread.__ContextBrokerThread()
        return ContextBrokerThread.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
