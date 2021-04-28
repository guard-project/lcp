from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import VirtualServer, Disk, DiskPartition, ExecutionEnvironment
from resource.hardware_definitions import VirtualServer as VirtualServerResource
from schema.hardware_definitions import LXCContainer
import json
import os
from test_utils import *
from test.testbase import LCPTestBase
from schema.hardware_definitions import  ExecutionEnvironment

class TestMyApp(LCPTestBase):
    def test_post_execenv_baremental(self):
        bm_server_dict = loadExampleFile("bare-metal-server-example.json")
        headers = {"content-type": "application/json"}
        data = {"type": "bare-metal", "environment": bm_server_dict}
        lcp_config = getLCPConfig()

        ExecutionEnvironment.load(self, data)

        print(json.dumps(data))
        result = self.simulate_post("/self/deployment", headers=headers,
                                    body=json.dumps(data))
        print(result.status_code)
        assert result.status_code == 201

        assert lcp_config.exec_env_type == "bare-metal"
        print(lcp_config.deployment)
        assert lcp_config.deployment['id'] == bm_server_dict['id']
        assert lcp_config.config['deployment']['id'] == bm_server_dict['id']
        assert lcp_config.config['type'] == 'bare-metal'
        assert lcp_config.exec_env_type == 'bare-metal'

    def test_post_execenv_virtual_server(self):
        v_server_dict = loadExampleFile("virtual-server-example.json")
        headers = {"content-type": "application/json"}
        data = {"type": "vm", "environment": v_server_dict}
        lcp_config = getLCPConfig()
        vs = VirtualServer()
        vs.load(v_server_dict)
        ExecutionEnvironment.load(self, data)

        print(json.dumps(data))
        result = self.simulate_post("/self/deployment", headers=headers,
                                    body=json.dumps(data))
        print(result.status_code)
        assert result.status_code == 201

        assert lcp_config.exec_env_type == "vm"
        print(lcp_config.deployment)
        assert lcp_config.deployment['id'] == v_server_dict['id']
        assert lcp_config.config['deployment']['id'] == v_server_dict['id']
        assert lcp_config.config['type'] == 'vm'
        assert lcp_config.exec_env_type == 'vm'

    def test_post_execenv_lxc(self):
        lxc_server_dict = loadExampleFile("lxc-example.json")
        headers = {"content-type": "application/json"}
        data = {"type": "container-lxc", "environment": lxc_server_dict}
        lcp_config = getLCPConfig()
        lxc_s = LXCContainer()
        ee_schema = ExecutionEnvironment()

        lxc_s.load(lxc_server_dict)
        ee_schema.load(data)

        result = self.simulate_post("/self/deployment", headers=headers,
                                    body=json.dumps(data))
        print(result.status_code)
        assert result.status_code == 201

        assert lcp_config.exec_env_type == "container-lxc"
        print(lcp_config.deployment)
        assert lcp_config.deployment['id'] == lxc_server_dict['id']
        assert lcp_config.config['deployment']['id'] == lxc_server_dict['id']
        assert lcp_config.config['type'] == 'container-lxc'
        assert lcp_config.exec_env_type == 'container-lxc'

    def test_get_exec_env(self):
        lcp_config = getLCPConfig()
        print("Exec_env: ", lcp_config.exec_env_type)
        print("Exec_env: ", lcp_config.config['type'])
        assert lcp_config.exec_env_type == 'bare-metal'

