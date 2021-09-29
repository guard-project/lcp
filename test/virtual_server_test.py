from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import VirtualServer, Disk, DiskPartition, ExecutionEnvironment
from resource.hardware_definitions import VirtualServer as VirtualServerResource
import json
import os
from test_utils import *
from test.testbase import LCPTestBase

class TestMyApp(LCPTestBase):
    def test_virtual_server(self):
        server = loadExampleFile("virtual-server-example.json")
        bm_server = VirtualServer(many=False)
        try:
            d = bm_server.load(server)
            print(d)
            assert(True)
        except ValidationError as ve:
            print(ve)
            assert(False)


    def test_get_virtual_server(self):
        bm_server = loadExampleFile("virtual-server-example.json")
        headers = getAuthorizationHeaders()

        cfg = LCPConfig()
        data = {"executionType": "vm", "environment": bm_server}
        cfg.setDeployment(data)

        result = self.simulate_get("/self/deployment", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        print(body)
        assert body['executionType'] == "vm"
        assert body['environment'] == bm_server

        try:
            bm_schema = VirtualServer(many=False)
            bm_schema.load(body['environment'])
            assert True
        except ValidationError as ve:
            print(ve)
            assert False


    def test_post_virtual_server(self):
        bm_server_dict = loadExampleFile("virtual-server-example.json")
        headers = getAuthorizationHeaders()
        data = {"executionType": "vm", "environment": bm_server_dict}

        body = json.dumps(data)
        result = self.simulate_post("/self/deployment", headers=headers,
                                    body=body)
        assert result.status_code == 201



