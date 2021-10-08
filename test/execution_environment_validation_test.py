from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import VirtualServer, ExecutionEnvironment
from test_utils import *
from test.testbase import LCPTestBase
from marshmallow.exceptions import ValidationError

from schema.hardware_definitions import VirtualServer, ExecutionEnvironment, LXCContainer, BaremetalServer
from test.testbase import LCPTestBase
from test_utils import *


class TestMyApp(LCPTestBase):
    def setUp(self):
        super().setUp()
        self.v_server_dict = loadExampleFile("virtual-server-example.json")
        self.bm_server_dict = loadExampleFile("bare-metal-server-example.json")
        self.lxc_container_dict = loadExampleFile("lxc-example.json")
        self.docker_container_dict = loadExampleFile("docker-container-example.json")

    def test_crossed_castings(self):
        bm_schema = BaremetalServer()
        vs_schema = VirtualServer()
        lxc_schema = LXCContainer()

        try:
            lxc_schema.load(self.v_server_dict)
        except ValidationError as ve:
            print(ve.messages)

        try:
            lxc_schema.load(self.lxc_container_dict)
            print("OK!!")
        except ValidationError as ve:
            print(ve.messages)
            assert False

    def test_execution_environment(self):
        """
        Test loading different cases of execution environments and its loading and validation.

        :return:
        """

        # Test for VirtualServer Schema type
        virtual_server_schema = VirtualServer()
        ee_type = "vm"

        data = {"executionType": ee_type, "environment": self.v_server_dict}

        ee_schema = ExecutionEnvironment()

        try:
            ee_schema.load(data)
        except ValidationError:
            assert True

        ee_schema = ExecutionEnvironment()
        try:
            ee_schema.load(data)
        except ValidationError:
            assert False

        # Test for validation of bare-metal server type declaring a VirtualServer -
        ee_schema = ExecutionEnvironment()
        data = {"executionType": ee_type, "environment": self.bm_server_dict}
        try:
            d, ok = ee_schema.load(data)
            print("ee_schema ", d)
            print("ok ", ok)
        except ValidationError as e:
            print(e.messages)
            assert True
