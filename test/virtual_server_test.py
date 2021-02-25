from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import VirtualServer, Disk, DiskPartition
from resource.hardware_definitions import VirtualServer as VirtualServerResource
import json
import os
from test_utils import *


class VirtualServerTesting(testing.TestCase):
    def setUp(self):
        super(VirtualServerTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                       dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(VirtualServerTesting):
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
        VirtualServerResource.data = []

        result = self.simulate_get("/virtualserver", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        VirtualServerResource.update_data(bm_server)
        result = self.simulate_get("/virtualserver", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 1

        try:
            bm_schema = VirtualServer(many=True)
            bm_schema.load(body)
            assert True
        except ValidationError as ve:
            print(ve)
            assert False


    def test_post_virtual_server(self):
        bm_server_dict = loadExampleFile("virtual-server-example.json")
        headers = getAuthorizationHeaders()
        VirtualServerResource.data = []

        body = json.dumps(bm_server_dict)
        result = self.simulate_post("/virtualserver", headers=headers,
                                    body=body)
        assert result.status_code == 201
        assert len(VirtualServerResource.data) == 1
        assert VirtualServerResource.data[0]["id"] == bm_server_dict["id"]


