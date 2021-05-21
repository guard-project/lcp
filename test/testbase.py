from utils.log import Log
from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import title, version
from extra.lcp_config import LCPConfig
from extra.clients_starter import end_client_threads

class LCPTestBase(testing.TestCase):
    log = None

    def setUp(self):
        super(LCPTestBase, self).setUp()
        LCPConfig.__drop_it__("examples/LCPConfig.yaml")
        lcp = LCPConfig()
        lcp.reset()
        lcp.testing = True
        self.db = Arg_Reader.read()
        if LCPTestBase.log is None:
            Log.init(config="../"+self.db.log_config)
            LCPTestBase.log = Log.get('api')
        self.app = api(title=title, version=version)

    def tearDown(self) -> None:
        end_client_threads()

