from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
import os
import json
from schema.software_definitions import SoftwareDefinition
from resource.software_definition import SoftwareDefinition as SoftwareDefinitionResource
from marshmallow.exceptions import ValidationError
from test_utils import *

class SoftwareDefinitionsTesting(testing.TestCase):
    def setUp(self):
        super(SoftwareDefinitionsTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                       dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(SoftwareDefinitionsTesting):
    def _getSoftwareExample(self):
        json_file = os.path.dirname(__file__) + \
                    "/examples/software-artifact-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    # def _getAuthorizationHeaders(self):
    #    return {"Authorization": "Basic bGNwOmd1YXJk"}

    def test_software_piece(self):
        software_dict = self._getSoftwareExample()
        software_schema = SoftwareDefinition(many=False)
        try:
            d = software_schema.load(software_dict)
            print(d)
            assert (True)
        except ValidationError as ve:
            print(ve)
            assert (False)

    def test_get_software(self):
        headers = getAuthorizationHeaders()

        SoftwareDefinitionResource.load_test_file()

        result = self.simulate_get("/software")
        assert (result.status == "401 Unauthorized")
        print(result)

        result = self.simulate_get("/software", headers=headers)
        assert (result.status == "200 OK")

        body = result.json
        assert (type(body) is list)
        for s in body:
            software_schema = SoftwareDefinition(many=False)
            try:
                software_schema.load(s)
                assert True
            except ValidationError as e:
                print(e)
                raise e

    def test_post_software(self):
        headers = getAuthorizationHeaders()
        software_dict = self._getSoftwareExample()

        try:
            # Test - Post
            resp = self.simulate_post("/software", headers=headers,
                                  body=json.dumps(software_dict))
            assert len(SoftwareDefinitionResource.data)==1
            assert SoftwareDefinitionResource.data[0]["id"] == software_dict["id"]
            assert resp.status_code == 201

            # Test - Update
            software_dict["name"]="MySQL Server"
            resp = self.simulate_post("/software", headers=headers,
                                      body=json.dumps(software_dict))
            assert len(SoftwareDefinitionResource.data)==1
            assert SoftwareDefinitionResource.data[0]["name"] == software_dict["name"]
            assert resp.status_code == 201

        except ValidationError as e:
            print(e)
            assert False




