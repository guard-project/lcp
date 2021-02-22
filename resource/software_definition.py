from resource.base import Base_Resource
from docstring import docstring
from schema.software_definitions import SoftwareDefinition as SoftwareDefinitionSchema
from lib.http import HTTP_Method
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
        json_file = os.path.dirname(__file__) + \
            "/../test/examples/software-artifact-example.json"
        with open(json_file) as f:
            file_data = f.read()
        SoftwareDefinition.data.append(json.loads(file_data))


    @docstring(source="Software/GetSoftware.yml")
    def on_get(self, req, resp):
        resp_data, valid = SoftwareDefinitionSchema(method=HTTP_Method.GET) \
          .validate(data={})

        resp.body = json.dumps(SoftwareDefinition.data)
