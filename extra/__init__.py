import time
from extra.lcp_config import LCPConfig
from extra.lcp_client import BetweenLCPMessages, LCPMessages, LCPClient
from threading import Thread


def threadLCP():
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


Thread(target=threadLCP).start()
