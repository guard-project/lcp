from docstring import docstring
from resource.base import Base_Resource
from marshmallow import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK, HTTP_ACCEPTED
from lib.http import HTTP_Method
from schema.lcp_schemas import LCPDescription, LCPFatherConnection
import json
from extra.lcp_config import LCPConfig
from extra.lcp_client import LCPClient, LCPMessages, BetweenLCPMessages
from utils.log import Log


class SonLCPIdentification(Base_Resource):
    # data = {}
    tag = {'name': 'lcp_relationships', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/lcp_son',

    def __init__(self):
        self.log = Log.get('SonLCPIdentification')

    @docstring(source="filiation/get_lcp_son.yaml")
    def on_get(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTP_Method.GET) \
          .validate(data={})
        self.log.notice("GET /lcp_son -- ")
        child_nodes = LCPConfig().sons
        resp.body = json.dumps(child_nodes)

    @docstring(source="filiation/post_lcp_son.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media if isinstance(req.media, list) else [req.media]
        cfg = LCPConfig()
        self.log.notice("POST /lcp_son -- ")
        try:
            lcp = LCPDescription(many=True)
            lcp.load(payload)
            valid = lcp.validate(payload)
            for f in payload:
                cfg.setSon(f)
                if cfg.context_broker is not None:
                    resp.body = json.dumps(cfg.context_broker)

            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = json.dumps(e.messages)


class ParentLCPIdentification(Base_Resource):
    tag = {'name': 'lcp_relationships', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/lcp_parent'

    def __init__(self):
        self.log = Log.get('SonLCPIdentification')


    @docstring(source="filiation/post_lcp_parent.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media if isinstance(req.media, list) else [req.media]
        cfg = LCPConfig()
        self.log.notice("POST /lcp_parent -- ")

        try:
            parent = LCPFatherConnection(many=True)
            parent.load(payload)
            parent.validate(payload)
            for f in payload:
                cfg.setParent(f)
                LCPClient().send(LCPMessages(BetweenLCPMessages.PostLCPSon, f))
            resp.status = HTTP_ACCEPTED
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = json.dumps(e.messages)

    @docstring(source="filiation/get_lcp_parents.yaml")
    def on_get(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTP_Method.GET) \
           .validate(data={})
        self.log.notice("GET /lcp_parent -- ")
        parents_urls = LCPConfig().parents
        resp.body = json.dumps(parents_urls)


class SonRequestIdentificationById(Base_Resource):
    tag = {'name': 'lcp_relationships', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/lcp_son/{id}',

    def __init__(self):
        pass

    @docstring(source='filiation/get_lcp_son_by_id.yaml')
    def on_get(self, req, resp, id):
        resp_Data, valid = LCPDescription(method=HTTP_Method.GET) \
            .validate(data={}, id=id)
        cfg = LCPConfig()
        son = cfg.getSonById(id)

        if son is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = json.dumps(son)

    @docstring(source='filiation/delete_lcp_son_by_id.yaml')
    def on_delete(self, req, resp, id):
        resp_Data, valid = LCPDescription(method=HTTP_Method.DELETE) \
            .validate(data={}, id=id)
        cfg = LCPConfig()
        d = cfg.deleteSonById(id)
        if d is not None:
            resp.body = json.dumps(d)
            resp.status = HTTP_OK
        else:
            resp.status = HTTP_NOT_FOUND



