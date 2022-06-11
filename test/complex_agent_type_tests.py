from schema.security_functions import *
from schema.security_functions import AgentType, Agent as AgentSchema
from marshmallow.exceptions import ValidationError
from test_utils import *

from test.testbase import LCPTestBase
import traceback
from extra.cb_helpers.agent_instance_helper import AgentInstanceHelper


class TestMyApp(LCPTestBase):
    def test_security_function(self):
        agent_type_dict = loadExampleFile("pga_filter_agent_type.json")
        config = getLCPConfig()
        headers = getAuthorizationHeaders()
        body = json.dumps(agent_type_dict)

        # Post agent type 1
        result = self.simulate_post("/agent/type", headers=headers,
                                    body=json.dumps(agent_type_dict))
        assert(result.status_code == 201)

        # Post agent type 2
        agent_type_dict = loadExampleFile("bpfflowmon_agent_type.json")
        result = self.simulate_post("/agent/type", headers=headers,
                                    body=json.dumps(agent_type_dict))
        assert(result.status_code == 201)

        # Post agent type
        agent_type_dict = loadExampleFile("vdpi-guard_agent_type.json")
        result = self.simulate_post("/agent/type", headers=headers,
                                    body=json.dumps(agent_type_dict))
        assert(result.status_code == 201)

        # Post agent type
        agent_type_dict = loadExampleFile("nprobe_agent_type.json"),
        result = self.simulate_post("/agent/type", headers=headers,
                                    body=json.dumps(agent_type_dict))
        assert(result.status_code == 201)

        # Post agent type
        agent_type_dict = loadExampleFile("vuln-scanner_agent_type.json"),
        result = self.simulate_post("/agent/type", headers=headers,
                                    body=json.dumps(agent_type_dict))
        assert(result.status_code == 201)

        result = self.simulate_get("/poll", headers=headers)
        assert(result.status_code == 200)
        body = result.json
        # print(json.dumps(result.json))

        result = self.simulate_get("/poll", headers=headers)
        assert(result.status_code == 200)
        body = result.json
        # print(json.dumps(result.json))

        result = self.simulate_get("/poll", headers=headers)
        assert(result.status_code == 200)
        body = result.json

        for a in body['agentType']:
            print(json.dumps(a))
