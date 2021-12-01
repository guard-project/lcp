from docstring import docstring
from resource.base import BaseResource
from marshmallow import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK, HTTP_ACCEPTED, HTTP_FAILED_DEPENDENCY
from lib.http import HTTPMethod
from schema.lcp_schemas import LCPDescription, LCPFatherConnection
import json
from extra.lcp_config import LCPConfig
from extra.lcp_client import LCPClient, LCPMessages, BetweenLCPMessages
from utils.log import Log
import requests


class SonLCPIdentification(BaseResource):
    # data = {}
    tag = {'name': 'lcp_relationships', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/lcp_son',

    def __init__(self):
        self.log = Log.get('SonLCPIdentification')

    @docstring(source="filiation/get_lcp_son.yaml")
    def on_get(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTPMethod.GET) \
          .validate(data={})
        self.log.notice("GET /lcp_son -- ")
        child_nodes = LCPConfig().sons
        resp.body = json.dumps(child_nodes)

    @docstring(source="filiation/post_lcp_son.yaml")
    def on_post(self, req, resp):
        self_lcp = LCPConfig().lcp
        if self_lcp is None:
            resp.status = HTTP_FAILED_DEPENDENCY
            resp.body = json.dumps({"messages": "Unconfigured LCP"})
            return

        resp_Data, valid = LCPDescription(method=HTTPMethod.POST) \
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
                self.test_if_im_in(f['url'])
                # TODO - Notify the parent about this, please.

            resp.status = HTTP_CREATED
            resp.body = json.dumps(self_lcp)
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = json.dumps(e.messages)


    def test_if_im_in(self, url):
        try:
            r = requests.get(url + "/lcp_parent")
            self_url = LCPConfig().lcp['url']
            parents = r.json()
            for p in parents:
                if p == self_url:
                    return
        except:
            pass
            ## Gues it's not ready... but send messages until it is ready.

        message = LCPMessages(BetweenLCPMessages.PostLCPParent, url)
        LCPClient().send(message)



class ParentLCPIdentification(BaseResource):
    tag = {'name': 'lcp_relationships', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/lcp_parent'

    def __init__(self):
        self.log = Log.get('SonLCPIdentification')
        self.notified = []


    @docstring(source="filiation/post_lcp_parent.yaml")
    def on_post(self, req, resp):
        self_lcp = LCPConfig().lcp
        if self_lcp is None:
            resp.status = HTTP_FAILED_DEPENDENCY
            resp.body = json.dumps({"messages": "Unconfigured LCP"})
            return
        resp_Data, valid = LCPDescription(method=HTTPMethod.POST) \
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
                if f not in self.notified:
                    self.notified.append(f)
                    LCPClient().send(LCPMessages(BetweenLCPMessages.PostLCPSon, f))
            resp.status = HTTP_ACCEPTED
            resp.body = json.dumps(self_lcp)
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE

    @docstring(source="filiation/get_lcp_parents.yaml")
    def on_get(self, req, resp):
        resp_Data, valid = LCPDescription(method=HTTPMethod.GET) \
           .validate(data={})
        self.log.notice("GET /lcp_parent -- ")
        parents_urls = LCPConfig().parents
        resp.body = json.dumps(parents_urls)

    @docstring(source="filiation/delete_lcp_parent.yaml")
    def on_delete(self, req, resp):
        self.log.notice("DELETE /lcp_parent --")
        resp.status = HTTP_NOT_FOUND


class SonRequestIdentificationById(BaseResource):
    tag = {'name': 'lcp_relationships', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/lcp_son/{id}',

    def __init__(self):
        pass

    @docstring(source='filiation/get_lcp_son_by_id.yaml')
    def on_get(self, req, resp, id):
        cfg = LCPConfig()
        son = cfg.getSonById(id)

        if son is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = json.dumps(son)

    @docstring(source='filiation/delete_lcp_son_by_id.yaml')
    def on_delete(self, req, resp, id):
        cfg = LCPConfig()
        d = cfg.deleteSonById(id)
        if d is not None:
            resp.body = json.dumps(d)
            resp.status = HTTP_OK
        else:
            resp.status = HTTP_NOT_FOUND

