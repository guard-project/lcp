import json
from extra.lcp_config import LCPConfig
import traceback

TEST_FILE = "/home/jicg/GUARD/Development/Integration/lcp/test/examples/agent-type-example.json"


class AgentInstanceHelper:
    def __init__(self, agent):
        self.dict_data = None
        self.config = LCPConfig()
        try:
            self.exec_env_id = self.config.lcp['id']
            self.agent_catalog_id = agent['type']
            self.description = "Agent " + self.agent_catalog_id + " for LCP " + self.exec_env_id
        except TypeError as e:
            traceback.print_exc()
            return

        self.id = agent['id']
        self.status = agent['status']

        self.dict_data = {
            "status": self.status,
            "description": self.description,
            "agent_catalog_id": self.agent_catalog_id,
            "exec_env_id": self.exec_env_id,
            "id": self.id
        }


    def dumps(self):
        if self.dict_data is None:
            return ""
        return json.dumps(self.dict_data)


if __name__ == "__main__":
    with open(TEST_FILE) as f:
        d = f.read()
    agent_data = json.loads(d)

    aih = AgentInstanceHelper(agent_data)
    print(aih.dumps())
