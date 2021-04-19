from extra.lcp_config import LCPConfig
from docstring import docstring
from resource.base import Base_Resource
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import VirtualServer as VirtualServerSchema
from schema.hardware_definitions import ExecutionEnvironment as ExcutionEnvironmentSchema
from lib.http import HTTP_Method
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED
from marshmallow import ValidationError
import json



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

       print(json.dumps(LCPConfig().lcp))
       resp.body = json.dumps(LCPConfig().lcp)

       payload = req.media if isinstance(req.media, list) else [req.media]
