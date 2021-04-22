from schema.security_functions import *
from schema.security_functions import AgentType
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

    def test_security_function(self):
        sf_dict = loadExampleFile("security-function-example.json")
        sf_schema = Agent(many=False)
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

        sf = Agent(many=False)
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
        sf = Agent()
        sf_dict['actions'] = agent_actions
        try:
            sf.validate(sf_dict)
        except ValidationError:
            assert False

    def testAgentTypesPost(self):
        at_dict = loadExampleFile("agent-type-example.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        schema_agent_type = AgentType()
        assert len(config.agent_types) == 0

        try:
            schema_agent_type.validate(at_dict)
            assert(True)
        except ValidationError as e:
            print(e)
            assert(False)

        body = json.dumps(at_dict)
        print(body)
        result = self.simulate_post("/agent_type", headers=headers,
                                    body=body)

        assert result.status_code == 201
        assert len(config.agent_types) == 1

    def testAgentTypeGet(self):
        at_dict = loadExampleFile("agent-type-example.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        schema_agent_type = AgentType()

        config.setAgentType(at_dict)

        assert len(config.agent_types) == 1
        result = self.simulate_get("/agent_type", headers=headers)

        assert result.status_code == 200
        body = result.json

        print(len(body))
        assert (type(body) is list)
        assert len(body) == 1
        assert body[0]['id'] == config.agent_types[0]["id"]
        assert body[0]['id'] == config.config['agent_types'][0]["id"]
