from extra.lcp_client import BetweenLCPMessages, LCPMessages, LCPClient
from extra.cb_client import ToContextBrokerMessages, CBMessages, CBClient
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


class ThreadCB:
    thread_started = False

    @classmethod
    def thread_cb(cls):
        if ThreadCB.thread_started:
            return

        config = LCPConfig()

        ThreadCB.thread_started = True

        cb_client = CBClient()

        cb_client.qread()
        ThreadCB.thread_started = False


def startup_client_threads():
    Thread(target=ThreadLCP.thread_lcp).start()
    Thread(target=ThreadCB.thread_cb).start()


def end_client_threads():
    et1 = CBMessages(ToContextBrokerMessages.END_THREAD, "")
    et2 = LCPMessages(BetweenLCPMessages.END_THREAD, "")
    LCPClient().send(et2)
    CBClient().send(et1)
