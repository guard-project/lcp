from schema.hardware_definitions import NetworkInterface, IPv4CIDR, IPv6CIDR, IPV4_RE
import re
from test.testbase import LCPTestBase


class TestMyApp(LCPTestBase):
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




