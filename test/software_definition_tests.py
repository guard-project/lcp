from schema.software_definitions import SoftwareDefinition, ContainerSchema
from marshmallow.exceptions import ValidationError
from test_utils import *
from test.testbase import LCPTestBase
from marshmallow.exceptions import ValidationError

from schema.software_definitions import SoftwareDefinition, ContainerSchema
from test.testbase import LCPTestBase
from test_utils import *


class TestMyApp(LCPTestBase):
    def _getSoftwareExample(self):
        json_file = os.path.dirname(__file__) + \
                    "/examples/software-artifact-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    # def _getAuthorizationHeaders(self):
    #    return {"Authorization": "Basic bGNwOmd1YXJk"}

    def test_software_piece(self):
        software_dict = self._getSoftwareExample()
        software_schema = SoftwareDefinition(many=False)
        try:
            d = loadExampleFile("software-artifact-example.json")
            print(d)
            assert (True)
        except ValidationError as ve:
            print(ve)
            assert (False)

    def test_get_software(self):
        headers = getAuthorizationHeaders()
        example = loadExampleFile("software-artifact-example.json")

        result = self.simulate_get("/self/software", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        LCPConfig().setSoftware(example)
        result = self.simulate_get("/self/software", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert len(body) == 1

        for s in body:
            software_schema = SoftwareDefinition(many=False)
            try:
                software_schema.load(s)
                assert True
            except ValidationError as e:
                raise e


    def test_post_software(self):
        headers = getAuthorizationHeaders()
        software_dict = loadExampleFile("software-artifact-example.json")

        try:
            # Test - Post
            resp = self.simulate_post("/self/software", headers=headers,
                                  body=json.dumps(software_dict))
            self_software = LCPConfig().self_software
            assert len(self_software) == 1
            assert self_software[0]["id"] == software_dict["id"]
            assert resp.status_code == 201

            # Test - Update
            software_dict["product"]="MySQL Server"
            resp = self.simulate_post("/self/software", headers=headers,
                                      body=json.dumps(software_dict))
            assert len(self_software) == 1
            assert self_software[0]["product"] == software_dict["product"]
            assert resp.status_code == 201

            # Test - Unaceptable
            software_dict['mistake'] = "nas"
            resp = self.simulate_post("/self/software", headers=headers,
                                      body=json.dumps(software_dict))
            assert resp.status_code == 406

        except ValidationError as e:
            print(e)
            assert False


    def test_container_definitions(self):
        container_schema = ContainerSchema()
        dict_container = loadExampleFile("SoftwareInContainer.json")

        try:
            container_schema.validate(dict_container)
        except ValidationError:
            assert(False)

        dict_container['technology'] = 'InvalidOne'
        try:
            container_schema.validate(dict_container)
        except ValidationError:
            assert(True)


    def test_get_containers(self):
        headers = getAuthorizationHeaders()

        example = loadExampleFile("SoftwareInContainer.json")

        result = self.simulate_get("/self/container", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        LCPConfig().setContainers(example)
        result = self.simulate_get("/self/container", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert len(body) == 1

        for s in body:
            software_schema = ContainerSchema(many=False)
            try:
                software_schema.load(s)
                assert True
            except ValidationError as e:
                print(e)
                raise e


    def test_post_container(self):
        headers = getAuthorizationHeaders()
        container_dict = loadExampleFile("SoftwareInContainer.json")

        cs = ContainerSchema()

        try:
            cs.load(container_dict)
            # Test - Post
            resp = self.simulate_post("/self/container", headers=headers,
                                  body=json.dumps(container_dict))
            self_containers = LCPConfig().self_containers
            assert len(self_containers) == 1
            assert self_containers[0]["id"] == container_dict["id"]
            assert resp.status_code == 201

            # Test - Update
            container_dict["technology"] = "docker"
            resp = self.simulate_post("/self/container", headers=headers,
                                      body=json.dumps(container_dict))
            assert len(self_containers) == 1
            assert self_containers[0]["id"] == container_dict["id"]
            assert resp.status_code == 201

            # Test - Unaceptable
            container_dict['software'][0]['mistake'] = "nas"
            resp = self.simulate_post("/self/container", headers=headers,
                                      body=json.dumps(container_dict))
            assert resp.status_code == 406
        except ValidationError as e:
            print(e)
            assert False

