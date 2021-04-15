import os
from extra.lcp_config import LCPConfig
from flask import Flask, request
from flask_restful import Resource, Api
from threading import Thread
import time
from queue import Queue
import json

def loadExampleFile(filename):
    json_file = os.path.dirname(__file__) + \
                    "/examples/" + filename
    with open(json_file) as f:
        file_data = f.read()
    return json.loads(file_data)


def getAuthorizationHeaders():
    return {"Authorization": "Basic bGNwOmd1YXJk"}

def getLCPConfig():
    config = LCPConfig("examples/TestConfigFile.yaml")
    config.testing = True
    return config


class TerminateHttpServer(Resource):
    def post(self):
        r = request
        if not request.is_json:
            return None, 406
        print(request.json)
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


class TestLCPSonFiliationRequest(Resource):
    def post(self):
        r = request
        if not request.is_json:
            return None, 406
        print(request.json)
        TestHttpServer.q.put(json.loads(request.json))
        print("Something set on queue!!!")
        return "", 202



class TestHttpServer:
    q = Queue()
    def __init__(self):
        self.app = Flask("test_server")
        self.api = Api(self.app)

        self.api.add_resource(TerminateHttpServer, "/terminate")
        self.api.add_resource(TestLCPSonFiliationRequest, "/lcp_son")
        self.port = 4884
        self.app.run(port=self.port)


def new_http_server():
    TestHttpServer()


def start_http_server():
    Thread(target=new_http_server).start()
    time.sleep(1)
