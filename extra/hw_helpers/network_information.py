from enum import IntEnum
import socket
import struct
from pathlib import Path

from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces

from ipaddress import IPv4Network, IPv6Network


# /sys/class/net -- Explanation
# https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-net


class ProcNetRouteFields(IntEnum):
    Iface = 0
    Destination = 1
    Gateway = 2
    Flags = 3
    RefCnt = 4
    Use = 5
    Metric = 6
    Mask = 7
    MTU = 8
    Window = 9
    IRTT = 10


class NetworkInterfacesInfo:
    def __init__(self):
        self.ifaces = netifaces.interfaces()
        self.ifaz, self.gw = self.get_default_gateway_linux()

        self.mac = self.get_mac_address(self.ifaz)
        self.ipv4 = self.get_network_ipv4(self.ifaz)
        self.ipv6 = self.get_network_ipv6(self.ifaz)
        self.mtu = self.get_mtu(self.ifaz)
        self.ifaz_type = self.get_card_type(self.ifaz)
        self.state = self.get_interface_state(self.ifaz)

    def net_info(self):
        d = {}
        network_interfaces = []
        d['networkInterfaces'] = network_interfaces

        ni = {}
        ni['IPv4Addresses'] = self.ipv4
        ni['IPv6Addresses'] = self.ipv6
        ni['MacAddress'] = self.mac
        ni['deviceType'] = self.ifaz_type
        ni['name'] = self.ifaz
        ni['id'] = "nwiface:" + self.ifaz
        ni['mtu'] = self.mtu

        network_interfaces.append(ni)

        return d

    def get_default_gateway_linux(self):
        with open("/proc/net/route") as fr:
            for line in fr:
                fields = line.strip().split()
                if fields[ProcNetRouteFields.Destination] != '00000000' or \
                        not int(fields[ProcNetRouteFields.Flags], 16) & 2:
                    continue

                gw = socket.inet_ntoa(struct.pack("=L", int(fields[ProcNetRouteFields.Destination], 16)))
                ifaz = fields[ProcNetRouteFields.Iface]

                return ifaz, gw

    def get_network_ipv4(self, ifaz: str):
        if ifaz not in self.ifaces:
            return None

        ipv4 = []
        for ipv4_ifaz in netifaces.ifaddresses(ifaz)[AF_INET]:
            mask = "0.0.0.0/" + ipv4_ifaz['netmask']
            bits = IPv4Network(mask).prefixlen

            ipv4.append(ipv4_ifaz['addr'] + "/" + str(bits))

        return ipv4

    def get_network_ipv6(self, ifaz: str):
        if ifaz not in self.ifaces:
            return None

        ipv6 = []
        try:
            for ipv6_ifaz in netifaces.ifaddresses(ifaz)[AF_INET6]:
                mask = ipv6_ifaz['netmask']
                bits = IPv6Network(mask).prefixlen

                ipv6.append(ipv6_ifaz['addr'].split('%')[0] + "/" + str(bits))
        except KeyError:
            pass

        return ipv6

    def get_mac_address(self, ifaz: str):
        if ifaz not in self.ifaces:
            return None

        return netifaces.ifaddresses(ifaz)[AF_LINK][0]['addr']

    def get_mtu(self, ifaz: str):
        if ifaz not in self.ifaces:
            return 0
        file = "/sys/class/net/" + ifaz + "/mtu"
        with open(file) as f:
            str_mtu = f.read()
        return int(str_mtu)

    def get_card_type(self, ifaz: str):
        if ifaz not in self.ifaces:
            return 0

        if ifaz.startswith("lo"):
            return "loopback"

        file = "/sys/class/net/" + ifaz + "/py80211"
        if Path(file).is_dir():
            return 'wifi'

        file = "/sys/class/net/" + ifaz + "/bridge"
        if Path(file).is_dir():
            return 'bridge'

        file = "/sys/class/net/" + ifaz + "/brport"
        if Path(file).is_dir():
            return 'brport'

        file = "/sys/class/net/" + ifaz + "/bonding"
        if Path(file).is_dir():
            return 'bond'

        return "ethernet"

    def get_interface_state(self, ifaz: str):
        if ifaz not in self.ifaces:
            return "down"

        file = "/sys/class/net/" + ifaz + "/carrier"
        with open(file) as f:
            carrier = f.read()

        if carrier == "0":
            return "down"
        return "up"
