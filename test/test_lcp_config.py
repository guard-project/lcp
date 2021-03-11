from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version

from lib.lcp_config import LCPConfig

class SecurityFunctionDefinitionTesting(testing.TestCase):
    def setUp(self):
        super(SecurityFunctionDefinitionTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                       dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(SecurityFunctionDefinitionTesting):
    def test_load_file(self):
        c = LCPConfig()
        print(c.lcp)
        print(c.sons)
        print(c.getDataForRegisterOnCB())
        print("------------------------------------------")
        print(c.config['deployment'])
