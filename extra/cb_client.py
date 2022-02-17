import enum
import threading
import time
from queue import Queue
from extra.lcp_config import LCPConfig
import requests
import traceback
import json
from extra.cb_helpers.agent_type_helper import AgentTypeForCBHelper
from extra.cb_helpers.agent_instance_helper import AgentInstanceHelper
from utils.log import Log

TIMEOUT = 5


class DeleteThisToContextBrokerMessages(enum.Enum):
    AddExecEnvironment = 1
    AddAgentType = 2
    AddAgentInstance = 3
    END_THREAD = 100


class DeleteThisCBMessages:
    def __init__(self, message_type: DeleteThisToContextBrokerMessages, data):
        self.message_type = message_type
        self.data = data

class DeleteThisCBClient:
    class __CBClient:
        def __init__(self):
            self.config = LCPConfig()
            self.q = Queue()
            self.log = Log.get('CBClient')
            self.controller = None

        def set_controller(self, controller):
            self.controller = controller

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
                self.log.notice("get  to %s  - rep %d - %s" % (query, resp.status_code, resp.json()))
            except TimeoutError as e:
                self.log.exception(e)
                return False

            if resp.status_code == 200:
                return True

            return False

        def exists_exec_env_type(self):
            cb = self.config.context_broker
            if not 'context_broker' in self.config.config:
                return False
            query = self.config.context_broker['url'] + '/exec-env-type/' + self.config.exec_env_type

            try:
                headers = self.headers()
                resp = requests.get(query, headers=headers, timeout=TIMEOUT)
                self.log.notice("get  to %s  - rep %d - %s" % (query, resp.status_code, resp.json()))
            except (ConnectionError, TimeoutError) as e:
                self.log.exception(e)
                return False

            if resp.status_code == 200:
                return True

            return False

        def post_exec_env_type(self):
            cb = self.config.context_broker
            if not 'context_broker' in self.config.config:
                return False
            query = self.config.context_broker['url'] + '/type/exec-env'
            data = {"id": self.config.exec_env_type, "name": self.config.exec_env_type}

            try:
                headers = self.headers()
                resp = requests.post(query, headers=headers, timeout=TIMEOUT,
                                     data = json.dumps(data))
                self.log.notice("Post  to %s  - rep %d - %s" % (query, resp.status_code, resp.json()))
                if resp.status_code in (200,201):
                    time.sleep(1) ## Ensure data is stored in elastic
            except (ConnectionError, TimeoutError) as e:
                self.log.exception(e)

        def ensure_exec_environment_type(self):
            if not self.exists_exec_env_type():
                self.post_exec_env_type()

        def post_exec_environment(self, data):
            if not 'context_broker' in self.config.config:
                return False

            self.ensure_exec_environment_type()

            query = self.config.context_broker['url'] + '/exec-env'
            data = self.config.exec_env_register_data()

            try:
                if not self.is_lcp_registered():
                    resp = requests.post(query, headers=self.headers(), timeout=TIMEOUT,
                                         data=json.dumps(data))
                    self.log.notice("post  to %s  - resp %d - %s" % (query, resp.status_code, resp.json()))
                else:
                    return
            except TimeoutError as e:
                traceback.print_exc()
                return False

            if resp.status_code in (200, 201, 406):
                return
            else:
                message = DeleteThisCBMessages(DeleteThisToContextBrokerMessages.AddExecEnvironment, data)
                threading.Timer(15, self.send, [message]).start() #Retry in 15 secs.


        def post_agent_type(self, agent):
            if not 'context_broker' in self.config.config:
                return False
            query = self.config.context_broker['url'] + '/catalog/agent'
            data = AgentTypeForCBHelper(agent).dumps()

            try:
                resp = requests.post(query, headers=self.headers(), timeout=TIMEOUT,
                                     data=data)
                self.log.notice("post  to %s  - resp %d - %s" % (query, resp.status_code, resp.json()))
            except TimeoutError:
                return False

            if resp.status_code in (200, 201, 406):
                return
            else:
                message = DeleteThisCBMessages(DeleteThisToContextBrokerMessages.AddAgentType, agent)
                threading.Timer(15, self.send, [message]).start() #Retry in 15 secs.

        def post_agent_instance(self, agent_instance):
            if not 'context_broker' in self.config.config:
                return False
            query = self.config.context_broker['url'] + '/instance/agent'
            data = AgentInstanceHelper(agent_instance).dumps()
            try:
                resp = requests.post(query, headers=self.headers(), timeout=TIMEOUT,
                                     data=data)
                self.log.notice("post  to %s  - resp %d - %s" % (query, resp.status_code, resp.json()))
            except TimeoutError:
                return False

            if resp.status_code in (200, 201, 406):
                return
            else:
                message = DeleteThisCBMessages(DeleteThisToContextBrokerMessages.AddAgentInstance, agent_instance)
                threading.Timer(15, self.send, [message]).start() #Retry in 15 secs.

        def qread(self):
            while True:
                message = self.q.get()

                if message.message_type ==DeleteThisToContextBrokerMessages.AddExecEnvironment:
                    self.post_exec_environment(message.data)
                elif message.message_type == DeleteThisToContextBrokerMessages.AddAgentType:
                    self.post_agent_type(message.data)
                elif message.message_type == DeleteThisToContextBrokerMessages.AddAgentInstance:
                    self.post_agent_instance(message.data)
                elif message.message_type == DeleteThisToContextBrokerMessages.END_THREAD:
                    break

        def send(self, message: DeleteThisCBMessages):
            self.q.put(message)

    instance = None

    def __new__(cls, *args, **kwargs):
        if DeleteThisCBClient.instance is None:
            DeleteThisCBClient.instance = DeleteThisCBClient.__CBClient()
        return DeleteThisCBClient.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
