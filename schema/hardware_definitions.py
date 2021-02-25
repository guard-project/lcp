from marshmallow import fields, Schema, validate
from schema.base import Base_Schema
from utils.schema import List_or_One
import re

__all__ = [
    'Disk',
    'DiskPartition',
    'NetworkInterface',
    'BaremetalServer',
    'VirtualServer',
    'LXCContainer',
    'DockerContainer',
    'IPv4CIDR',
    'IPv6CIDR'
]

IPV6_RE = r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))/(12[0-8]|1[01][0-9]|[1-9][0-9]|[0-9])$"
IPV4_RE = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(/(3[0-2]|[0-2][0-9]|[0-9]))?$"
MACADDR_RE = r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"


class DiskPartition(Base_Schema):
    """Define a Disk partition schema"""
    size = fields.Float(required=True, example="314461424",
                        description="Partition Size in Kilo Bytes")
    type = fields.Str(required=False, example='ext4',
                      description="Partition type or Filesystem")
    name = fields.Str(required=True, example="nveme0n1p6",
                      description="Partition name in the OS")


class Disk(Base_Schema):
    """
    Hard Disk device Schema for one disk of the Hardware.
    """
    id = fields.Str(required=True, example="5db06770-8c64-4693-9724-ff318b02f897",
                    description="Disk UUID.")
    name = fields.Str(required=True, example='nvme0n1',
                      description="Disk Name in the OS")
    size = fields.Int(required=True, example="314461424",
                      description="Complete Disk Size in Kilo Bytes")
    model = fields.Str(required=False, example="KBG30ZMV512G TOSHIBA",
                       description="Disk Model/Vendor")
    diskPartitions = List_or_One(fields.Nested(DiskPartition, required=False,
                                               description="Disk Partitions for the Disk"))


class IPv4CIDR(fields.Str):
    def __init__(self):
        super().__init__(validate=validate.Regexp(re.compile(IPV4_RE)))
        self._field_cache = {}


class IPv6CIDR(fields.Str):
    def __init__(self):
        super().__init__(validate=validate.Regexp(re.compile(IPV6_RE)))
        self._field_cache = {}


class NetworkInterface(Base_Schema):
    """
    Description of a Network Interface.
    """
    id = fields.Str(required=True, example="d450f1ce-95a1-4c3d-9e01-6e37f3d0c584",
                    description="Network Card UUID.")
    name = fields.Str(required=True, example='enx503eaaddcbeb',
                      description="Network interface Name in the OS")
    mtu = fields.Int(required=True, example="1500",
                     description="Network Interface MTU value")
    state = fields.Str(required=True, example="UP",
                       description="Network Interface state in the OS")
    deviceType = fields.Str(required=False, example="ethernet",
                            description="Type of Network device")
    MacAddress = fields.Str(required=False, example="a2:bc:14:43:ff:43", name="MacAddress",
                            description="Network Interface's Mac Address",
                            validate=validate.Regexp(re.compile(MACADDR_RE)))
    IPv4Addresses = fields.List(IPv4CIDR, required=False,
                                description="List of CIDR for IPv4 values")
    IPv6Addresses = fields.List(IPv6CIDR, required=False,
                                description="List of CIDR for IPv6 values")


class BaremetalServer(Base_Schema):
    """
    BaremetalServer Description
    """
    id = fields.Str(required=True, example="ed5bd35a-7213-47a9-ae6e-76212e62a157",
                    description="Network Card UUID.")
    hostname = fields.Str(required=True, example='corporario.example.com',
                          description="Network interface Name in the OS")
    cpus = fields.Int(required=True, example="8",
                      description="CPU Cores in the Server")
    ram = fields.Int(required=True, example="8",
                     description="RAM installed in the Server in Megabytes")
    operatingSystem = fields.Str(required=True, example='Ubuntu Linux 20.04.2 LTS',
                                 description="Network interface Name in the OS")
    networkInterfaces = List_or_One(fields.Nested(NetworkInterface), required=False,
                                    description="List of Network Interfaces in the host")
    diskDevices = List_or_One(fields.Nested(Disk, required=False,
                                            description="Disks installed in the Server"))


class VirtualServer(BaremetalServer):
    hypervisor = fields.Str(required=True, example='KVM',
                            description="Hypervisor name/technology")
    cloud_id = fields.Str(required=False, example="a4518fe5-9da9-43a5-8bc6-1433e28935f1",
                          description="Cloud ID -- Maybe None if somehow hosted")
    host_id = fields.Str(required=False, example="39f1f5e0-7aaa-4dd7-8e0e-8524cddb7a9c",
                         description="ID of underlying Baremetal Server")


class DockerContainer(Base_Schema):
    id = fields.Str(required=True, example="413216e3-169f-4638-830e-ef0607732fde",
                    description="Id of the Docker Container.")
    hostname = fields.Str(required=True, example='lcpdocker',
                          description="Docker name")
    host_id = fields.Str(required=False, example="e501d0d8-49bf-4db3-83ba-37c8cbdac6ba",
                         description="ID of underlying Baremetal, LXC or Virtual Server")
    software_id = fields.Str(required=False, example="82cd4399-1d95-4d67-831f-5724c47e577a",
                         description="Software Installed in Docker, if declared")


class LXCContainer(Base_Schema):
    id = fields.Str(required=True, example="bf9aff0c-6185-4b9f-8d39-c5f8e1b522e9",
                    description="Id of the LXC Container.")
    hostname = fields.Str(required=True, example='lxc_kafka',
                          description="LXC's name for the underlying example")
    operatingSystem = fields.Str(required=True, example='Ubuntu Linux 20.04.2 LTS',
                                 description="Emulated OS in the container")
    networkInterfaces = List_or_One(fields.Nested(NetworkInterface), required=False,
                                    description="List of Network Interfaces in the lxc container")
    host_id = fields.Str(required=False, example="39f1f5e0-7aaa-4dd7-8e0e-8524cddb7a9c",
                         description="ID of underlying Baremetal or Virtual Server")
