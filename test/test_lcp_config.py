from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import title, version
from extra.lcp_config import LCPConfig
import os

class SecurityFunctionDefinitionTesting(testing.TestCase):
    def setUp(self):
        super(SecurityFunctionDefinitionTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                       dev_username=self.db.dev_username, dev_password=self.db.dev_password)


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

