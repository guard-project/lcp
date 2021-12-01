from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import BaremetalServer, Disk, DiskPartition
from resource.hardware_definitions import BaremetalServer as BaremetalServerResource
from test_utils import *
from test.testbase import LCPTestBase


class TestMyApp(LCPTestBase):
    def _getBaremetalServer(self):
        json_file = os.path.dirname(
            __file__) + "/examples/bare-metal-server-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    def test_baremetal_server(self):
        server = loadExampleFile("bare-metal-server-example.json")
        bm_server = BaremetalServer(many=False)
        try:
            d = bm_server.load(server)
            print(d)
            assert (True)
        except ValidationError as ve:
            print(ve)
            assert (False)

        """ dict_disk_partitions =self._getTestingPartitionsHD2()
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
        print(disk)"""

    def test_chk(self):
        # bm_server = self._getBaremetalServer()
        bm_server = loadExampleFile("bare-metal-server-example.json")
        diskDevices = bm_server['diskDevices']

        d = {"size": 143.24, "type": "ext4", "name": "/dev/nvme0n1p6"}
        print("Load: ", d)
        # , "size": 0.26, "type": "ext4"}
        DiskPartition().load(d)

        for device in diskDevices:
            try:
                dsk = Disk()
                dsk.load(device)
                print("OK: ", device)
            except ValidationError as ve:
                print("DEV: ", device['diskPartitions'][0])
                DiskPartition().load(device['diskPartitions'][0])
                print(device)
                print(ve)

    def test_get_baremetal_server(self):
        bm_server = loadExampleFile("bare-metal-server-example.json")
        headers = getAuthorizationHeaders()
        BaremetalServerResource.data = []

        # result = self.simulate_get("/baremetal", headers=headers)
        result = self.simulate_get("/self/deployment", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (body['environment'] == {})

        cfg = LCPConfig()
        data = {"executionType": "bare-metal", "environment": bm_server}
        cfg.setDeployment(data)

        result = self.simulate_get("/self/deployment", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert body['executionType'] == 'bare-metal'
        assert body['environment'] == bm_server

        print(json.dumps(bm_server))
        print()

        try:
            bm_schema = BaremetalServer(many=False)
            bm_schema.load(body['environment'])
            assert True
        except ValidationError as ve:
            print(ve)
            assert False

    def test_post_baremetal_server(self):
        bm_server_dict = loadExampleFile("bare-metal-server-example.json")
        headers = getAuthorizationHeaders()

        data = {"executionType": "bare-metal", "environment": bm_server_dict}

        body = json.dumps(data)
        result = self.simulate_post("/self/deployment", headers=headers,
                                    body=body)
        assert result.status_code == 201
