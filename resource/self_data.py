from extra.lcp_config import LCPConfig
from docstring import docstring
from resource.base import Base_Resource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import VirtualServer as VirtualServerSchema
from schema.hardware_definitions import ExecutionEnvironment as ExcutionEnvironmentSchema
from lib.http import HTTP_Method
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR
from marshmallow import ValidationError
from schema.filiation import InitialConfigurationSchema
import json

from extra.hw_helpers.host_info import HostInfoToLcpHelper


class DescribeDeployment(Base_Resource):
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server where LCP is deployed.'}
    routes = '/self/deployment',

    @docstring(source="BaremetalServer/GetBaremetalServerDeployment.yml")
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

        lcp = json.dumps(LCPConfig().lcp)
        if lcp == "null":
            resp.body = None
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = lcp
            payload = req.media if isinstance(req.media, list) else [req.media]


class InitialSelfConfiguration(Base_Resource):
    data = {}
    tag = {'name': 'initial_configuration',
           'description': 'This method does the initial configuration'}
    routes = '/self/configuration',

    def on_post(self, req, resp):
        resp_Data, valid = InitialConfigurationSchema(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media
        try:
            cfg = LCPConfig()
            ic_schema = InitialConfigurationSchema(many=False)
            ic_schema.load(payload)
            should_restart = cfg.setInitialConfiguration(payload)
            if should_restart:
                from extra import startup_lcp_thread
                startup_lcp_thread()
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            resp.status = HTTP_NOT_ACCEPTABLE


class SelfAutoConfig(Base_Resource):
    data = {}
    tag = {'name': 'initial_configuration',
           'description': 'This method does the initial configuration'}
    routes = '/self/autoconfig'

    def on_post(self, req, resp):
        payload = req.media
        if payload is not None:
            resp.body = '{"error": "No payload expected"}'
            resp.status = HTTP_NOT_ACCEPTABLE

        #try:
        cfg = LCPConfig()
        host_info = HostInfoToLcpHelper().js_info
        cfg.setDeployment(host_info)
        # except Exception as e:
        #    print(e)
        #    resp.body = '{"error": "Could not autoconfigure"}'
        #    resp.status = HTTP_INTERNAL_SERVER_ERROR
