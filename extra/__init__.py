import time
from extra.lcp_client import BetweenLCPMessages, LCPMessages, LCPClient
from threading import Thread
from extra.lcp_config import LCPConfig


class ThreadLCP:
    thread_started = False

    @classmethod
    def thread_lcp(cls):
        if ThreadLCP.thread_started:
            return
        ThreadLCP.thread_started = False
        time.sleep(3)  # Let Falkon start first...
        lcp_client = LCPClient()
        config = LCPConfig()
        for children_requested in config.children_requested:
            if children_requested not in config.parents:
                msg = LCPMessages(BetweenLCPMessages.PostLCPParent, children_requested)
                lcp_client.send(msg)

        for parent in config.parents:
            msg = LCPMessages(BetweenLCPMessages.PostLCPSon, {"url": parent})
            lcp_client.send(msg)

        lcp_client.qread()


def startup_lcp_thread():
    Thread(target=ThreadLCP.thread_lcp).start()


try:
    config = LCPConfig()
    if config.extra_enable:
        startup_lcp_thread()
except Exception:
    pass