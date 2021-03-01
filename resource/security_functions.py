from schema.security_functions import SecurityFunction as SecurityFunctionSchema
from docstring import docstring
from resource.base import Base_Resource
from lib.http import HTTP_Method
import json
from marshmallow.exceptions import ValidationError
from falcon import HTTP_CREATED, HTTP_NOT_ACCEPTABLE


class SecurityFunction(Base_Resource):
    data = []
    tag = {'name': 'software',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/securityFunctions',

    def __init__(self):
        pass

    @classmethod
    def update_data(cls, elem):
        updated = False
        for i in range(0, len(SecurityFunction.data)):
            if SecurityFunction.data[i]["id"] == elem["id"]:
                updated = True
                SecurityFunction.data[i] = elem
        if not updated:
            SecurityFunction.data.append(elem)

    @docstring(source='SecurityFunctions/GetSecurityFunctions.yml')
    def on_get(self, req, resp):
        resp_data, valid = SecurityFunctionSchema(method=HTTP_Method.GET) \
            .validate(data={})
        resp.body = json.dumps(SecurityFunction.data)

    @docstring(source='SecurityFunctions/PostSecurityFunctions.yml')
    def on_post(self, req, resp):
        resp_data, valid = SecurityFunctionSchema(method=HTTP_Method.POST) \
            .validate(data={})

        payload = req.media
        try:
            many = isinstance(payload, list)
            if not many:
                payload = [payload]
            sf_schema = SecurityFunctionSchema(many=True)
            d = sf_schema.load(req.media)
            for e in payload:
                SecurityFunction.update_data(e)

            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE

