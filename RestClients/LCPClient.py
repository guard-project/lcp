from lib.lcp_config import LCPConfig
import requests
from requests.exceptions import Timeout
import threading
import json
from schema.filiation import ContextBrokerConnection as ContextBrokerConnectionSchema
from marshmallow import ValidationError

from queue import Queue
import enum
import base64
from threading import Thread


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
            auth = self.config['user'] + ":" + self.config['password']
            auth_b64 = base64.b64encode(auth)
            headers['Authorization'] = "Basic " + auth_b64
            return headers

        def postLcpSon(self):
            if len(self.config.parents) > 0:
                parent = self.config.parents[0]

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
                threading.Timer(15, self.filiate).start()

        def postLcpParent(self, message):
            """
            When a /lcp_parent request is recieved, this LCP, as son, will send its data to
            parent LCP in order to get the information of the parent. --- It filiates itself.

            It keeps retrying every 15seconds for a good connection

            :param parent: dictionary containing 'url' of parent's
            :return: Nothing.
            """
            data = {"url": self.config.lcp['url']}
            headers = self.getHeaders()
            try:
                url = parent['url'] +"/lcp_parent"

                j = json.dumps(self.config.lcp)
                resp = requests.post(url, headers=headers,
                                     json=j, timeout=5000)
                if resp.status_code == 202: #Accepted
                    message = LCPMessages(BetweenLCPMessages.ConnectLCPSon, self.config.lcp)
                    self.send(message)
                else:
                    raise Timeout
            except Timeout as e:
                print(e)
                threading.Timer(15, self.postLcpParent(), [parent]).start()


        def qread(self):
            while True:
                message = self.q.read()
                if message.message_type == BetweenLCPMessages.ConnectLCPSon:
                    self.postLcpSon()
                elif message.message_type == BetweenLCPMessages.ConnectLCPParent:
                    self.postLcpSon(message.data)

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
