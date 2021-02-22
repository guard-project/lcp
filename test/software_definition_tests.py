from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
import os
import json
from schema.software_definitions import SoftwareDefinition
from marshmallow.exceptions import ValidationError


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

    def _getAuthorizationHeaders(self):
        return {"Authorization": "Basic bGNwOmd1YXJk"}

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
        headers = self._getAuthorizationHeaders()

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
                assert False
