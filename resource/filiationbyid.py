from docstring import docstring
from resource.base import Base_Resource
from schema.filiation import LCPBasics
from marshmallow import ValidationError
from schema.response import Created_Response
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from utils.sequence import is_list, wrap
import json

__all__ = [
    'FiliationById',
    'Filiation'
]

class Filiation(Base_Resource):
    data = {}
    tag = {'name': 'Filiation', 'description': 'Does Nothing but allows me learn.'}
    routes = '/filiation',

    def __init__(self):
        pass

    @docstring(source='filiation/get.yaml')
    def on_get(self, req, resp):
        child_nodes = []
        for k in Filiation.data:
            child_nodes.append(Filiation.data[k])
        resp.body = json.dumps(child_nodes)

    @docstring(source="filiation/get.yaml")
    def on_post(self, req, resp):
        payload = req.media
        try:
            lcp = LCPBasics(many=False)
            lcp.load(payload)
            valid = lcp.validate(payload)
            Filiation.data[payload['id']] = payload
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = json.dumps(e.messages)


class FiliationById(Base_Resource):
    tag = {'name': 'Filiation', 'description': 'Does Nothing but allows me learn.'}
    routes = '/filiation/{id}',

    def __init__(self):
        pass

    @docstring(source='filiation/get.yaml')
    def on_get(self, req, resp, id):
        if id in Filiation.data:
            o = Filiation.data[id]
            resp.body = json.dumps(o)
            return
        else:
            resp.status = HTTP_NOT_FOUND

    @docstring(source='filiation/get.yaml')
    def on_delete(self, req, resp, id):
        if id in Filiation.data:
            o = Filiation.data
            Filiation.data.pop(id)
            resp.body = json.dumps(o)
            resp.status = HTTP_OK
        else:
            resp.status = HTTP_NOT_FOUND



