from extra.lcp_config import LCPConfig
from docstring import docstring
from resource.base import Base_Resource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import ExecutionEnvironment as ExcutionEnvironmentSchema
from lib.http import HTTP_Method
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR
from marshmallow import ValidationError
from schema.filiation import InitialConfigurationSchema
import json
from extra.cb_client import CBClient, CBMessages, ToContextBrokerMessages

from extra.hw_helpers.host_info import HostInfoToLcpHelper


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
    tag = {'name': 'self',
           'description': 'Initial configuration for the LCP'}
    routes = '/self/configuration',

    @docstring(source="self/post.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = InitialConfigurationSchema(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media
        try:
            cfg = LCPConfig()
            ic_schema = InitialConfigurationSchema(many=False)
            ic_schema.load(payload)
            if cfg.exec_env_type is None:
                host_info = HostInfoToLcpHelper().js_info
                cfg.setDeployment(host_info)
            should_restart = cfg.setInitialConfiguration(payload)
            if should_restart:
                from extra import startup_client_threads
                startup_client_threads()
            elif 'context-broker' in payload:
                from extra import ThreadCB
                ThreadCB.send_cb_messages()
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            resp.status = HTTP_NOT_ACCEPTABLE


class SelfAutoConfig(Base_Resource):
    data = {}
    tag = {'name': 'self',
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

