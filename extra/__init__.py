import time
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
        ThreadLCP.thread_started = True
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


class ThreadCB:
    thread_started = False

    @classmethod
    def send_cb_messages(cls):
        cb_client = CBClient()

        # Register to ContextBroker
        message = CBMessages(ToContextBrokerMessages.AddExecEnvironment,
                             config.exec_env_register_data())
        cb_client.send(message)

        # Register AgentTypes
        for agent_type in config.agent_types:
            message = CBMessages(ToContextBrokerMessages.AddAgentType,
                                 agent_type)
            cb_client.send(message)

        # Register Agents
        for agent in config.agents:
            message = CBMessages(ToContextBrokerMessages.AddAgentInstance, agent)
            cb_client.send(message)

    @classmethod
    def thread_cb(cls):
        if ThreadCB.thread_started:
            return

        config = LCPConfig()
        if config.context_broker is None:
            return

        ThreadCB.thread_started = True
        time.sleep(3)  # Let Falkon start first...

        ThreadCB.send_cb_messages()
        cb_client = CBClient()
        cb_client.qread()


def startup_client_threads():
    Thread(target=ThreadLCP.thread_lcp).start()
    Thread(target=ThreadCB.thread_cb).start()


try:
    config = LCPConfig()
    if config.extra_enable:
        startup_client_threads()
except Exception:
    pass
