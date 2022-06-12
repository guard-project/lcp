from extra.lcp_config import LCPConfig
from extra.hw_helpers.host_info import HostInfoToLcpHelper
from extra.clients_starter import startup_client_threads
from extra.lcp_client import BetweenLCPMessages, LCPMessages, LCPClient
from schema.hardware_definitions import ExecutionEnvironment
from marshmallow import ValidationError
import time
import json

import hashlib


class LCPController:
    class __LCPController:
        def __init__(self):
            self.config = LCPConfig()
            self.migrate_agents()
            self.build_environment()

            self.initial_messages_to_lcp_sent = False

            LCPClient().set_controller(self)

        def reset(self):
            self.config = LCPConfig()
            self.migrate_agents()
            self.build_environment()

            self.initial_messages_to_lcp_sent = False

            LCPClient().set_controller(self)

        def migrate_agents(self):
            agents = self.config.agent_types
            for a in agents:
                self.tweak_old_agent_type(a)
                self.config.set_agent_type(a)

        def build_environment(self):
            if self.config.exec_env_type is None:
                host_info = HostInfoToLcpHelper().js_info
                try:
                    ExecutionEnvironment(many=False).validate(host_info)
                except ValidationError as ve:
                    print(ve.messages)
                    raise ve
                self.config.setDeployment(host_info)

        def start_threads(self):
            startup_client_threads()
            time.sleep(2)  # Let Falkon start first...
            self.send_initial_messages_lcp()

        def send_msg_cb(self):
            pass

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
            payload['exec_env_type'] = self.config.exec_env_type
            self.config.setInitialConfiguration(payload)

            if 'lcp' in payload and not self.initial_messages_to_lcp_sent:
                self.send_initial_messages_lcp()

        def set_agent_type(self, playload):
            self.config.set_agent_type(playload)

        def set_agent_instance(self, payload):
            req_agent_type = payload['hasAgentType']
            agent_type = self.config.get_agent_type_by_id(req_agent_type)
            if agent_type is None:
                raise KeyError()
            self.config.set_agent(payload)

        def set_context_broker(self, payload):
            self.config.setContextBroker(payload)
            if self.config.context_broker is not None:
                self.send_initial_messages_cb()

        def tweak_old_agent_type(self, data):
            resources = None
            if 'schema' in data:
                if data['schema'] == 'cb-defined':
                    data['resources'] = []
                if 'resources' not in data:
                    data['resources'] = []
                    resources = {"schema": data['schema']}
                    data.pop('schema')
                    if 'source' in data:
                        resources['source'] = data['source']
                        data.pop('source')
                    if 'parameters' in data:
                        resources['parameters'] = data['parameters']
                        for r in resources['parameters']:
                            if 'id' not in r:
                                sha1 = hashlib.sha1()
                                sha1.update(r['path'].encode('UTF-8'))
                                r['id'] = sha1.hexdigest()
                        data.pop('parameters')
                    if not 'id' in data['resources']:
                        sha1 = hashlib.sha1()
                        sha1.update(resources['source'].encode('UTF-8'))
                        resources['id'] = sha1.hexdigest()
                        resources['type'] = 'AgentResource'
                    data['resources'].append(resources)

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
