import os
from extra.lcp_config import LCPConfig
from flask import Flask, request
from flask_restful import Resource, Api
from threading import Thread
import time
from queue import Queue
import json
import requests
from lib.token import create_token


def loadExampleFile(filename):
    json_file = os.path.dirname(__file__) + \
                "/examples/" + filename
    with open(json_file) as f:
        file_data = f.read()
    return json.loads(file_data)


def getAuthorizationHeaders():
    return {"Authorization": create_token(),
           "content-type": "application/json"}


def getLCPConfig():
    config = LCPConfig("examples/TestConfigFile.yaml")
    config.testing = True
    return config


class TestCBPostExecEnv(Resource):
    def post(self):
        pass

    def put(self):
        pass

    def get(self):
        pass


app = Flask("test_server")


@app.route("/terminate", methods=['POST'])
def terminate():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "", 200


@app.route("/lcp_son", methods=['POST'])
def lcp_son_post():
    r = request
    if not request.is_json:
        return None, 406
    TestHttpServer.q.put(request.json)
    return '{"url": "http://localhost:5000"}', 202


@app.route("/catalog/agent", methods=["POST", "PUT", "GET"])
def post_catalog_agent():
    r = request
    if not request.is_json:
        return None, 406
    json_data = request.json
    print("MOCK-HTTP: ", json_data)
    TestHttpServer.q.put(json_data)
    return "", 202

@app.route("/exec-env", methods=["POST", "PUT", "GET"])
def post_exec_env():
    return "", 200

@app.route("/exec-env/<eid>", methods=["POST", "PUT", "GET"])
def post_exec_env_env_id(eid=None):
    if eid is None:
        print("NONE Parameter... res de res")
    else:
        print("eid:", eid)
    return "", 200


# self.api.add_resource(TerminateHttpServer, "/terminate")
# self.api.add_resource(TestLCPSonFiliationRequest, "/lcp_son")
# self.api.add_resource(TestCBPostAgent, "/catalog/agent")
# self.api.add_resource(TestCBPostExecEnv, "/exec-env")
# self.api.add_resource(self.post_exec_env, "/exec-env/<eeid>")
class TestHttpServer:
    q = Queue()

    def post_exec_env(self, eeid=None):
        print("Somewhere far beyond!")
        pass

    def __init__(self):
        self.api = Api(app)
        self.port = 4884
        app.run(port=self.port)


def new_http_server():
    TestHttpServer()


def start_mock_http_server():
    time.sleep(1)
    Thread(target=new_http_server).start()
    time.sleep(1)


def stop_mock_http_server():
    requests.post("http://localhost:4884/terminate", json=json.dumps({"hello": "world"}))
    time.sleep(1)


if __name__ == "__main__":
    #     stop_mock_http_server()
    start_mock_http_server()
    stop_mock_http_server()
