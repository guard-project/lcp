from extra.lcp_client import BetweenLCPMessages, LCPMessages, LCPClient
from threading import Thread
from extra.lcp_config import LCPConfig


class ThreadLCP:
    thread_started = False

    @classmethod
    def thread_lcp(cls):
        if ThreadLCP.thread_started:
            return
        lcp_client = LCPClient()
        ThreadLCP.thread_started = True
        lcp_client.qread()
        ThreadLCP.thread_started = False



def startup_client_threads():
    Thread(target=ThreadLCP.thread_lcp).start()


def end_client_threads():
    et2 = LCPMessages(BetweenLCPMessages.END_THREAD, "")
    LCPClient().send(et2)
