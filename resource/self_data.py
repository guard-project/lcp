from extra.lcp_config import LCPConfig
from docstring import docstring
from resource.base import BaseResource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import ExecutionEnvironment
from lib.http import HTTPMethod
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR
from marshmallow import ValidationError
from schema.lcp_schemas import LCPDescription
import json
from extra.hw_helpers.host_info import HostInfoToLcpHelper
from extra.controller import LCPController
from extra.cb_helpers.security_context_helper import SecurityContextHelper
from resource.lcp_resources import ParentLCPIdentification


class DescribeDeployment(BaseResource):
    tag = {'name': 'self',
           'description': 'This method does the initial configuration'}
    routes = '/self/deployment',

    @docstring(source="self/self_deployment.yaml")
    def on_get(self, req, resp):
       lcp_config = LCPConfig()

       r = {"executionType": lcp_config.exec_env_type, "environment": lcp_config.deployment}

       resp.body = json.dumps(r)

    @docstring(source="self/post_self_deployment.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = ExecutionEnvironment(method=HTTPMethod.GET) \
            .validate(req.media)
        payload = req.media
        try:
            cfg = LCPConfig()
            ee_schema = ExecutionEnvironment(many=False)
            ee_schema.load(payload)
            cfg.setDeployment(payload)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = json.dumps(e.messages)
            req.status = HTTP_NOT_ACCEPTABLE


class DescribeSelf(BaseResource):
    data = {}
    tag = {'name': 'self',
           'description': 'Returns description of self LCP.'}
    routes = '/self',


    @docstring(source="self/get.yaml")
    def on_get(self, req, resp):
        # TODO: Organizar este codigo bien, con el esquema que corresponda!
        resp_Data, valid = BaremetalServerSchema(method=HTTPMethod.GET) \
            .validate(data={})

        lcp = json.dumps(LCPConfig().lcp)
        if lcp == "null":
            resp.body = None
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = lcp
            payload = req.media if isinstance(req.media, list) else [req.media]


class InitialSelfConfiguration(BaseResource):
    data = {}
    tag = {'name': 'self',
           'description': 'Initial configuration for the LCP'}
    routes = '/self/configuration',

    @docstring(source="self/post.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTPMethod.POST) \
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

    def on_delete(self, req, resp):
        LCPConfig().reset()
        ParentLCPIdentification.notifed = []
        LCPController().reset()

    def on_get(self, req, resp):
        lcp = json.dumps(LCPConfig().lcp)
        if lcp == "null":
            resp.body = None
            resp.status = HTTP_NOT_FOUND
        else:
            helper = SecurityContextHelper(LCPConfig())
            helper.getData()
            data = helper.security_context

            nd = {"lcp": data['exec_env']['lcp']}
            nd['enabled'] = "yes"
            nd['hostname'] = data['exec_env']['hostname']
            nd['type_id'] = data['exec_env']['type_id']
            nd['description'] = data['exec_env']['description']
            nd['id'] = data['exec_env']['id']

            if 'sons' in nd['lcp']:
                nd['lcp'].pop('sons')
            if 'father' in nd['lcp']:
                nd['lcp'].pop('father')
            resp.body = json.dumps(nd)

