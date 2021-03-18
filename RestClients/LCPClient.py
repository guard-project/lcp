from lib.lcp_config import LCPConfig
import requests
from requests.exceptions import Timeout
import threading
import json
from schema.filiation import ContextBrokerConnection as ContextBrokerConnectionSchema
from marshmallow import ValidationError

from queue import Queue
import enum

from threading import Thread


class BetweenLCPMessages(enum.Enum):
    ConnectLCPSon = 1
    ConnectLCPParent = 2


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

        def filiate(self):
            if len(self.config.parents) > 0:
                parent = self.config.parents[0]

            headers = {"content-type: application/json"}
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

        def messageLcpParent(self, parent):
            """
            When a /lcp_parent request is recieved, this LCP, as son, will send its data to
            parent LCP in order to get the information of the parent. --- It filiates itself.

            It keeps retrying every 15seconds for a good connection

            :param parent: dictionary containing 'url' of parent's
            :return: Nothing.
            """
            data = {"url": self.config.lcp['url']}
            headers = {"content-type": "application/json"}
            try:
                url = parent['url'] +"/lcp_son"
                j = json.dumps(LCPConfig().lcp)
                resp = requests.post(url, headers=headers,
                                     json=j, timeout=5000)
                if resp.status_code == 202: #Accepted
                    message = LCPMessages(BetweenLCPMessages.ConnectLCPSon, self.config.lcp)
                    self.send(message)
                else:
                    raise Timeout
            except Timeout as e:
                print(e)
                threading.Timer(15, self.sendParentMessageToLCPSon, [parent]).start()


        def __qread(self):
            while True:
                message = self.q.read()
                if message.message_type == BetweenLCPMessages.ConnectLCPSon:
                    self.filiate()
                elif message.message_type == BetweenLCPMessages.ConnectLCPParent:
                    self.messageLcpParent(message.data)

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
