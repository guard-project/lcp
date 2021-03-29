from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
import os
import json
from schema.security_functions import *
from resource.security_functions import SecurityFunction as SecurityFunctionResource
from resource.software_definition import SoftwareDefinition as SoftwareDefinitionResource
from marshmallow.exceptions import ValidationError
from test_utils import *

from lib.lcp_config import LCPConfig


class SecurityFunctionDefinitionTesting(testing.TestCase):
    def setUp(self):
        super(SecurityFunctionDefinitionTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                       dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(SecurityFunctionDefinitionTesting):
    def _getSecurityFucntionExample(self):
        json_file = os.path.dirname(__file__) + \
                    "/examples/security-function-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    def test_security_function(self):
        sf_dict = loadExampleFile("security-function-example.json")
        sf_schema = SecurityFunction(many=False)
        try:
            d = sf_schema.load(sf_dict)
            assert(True)
        except ValidationError as ve:
            print(ve)
            assert(False)

    def test_get_security_function(self):
        sf_dict = loadExampleFile("security-function-example.json")
        config = getLCPConfig()

        headers = getAuthorizationHeaders()
        config.dropAllAgents()

        result = self.simulate_get("/securityFunctions")
        assert(result.status_code == 401)

        result = self.simulate_get("/securityFunctions", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        config.setAgent(sf_dict)
        d = config.agents

        result = self.simulate_get("/securityFunctions", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 1
        assert body[0]['name'] == "VM Sensor Probe"


    def test_post_security_function(self):
        sf_dict = loadExampleFile("security-function-example.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        config.dropAllAgents()

        body = json.dumps(sf_dict)
        result = self.simulate_post("/securityFunctions", headers=headers,
                                    body=body)
        assert(result.status_code == 201)
        assert len(config.agents) == 1
        assert config.agents[0]["id"] == sf_dict["id"]

        sf_dict["vendor"] = "GUARD-Project.eu"
        body = json.dumps(sf_dict)
        result = self.simulate_post("/securityFunctions", headers=headers,
                                    body=body)
        assert(result.status_code == 201)
        assert len(config.agents) == 1
        assert config.agents[0]["vendor"] == sf_dict["vendor"]

    def testAgentParameters(self):
        sf_dict = loadExampleFile("security-function-example.json")
        ag_params = [
            {
                "name": "qemu_connect",
                "type": "string",
                "value": "qemu:///system",
                "description": "Quemu Connection Strings to extract data from Libvirt"
            },
            {
                "name": "elastik_search_url",
                "type": "string",
                "value": "http://admtools.lab.fiware.org:9200/",
                "description": "Elastik Search endpoint where to send Service's data"
            }
            ]
        sf_dict['parameters'] = ag_params
        agp = AgentParameter(many=True)
        try:
            agp.validate(ag_params)
        except ValidationError:
            assert False

        sf = SecurityFunction(many=False)
        try:
            sf.validate(sf_dict)
        except ValidationError:
            assert False

    def testAgentActions(self):
        agent_actions = [{
            "id": "start",
            "cmd": "sudo systemctl start goroku",
            "status": "started",
        },
        {
            "id": "stop",
            "cmd": "sudo systemctl stop goroku",
            "status": "stopped",
        }]
        sf_actions = AgentActionSchema()
        try:
            sf_actions.validate(agent_actions)
        except ValidationError:
            assert False

        sf_dict = loadExampleFile("security-function-example.json")
        sf = SecurityFunction()
        sf_dict['actions'] = agent_actions
        try:
            sf.validate(sf_dict)
        except ValidationError:
            assert False





