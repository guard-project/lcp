from schema.security_functions import SecurityFunction as SecurityFunctionSchema
from docstring import docstring
from resource.base import Base_Resource
from lib.http import HTTP_Method
import json
from marshmallow.exceptions import ValidationError
from falcon import HTTP_CREATED, HTTP_NOT_ACCEPTABLE
from lib.lcp_config import LCPConfig


class SecurityFunction(Base_Resource):
    tag = {'name': 'software',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/securityFunctions',

    def __init__(self):
        pass

    @docstring(source='SecurityFunctions/GetSecurityFunctions.yml')
    def on_get(self, req, resp):
        # resp_data, valid = SecurityFunctionSchema(method=HTTP_Method.GET) \
        #    .validate(data={})
        resp.body = json.dumps(LCPConfig().agents)

    @docstring(source='SecurityFunctions/PostSecurityFunctions.yml')
    def on_post(self, req, resp):
        # resp_data, valid = SecurityFunctionSchema(method=HTTP_Method.POST) \
        #    .validate(data={})

        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            sf_schema = SecurityFunctionSchema(many=True)
            d = sf_schema.load(payload)
            for e in payload:
                LCPConfig().setAgent(e)

            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE

