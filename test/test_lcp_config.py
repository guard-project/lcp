from falcon import testing
from api import api
from reader.arg import ArgReader
from about import title, version
from extra.lcp_config import LCPConfig
import os
from utils.log import Log  # noqa: E402
from test.test_utils import getLCPConfig, getAuthorizationHeaders

class SecurityFunctionDefinitionTesting(testing.TestCase):
    def setUp(self):
        super(SecurityFunctionDefinitionTesting, self).setUp()
        self.db = ArgReader.read()
        db = ArgReader.read()
        Log.init(config="../" + db.log_config)
        Log.get('api').success(f'Accept requests at {db.host}:{db.port}')
        self.app = api(title=title, version=version)


class TestMyApp(SecurityFunctionDefinitionTesting):
    def test_load_file(self):
        print(os.getcwd())
        # c = LCPConfig("examples/TestConfigFile.yaml")
        c = getLCPConfig()
        c.testing = True
        print(c.lcp)
        print(c.sons)
        print(c.getDataForRegisterOnCB())
        print("------------------------------------------")
        print(c.deployment)


class TestQueryConfiguration(SecurityFunctionDefinitionTesting):
    def test_load_file(self):
        c = LCPConfig("examples/TestConfigFileComplex.yaml")
        assert len(c.network_links) == 1
        assert c.network_links[0]['id'] == 'urn:lcp:guard-local-lcp-test-network-link'

        headers = getAuthorizationHeaders()
        result = self.simulate_get("/poll", headers=headers)

        ex_env = result.json['exec_env']
        assert len(ex_env['network_links']) == 1
        assert ex_env['network_links'][0]['id'] == 'urn:lcp:guard-local-lcp-test-network-link'


