from resource.base import Base_Resource
from docstring import docstring
from schema.software_definitions import SoftwareDefinition as SoftwareDefinitionSchema
from lib.http import HTTP_Method
from marshmallow.exceptions import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
import json
import os

__all__ = [
    'SoftwareDefinition'
]


class SoftwareDefinition(Base_Resource):
    data = []
    tag = {'name': 'software',
           'description': 'Returns the description of software installed'}
    routes = '/software'

    def __init__(self):
        pass

    @classmethod
    def load_test_file(self):
        json_file = os.path.dirname(__file__) + \
            "/../test/examples/software-artifact-example.json"
        with open(json_file) as f:
            file_data = f.read()
        SoftwareDefinition.data.append(json.loads(file_data))

    @classmethod
    def update_data(cls, elem):
        updated = False
        for i in range(0, len(SoftwareDefinition.data)):
            if SoftwareDefinition.data[i]["id"] == elem["id"]:
                updated = True
                SoftwareDefinition.data[i] = elem
        if not updated:
            SoftwareDefinition.data.append(elem)

    @docstring(source="Software/GetSoftware.yml")
    def on_get(self, req, resp):
        resp_data, valid = SoftwareDefinitionSchema(method=HTTP_Method.GET) \
            .validate(data={})

        resp.body = json.dumps(SoftwareDefinition.data)

    @docstring(source="Software/PostSoftware.yml")
    def on_post(self, req, resp):
        resp_data, valid = SoftwareDefinitionSchema(method=HTTP_Method.POST) \
            .validate(data={})

        payload = req.media
        try:
            many = isinstance(payload, list)
            if not many:
                payload = [payload]
            software_schema = SoftwareDefinitionSchema(many=True)
            resp.status = HTTP_CREATED

            for e in payload:
                SoftwareDefinition.update_data(e)

        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
