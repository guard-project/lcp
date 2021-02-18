from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version

from schema.hardware_definitions import NetworkInterface, IPv4CIDR, IPv6CIDR, IPV4_RE
import re

class NetworkDefinitionsTesting(testing.TestCase):
    def setUp(self):
        super(NetworkDefinitionsTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                        dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(NetworkDefinitionsTesting):
    def _getTestingNetwork(self):
        net_interface = {
            "id": "NetworkInterface1",
            "name": "eth0",
            "MacAddress": "00:16:3e:00:00:00",
            "state": "UP",
            "mtu": 1500,
            "IPv4Addresses": ["192.168.0.16/24", "127.0.0.3/8"],
            "IPv6Addresses": ["fe80::8f3b:1216:853b:7368/128"]
        }
        return net_interface


    def test_disk_definitions(self):
        ni = NetworkInterface(many=False)
        dict_network_interface=self._getTestingNetwork()
        d = ni.load(dict_network_interface)
        valid = ni.validate(dict_network_interface)
        assert(valid[1])




