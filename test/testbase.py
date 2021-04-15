from utils.log import Log
from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import title, version
from extra.lcp_config import LCPConfig

class LCPTestBase(testing.TestCase):
    log = None

    def setUp(self):
        super(LCPTestBase, self).setUp()
        lcp = LCPConfig("examples/LCPConfig.yaml")
        lcp.reset()
        lcp.testing = True
        self.db = Arg_Reader.read()
        if LCPTestBase.log is None:
            Log.init(config="../"+self.db.log_config)
            LCPTestBase.log = Log.get('api')
        self.app = api(title=title, version=version)

