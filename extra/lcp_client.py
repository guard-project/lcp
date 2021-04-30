from extra.lcp_config import LCPConfig
import requests
from requests.exceptions import Timeout
import threading
import json
from schema.filiation import ContextBrokerConnection as ContextBrokerConnectionSchema
from marshmallow import ValidationError
from extra.cb_helpers.agent_type_helper import AgentTypeForCBHelper
from queue import Queue
import enum
import base64


class BetweenLCPMessages(enum.Enum):
    PostLCPSon = 1
    PostLCPParent = 2


class LCPMessages:
    def __init__(self, message_type:BetweenLCPMessages, data):
        self.message_type = message_type
        self.data = data


class LCPClient(object):
    class __LCPClient:
        def __init__(self):
            self.config = LCPConfig()
            self.filated = False
            self.q = Queue()

        def getHeaders(self):
            headers = {'content-type': 'application/json'}
            auth = self.config.user + ":" + self.config.password
            auth_b64 = base64.b64encode(auth.encode('utf-8'))
            headers['Authorization'] = "Basic " + str(auth_b64, "utf-8")
            return headers

        def reenqueuePostLcpSon(self, parent):
            message = LCPMessages(BetweenLCPMessages.PostLCPSon, parent)
            self.send(message)

        def postLcpSon(self, parent):
            headers = self.getHeaders()
            payload = self.config.lcp
            try:
                resp = requests.post(parent['url'] + "/lcp_son", headers=headers,
                                     data=json.dumps(payload), timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    cb_schema = ContextBrokerConnectionSchema()
                    self.config.setContextBroker()
                    cb_schema.validate(resp.json())
            except (Timeout, ValidationError) as e:
                threading.Timer(15, self.postLcpSon).start()


        def reenqueueLcpParentToSon(self, requested_children_url):
            message = LCPMessages(BetweenLCPMessages.PostLCPParent, requested_children_url)
            self.send(message)

        def postLcpParentToSon(self, requested_children_url):  # I am your faher
            """
            When a /lcp_parent request is recieved, this LCP, as son, will send its data to
            parent LCP in order to get the information of the parent. --- It filiates itself.

            It keeps retrying every 15seconds for a good connection

            :param parent: dictionary containing 'url' of parent's
            :return: Nothing.
            """
            err = False
            data = {"url": self.config.lcp['url']}
            headers = self.getHeaders()
            try:
                url = requested_children_url +"/lcp_son"
                print("Post ", url)

                j = json.dumps({"url": self.config.lcp['url']})
                resp = requests.post(url, headers=headers,
                                     json=data, timeout=5000)
                if resp.status_code != 202: #Accepted
                    err = True
            except Timeout as e:
                err = True

            if err:
                threading.Timer(15, self.reenqueueLcpParentToSon, [requested_children_url]).start()

        def get_exec_env_data(self):
            d = {}
            d['id'] = self.config.lcp


        def qread(self):
            while True:
                message = self.q.get()

                if message.message_type == BetweenLCPMessages.PostLCPSon:
                    self.postLcpSon(message.data)
                elif message.message_type == BetweenLCPMessages.PostLCPParent:
                    self.postLcpParentToSon(message.data)

        def send(self, message: LCPMessages):
            self.q.put(message)


    instance = None

    def __new__(cls, *args, **kwargs):
        if LCPClient.instance is None:
            LCPClient.instance = LCPClient.__LCPClient()
        return LCPClient.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
