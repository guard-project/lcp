from marshmallow.exceptions import ValidationError
from schema.software_definitions import SoftwareDefinition, ContainerSchema
from test.testbase import LCPTestBase
from test_utils import *
from schema.artifacts import ExternalStorageSchema, InteractsWithSchema

class TestMyApp(LCPTestBase):
    def __getInteractsWithData(self):
        d_storage = loadExampleFile("external_storage_examples.json")
        d_software = loadExampleFile("software-artifact-example.json")
        ess = ExternalStorageSchema()
        ess.load(d_storage, many=False)
        ess.validate(d_storage)
        esoft_schema = SoftwareDefinition()
        esoft_schema.load(d_software, many=False)
        esoft_schema.validate(d_software)

        d = {"externalStorage": [d_storage],
             "softwareArtifacts": [d_software]}
        return d

    def test_valid_artifact_types(self):
        try:
            d = self.__getInteractsWithData()
            interactions = InteractsWithSchema()
            interactions.load(d, many=False)
        except ValidationError as ve:
            assert False

    def test_post(self):
        d = self.__getInteractsWithData()
        headers = getAuthorizationHeaders()
        cfg = LCPConfig()

        result = self.simulate_post("/interactions", headers=headers,
                                    body=json.dumps(d))

        assert result.status_code == 201
        assert 'externalStorage' in cfg.interactions
        assert len(cfg.interactions['externalStorage']) == 1
        assert cfg.interactions['externalStorage'][0]['id'] == 'example:nfs:storage'
        assert 'softwareArtifacts' in cfg.interactions
        assert len(cfg.interactions['softwareArtifacts']) == 1
        assert cfg.interactions['softwareArtifacts'][0]['id'] == 'oracle:mysql:5.8.1.0.5ubuntu2'

    def test_get(self):
        d = self.__getInteractsWithData()
        headers = getAuthorizationHeaders()
        cfg = LCPConfig()

        result = self.simulate_get("/interactions", headers=headers)

        print("---------------------")
        print("Status Code:", result.status_code)
        print("---------------------")

        assert result.status_code == 200
        body = result.json
        assert type(body) is dict
        assert 'softwareArtifacts' in body
        assert 'externalStorage' in body

        assert len(body['softwareArtifacts']) == 0
        assert len(body['externalStorage']) == 0

        # Add some data and test:
        cfg.add_external_software_interaction(d['softwareArtifacts'])
        cfg.add_external_storage_interaction(d['externalStorage'])

        result = self.simulate_get("/interactions", headers=headers)
        body = result.json
        assert result.status_code == 200
        assert 'softwareArtifacts' in body
        assert 'externalStorage' in body
        assert len(body['softwareArtifacts']) == 1
        assert len(body['externalStorage']) == 1


