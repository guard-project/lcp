from json import dumps
from pathlib import Path
from resource import tags as rc_tags

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_apispec import FalconPlugin

from utils.string import is_str


class Spec:
    def __init__(self, api, title, version):
        schema_name_resolver = self.__schema_name_resolver
        self.obj = APISpec(title=title, version=version, openapi_version='2.0',
                           produces=['application/json'],
                           consumes=['application/json'],
                           tags=rc_tags,
                           plugins=[FalconPlugin(api),
                                    MarshmallowPlugin(schema_name_resolver)])

    def get(self):
        return self.obj

    def write(self):
        path = Path(__file__).parent / '../swagger/schema.yaml'
        with path.open('w') as file:
            file.write(self.obj.to_yaml())
        path = Path(__file__).parent / '../swagger/schema.json'
        with path.open('w') as file:
            file.write(dumps(self.obj.to_dict(), indent=2))

    @staticmethod
    def __schema_name_resolver(schema):
        ref = schema if is_str(schema) else schema.__class__.__name__
        return ref.replace('_Schema', '')
