from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version

from schema.hardware_definitions import Disk, DiskPartition, \
    VirtualServer, BaremetalServer, LXCContainer
from test_utils import *
from test.testbase import LCPTestBase
from test.test_utils import loadExampleFile
from marshmallow import ValidationError


# class HardwareDefinitionsTesting(testing.TestCase):
#    def setUp(self):
#        super(HardwareDefinitionsTesting, self).setUp()
#        self.db = Arg_Reader.read()
#        self.app = api(title=title, version=version,
#                        dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(LCPTestBase):
    def _getTestingPartitionsHD2(self):
        partitionsHD2 = {"id": "2200328d-c1ac-4788-8690-c973bcae9985", "name": "mmcblk0p1", "size": 0, type: "ext4"}
        return partitionsHD2

    def _getTestingPartitionsHD1(self):
        partitionsHD1 = [{"id": "4AFF-2CFC", "name": "nvme0n1p1", "size": 0, "type": "vfat"},
             {"id": "247CD4AA7CD477CE", "name": "nvme0n1p3", "size": 0, "type":"ntfs"},
             {"id": "C6CCF4D7CCF4C32B", "name": "nvme0n1p4", "size": 0, "type": "ntfs"},
             {"id": "aa38a071-cde3-4e25-b2ab-df93a364e358", "name": "nvme0n1p5", "size": 0, type:"swap"},
             {"id": "d66769a4-039f-482b-a81f-8ceb8022e846", "name": "nvme0n1p6", "size": 0, type:"ext4"}]
        return partitionsHD1

    def _getTestingDiskHD1(self):
        partitionsHD1 = self._getTestingPartitionsHD1()
        disk = {
            "id": 'ac868a79-e642-4077-88cc-aabe5940e16f', "name": "nvme0n1",
            "size": 0, "model": 'KBG30ZMV512G TOSHIBA',
            "partitions": partitionsHD1
        }
        return disk

    def test_disk_definitions(self):
        dp = DiskPartition(many=False)
        dict_disk_partitions =self._getTestingPartitionsHD2()
        valid = dp.validate(dict_disk_partitions)
        assert(valid)

        dp = DiskPartition(many=False)
        dict_disk_partitions =self._getTestingPartitionsHD1()
        valid = dp.validate(dict_disk_partitions)
        assert(valid)

        disk_partition = dp.dumps(dict_disk_partitions)

        dsk = Disk()
        dict_disk = self._getTestingDiskHD1()
        valid = dsk.validate(dict_disk)
        assert(valid)
        disk = dsk.dumps(dict_disk) #disk es str!!
        print(disk)

    def test_various_things(self):
        baremetal_server = loadExampleFile("bare-metal-server-example.json")
        virtual_server = loadExampleFile("virtual-server-example.json")
        lxc_container = loadExampleFile("lxc-example.json")

        print("... Validate: lxc_container as VirtualServer")
        vs_schema = VirtualServer()
        try:
            vs_schema.load(lxc_container)
        except ValidationError as ve:
            print(ve)

        print("... Validate: lxc_container as BaremetalServer")
        bm_schema = BaremetalServer()
        try:
            bm_schema.load(lxc_container)
        except ValidationError as ve:
            print(ve)

        print("... Validate: lxc_container as LXCContainer")
        lxc_schema = LXCContainer()
        try:
            lxc_schema.load(lxc_container)
        except ValidationError as ve:
            print(ve)

        print("... Validate: BaremetalServer as LXC_container")
        try:
            lxc_schema.load(baremetal_server)
        except ValidationError as ve:
            print(ve)

        print("... Validate: BaremetalServer as VirtualServer")
        try:
            vs_schema.load(baremetal_server)
        except ValidationError as ve:
            print(ve)


        print("... Validate: VirtualServer as LXCOntainer")
        try:
            lxc_schema.load(VirtualServer)
        except ValidationError as ve:
            print(ve)

        print("... Validate: VirtualServer as Baremetar")
        try:
            bm_schema.load(virtual_server)
        except ValidationError as ve:
            print(ve)
