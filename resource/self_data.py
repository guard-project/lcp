from extra.lcp_config import LCPConfig
from docstring import docstring
from resource.base import Base_Resource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import ExecutionEnvironment as ExcutionEnvironmentSchema
from lib.http import HTTP_Method
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR
from marshmallow import ValidationError
from schema.lcp_schemas import LCPDescription
import json

from extra.hw_helpers.host_info import HostInfoToLcpHelper
from extra.controller import LCPController

class DescribeDeployment(Base_Resource):
    tag = {'name': 'self',
           'description': 'This method does the initial configuration'}
    routes = '/self/deployment',

    @docstring(source="self/self_deployment.yaml")
    def on_get(self, req, resp):
       resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})

       lcp_config = LCPConfig()

       r = {"type": lcp_config.exec_env_type, "environment": lcp_config.deployment}

       resp.body = json.dumps(r)

    @docstring(source="BaremetalServer/PostBaremetalServerDeployment.yml")
    def on_post(self, req, resp):
        resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})
        payload = req.media
        try:
            cfg = LCPConfig()
            ee_schema = ExcutionEnvironmentSchema(many=False)
            ee_schema.load(payload)
            cfg.setDeployment(payload)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = json.dumps(e.messages)
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

        lcp = json.dumps(LCPConfig().lcp)
        if lcp == "null":
            resp.body = None
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = lcp
            payload = req.media if isinstance(req.media, list) else [req.media]


class InitialSelfConfiguration(Base_Resource):
    data = {}
    tag = {'name': 'self',
           'description': 'Initial configuration for the LCP'}
    routes = '/self/configuration',

    @docstring(source="self/post.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media
        try:
            controller = LCPController()
            ic_schema = LCPDescription(many=False)
            ic_schema.load(payload)
            res = controller.set_self_initial_configuration(payload)

            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = json.dumps(e.messages)
            resp.status = HTTP_NOT_ACCEPTABLE
