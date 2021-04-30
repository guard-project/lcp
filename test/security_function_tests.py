from schema.security_functions import *
from schema.security_functions import AgentType, Agent as AgentSchema
from marshmallow.exceptions import ValidationError
from test_utils import *

from test.testbase import LCPTestBase
import traceback
from extra.cb_helpers.agent_instance_helper import AgentInstanceHelper


class TestMyApp(LCPTestBase):
    def test_security_function(self):
        sf_dict = loadExampleFile("security-function-example.json")
        sf_schema = AgentSchema(many=False)
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

        result = self.simulate_get("/agent/instance", headers=headers)
        print(result.status)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        config.setAgent(sf_dict)
        d = config.agents

        result = self.simulate_get("/agent/instance", headers=headers)
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
        result = self.simulate_post("/agent/instance", headers=headers,
                                    body=body)
        assert(result.status_code == 201)
        assert len(config.agents) == 1
        assert config.agents[0]["id"] == sf_dict["id"]

        sf_dict["vendor"] = "GUARD-Project.eu"
        body = json.dumps(sf_dict)
        result = self.simulate_post("/agent/instance", headers=headers,
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
        sf_actions = AgentActionSchema(many=True)
        try:
            sf_actions.load(agent_actions)
        except ValidationError as e:
            traceback.print_exc(e)
            assert False

        sf_dict = loadExampleFile("security-function-example.json")
        sf = Agent()
        try:
            sf.load(sf_dict)
        except ValidationError as e:
            traceback.print_exc(e)
            assert False

    def testAgentTypesPost(self):
        at_dict = loadExampleFile("agent-type-example.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        schema_agent_type = AgentType(many=True)
        assert len(config.agent_types) == 0

        try:
            schema_agent_type.validate([at_dict])
            assert(True)
        except ValidationError as e:
            print(e)
            assert(False)

        body = json.dumps(at_dict)
        result = self.simulate_post("/agent/type", headers=headers,
                                    body=body)

        assert result.status_code == 201
        assert len(config.agent_types) == 1

    def testAgentTypeFileContent(self):
        at_dict = loadExampleFile("agent-type-example.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        schema_agent_type = AgentType(many=True)
        try:
            schema_agent_type.load([at_dict])
        except ValidationError as e:
            print(e.messages)

    def testAgentTypeGet(self):
        at_dict = loadExampleFile("agent-type-example.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        schema_agent_type = AgentType()

        config.setAgentType(at_dict)

        assert len(config.agent_types) == 1
        result = self.simulate_get("/agent/type", headers=headers)

        assert result.status_code == 200
        body = result.json

        assert (type(body) is list)
        assert len(body) == 1
        assert body[0]['id'] == config.agent_types[0]["id"]
        assert body[0]['id'] == config.config['agent_types'][0]["id"]

    def testAgentTypeExample(self):
        at_dict = loadExampleFile("agent-type-example.json")
        config = getLCPConfig()

        schema_agent_type = AgentType()
        schema_agent_type.load(at_dict)

        a_dict = loadExampleFile("agent-instance-example-for-lcp.json")
        schema_agent = Agent()
        schema_agent.load(a_dict)

        aih = AgentInstanceHelper(a_dict)
        print(aih.dumps())
