from lib.lcp_config import LCPConfig
from docstring import docstring
from resource.base import Base_Resource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from lib.http import HTTP_Method
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from marshmallow import ValidationError
import json


__all__ = [
    'DescribeDeployment',
    'DescribeSelf'
]


class DescribeDeployment(Base_Resource):
    data = {}
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/self/deployment',

    def on_get(self, req, resp):
       resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})

       resp.body = json.dumps(LCPConfig().deployment)

    def on_post(self, req, resp):
        resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})
        payload = req.media
        try:
            bm_schema = BaremetalServerSchema(many=False)
            bm_schema.load(payload)
            LCPConfig().setDeployment(payload)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE
        LCPConfig().setDeployment(payload)


class DescribeSelf(Base_Resource):
    data = {}
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/self',

    def on_get(self, req, resp):
    # TODO: Organizar este codigo bien, con el esquema que corresponda!
       resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})
       resp.body = json.dumps(LCPConfig().lcp)

       payload = req.media if isinstance(req.media, list) else [req.media]
