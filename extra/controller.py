from extra.lcp_config import LCPConfig
from extra.hw_helpers.host_info import HostInfoToLcpHelper
from extra.clients_starter import startup_client_threads
from extra.lcp_client import BetweenLCPMessages, LCPMessages, LCPClient
from extra.cb_client import ToContextBrokerMessages, CBMessages, CBClient
import time


class LCPController:
    class __LCPController:
        def __init__(self):
            self.config = LCPConfig()
            self.build_environment()

            self.initial_messages_to_lcp_sent = False
            self.initial_messages_to_cb_sent = False

        def build_environment(self):
            if self.config.exec_env_type is None:
                host_info = HostInfoToLcpHelper().js_info
                print(host_info)
                self.config.setDeployment(host_info)

        def start_threads(self):
            startup_client_threads()
            time.sleep(2)  # Let Falkon start first...
            self.send_initial_messages_cb()
            self.send_initial_messages_lcp()

        def send_msg_cb(self):
            pass

        def send_initial_messages_cb(self):
            cb = self.config.context_broker
            if cb is None:
                # No CB is configured. Can't end messages
                return

            # Register this LCP to ContextBroker
            message = CBMessages(ToContextBrokerMessages.AddExecEnvironment,
                                 self.config.exec_env_register_data())
            cb_client = CBClient()
            cb_client.send(message)

            # Register AgentTypes
            for agent_type in self.config.agent_types:
                message = CBMessages(ToContextBrokerMessages.AddAgentType,
                                     agent_type)
                cb_client.send(message)

            # In case of new registered LCP, let logstash have some time
            # to finish its task...
            time.sleep(1)

            # Register Agents
            for agent in self.config.agents:
                message = CBMessages(ToContextBrokerMessages.AddAgentInstance, agent)
                cb_client.send(message)

            self.initial_messages_to_cb_sent = True

        def send_initial_messages_lcp(self):
            lcp = self.config.lcp
            if lcp is None:
                # No lcp is configured. Can't send messages
                return

            lcp_client = LCPClient()
            for children_requested in self.config.children_requested:
                if children_requested not in self.config.parents:
                    msg = LCPMessages(BetweenLCPMessages.PostLCPParent, children_requested)
                    lcp_client.send(msg)

            for parent in self.config.parents:
                msg = LCPMessages(BetweenLCPMessages.PostLCPSon, {"url": parent})
                lcp_client.send(msg)

            self.initial_messages_to_lcp_sent = True

        def send_msg_lcp(self):
            pass

        def set_self_initial_configuration(self, payload):
            self.config.setInitialConfiguration(payload)

            if 'context_broker' in payload and not self.initial_messages_to_cb_sent:
                self.send_initial_messages_cb()

            if 'lcp' in payload and not self.initial_messages_to_lcp_sent:
                self.send_initial_messages_lcp()

        def set_agent_type(self, playload):
            self.config.setAgentType(playload)
            if self.config.context_broker is not None:
                message = CBMessages(ToContextBrokerMessages.AddAgentType, playload)
                CBClient().send(message)

        def set_agent_instance(self, payload):
            req_agent_type = payload['type']
            agent_type = self.config.get_agent_type_by_id(req_agent_type)
            if agent_type is None:
                raise KeyError()
            self.config.setAgent(payload)
            if self.config.context_broker is not None:
                message = CBMessages(ToContextBrokerMessages.AddAgentInstance, payload)
                CBClient().send(message)


    instance = None

    def __new__(cls):
        if LCPController.instance is None:
            LCPController.instance = LCPController.__LCPController()
        return LCPController.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


if __name__ == "__main__":
    LCPController()
    print("DONE!")
