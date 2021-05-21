from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
import os
import json
from schema.cloudschema import CloudSchema
from resource.cloud_resource import CloudInfrastructure
from resource.software_definition import SoftwareDefinition as SoftwareDefinitionResource
from marshmallow.exceptions import ValidationError
from test_utils import *

from test.testbase import LCPTestBase


class TestMyApp(LCPTestBase):
    def _getSecurityFucntionExample(self):
        json_file = os.path.dirname(__file__) + \
                    "/examples/security-function-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    def test_cloud_infrastructure(self):
        cl_dict = loadExampleFile("cloud-infrastructure-example.json")
        cloud_schema = CloudSchema(many=False)
        try:
            d = cloud_schema.load(cl_dict)
            assert True
        except ValidationError as ve:
            print(ve)
            assert False

    def test_get_cloud_infrastructure(self):
        cl_dict = loadExampleFile("cloud-infrastructure-example.json")
        headers = getAuthorizationHeaders()
        CloudInfrastructure.data = []

        result = self.simulate_get("/cloud", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        CloudInfrastructure.data.append(cl_dict)
        result = self.simulate_get("/cloud", headers=headers)
        assert result.status == "200 OK"
        body = result.json
        assert type(body) is list
        assert len(body) == 1

        try:
            cloud_schema = CloudSchema(many=True)
            cloud_schema.load(body)
            assert True
        except ValidationError as ve:
            print(ve)
            assert False

