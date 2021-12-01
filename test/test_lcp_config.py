from falcon import testing
from api import api
from reader.arg import ArgReader
from about import title, version
from extra.lcp_config import LCPConfig
import os
from utils.log import Log  # noqa: E402


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
        c = LCPConfig("examples/TestConfigFile.yaml")
        c.testing = True
        print(c.lcp)
        print(c.sons)
        print(c.getDataForRegisterOnCB())
        print("------------------------------------------")
        print(c.deployment)

