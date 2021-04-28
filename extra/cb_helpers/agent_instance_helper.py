import json
from extra.lcp_config import LCPConfig

TEST_FILE = "/home/jicg/GUARD/Development/Integration/lcp/test/examples/agent-type-example.json"


class AgentInstanceHelper:
    def __init__(self, agent, status):
        self.dict_data = None
        self.config = LCPConfig()
        try:
            self.exec_env_id = self.config.lcp['id']
            self.agent_catalog_id = agent['id']
            self.description = "Agent " + self.agent_catalog_id + " for LCP " + self.exec_env_id
        except TypeError:
            # No Agent has been defined
            return

        self.id = self.agent_catalog_id + "@" + self.exec_env_id
        self.status = status

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

    aih = AgentInstanceHelper(agent_data, "stopped")
    print(aih.dumps())
