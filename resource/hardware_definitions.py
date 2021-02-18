from docstring import docstring
from resource.base import Base_Resource
from schema.filiation import LCPSonDescription
from marshmallow import ValidationError
from schema.response import Created_Response
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from utils.sequence import is_list, wrap
from lib.http import HTTP_Method
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
import json
import os

__all__ = [
    'BaremetalServer'
]


class BaremetalServer(Base_Resource):
    data = {}
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/baremetal',

    def __init__(self):
        file = os.path.dirname(
            __file__) + "/../test/examples/bare-metal-server-example.json"
        with open(file) as f:
            BaremetalServer.data = json.loads(f.read())

    @docstring(source='BaremetalServer/GetBaremetalServer.yml')
    def on_get(self, req, resp):
        resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
        .validate(data={})

        resp.body = json.dumps(BaremetalServer.data)
