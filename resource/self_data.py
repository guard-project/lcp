from lib.lcp_config import LCPConfig
from docstring import docstring
from resource.base import Base_Resource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import VirtualServer as VirtualServerSchema
from lib.http import HTTP_Method
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from marshmallow import ValidationError
import json


__all__ = [
    'DescribeDeploymentBareMetal',
    'DescribeDeploymentVM',
    'DescribeSelf'
]


class DescribeDeploymentBareMetal(Base_Resource):
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server where LCP is deployed.'}
    routes = '/self/deployment/bare-metal',

    @docstring(source="BaremetalServer/GetBaremetalServerDeployment.yml")
    def on_get(self, req, resp):
       resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})

       resp.body = json.dumps(LCPConfig().deployment)

    @docstring(source="BaremetalServer/PostBaremetalServerDeployment.yml")
    def on_post(self, req, resp):
        resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})
        payload = req.media
        try:
            cfg = LCPConfig()
            bm_schema = BaremetalServerSchema(many=False)
            bm_schema.load(payload)
            cfg.type = "bare-metal"
            cfg.setDeployment(payload)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE


class DescribeDeploymentVM(Base_Resource):
    tag = {'name': 'hardware',
           'description': 'Returns description of a Virtual Server where LCP is deployed'}
    routes = '/self/deployment/vm',

    @docstring(source="VirtualServer/GetVirtualServerDeployment.yml")
    def on_get(self, req, resp):
       resp_Data, valid = VirtualServerSchema(method=HTTP_Method.GET) \
            .validate(data={})

       resp.body = json.dumps(LCPConfig().deployment)

    @docstring(source="VirtualServer/PostVirtualServerDeployment.yml")
    def on_post(self, req, resp):
        resp_Data, valid = VirtualServerSchema(method=HTTP_Method.GET) \
            .validate(data={})
        payload = req.media
        try:
            cfg = LCPConfig()
            bm_schema = VirtualServerSchema(many=False)
            bm_schema.load(payload)
            cfg.type = "vm"
            cfg.setDeployment(payload)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE


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
