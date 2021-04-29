import enum
import threading
from queue import Queue
from extra.lcp_config import LCPConfig
import requests
import traceback
import json

TIMEOUT = 5


class ToContextBrokerMessages(enum.Enum):
    AddExecEnvironment = 1
    AddAgentType = 2
    AddAgentInstance = 3


class CBMessages:
    def __init__(self, message_type: ToContextBrokerMessages, data):
        self.message_type = message_type
        self.data = data

class CBClient:
    class __CBClient:
        def __init__(self):
            self.config = LCPConfig()
            self.q = Queue()

        def headers(self):
            headers = {"content-type": "application/json"}
            if 'context_broker' in self.config.config:
                try:
                    headers['authorization'] = self.config.context_broker['auth_header']
                except KeyError as e:
                    traceback.print_exc()
                    pass

            return headers

        def is_lcp_registered(self):
            cb = self.config.context_broker
            if not 'context_broker' in self.config.config:
                return False
            query = self.config.context_broker['url'] + '/exec-env/' + self.config.lcp['id']

            try:
                headers = self.headers()
                resp = requests.get(query, headers=headers, timeout=TIMEOUT)
            except TimeoutError:
                return False

            if resp.status_code == 200:
                return True

            return False

        def post_exec_environment(self, data):
            if not 'context_broker' in self.config.config:
                print("Not context_broker!!!")
                return False
            query = self.config.context_broker['url'] + '/exec-env'
            data = self.config.exec_env_register_data()

            try:
                if not self.is_lcp_registered():
                    resp = requests.post(query, headers=self.headers(), timeout=TIMEOUT,
                                         data=json.dumps(data))
                else:
                    print("YA CREADO!")
                    return
            except TimeoutError as e:
                traceback.print_exc()
                return False

            if resp.status_code in (200, 201):
                pass
            else:
                message = CBMessages(ToContextBrokerMessages.AddExecEnvironment, data)
                threading.Timer(15, self.send, [message]).start() #Retry in 15 secs.


        def post_agent_type(self, data):
            pass

        def post_agent_instance(self, data):
            pass

        def qread(self):
            while True:
                message = self.q.get()

                if message.message_type == ToContextBrokerMessages.AddExecEnvironment:
                    self.post_exec_environment(message.data)
                elif message.message_type == ToContextBrokerMessages.AddAgentType:
                    self.post_agent_type(message.data)
                elif message.message_type == ToContextBrokerMessages.AddAgentInstance:
                    self.post_agent_instance(message.data)

        def send(self, message: CBMessages):
            self.q.put(message)

    instance = None

    def __new__(cls, *args, **kwargs):
        if CBClient.instance is None:
            CBClient.instance = CBClient.__CBClient()
        return CBClient.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
