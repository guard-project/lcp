from docstring import docstring
from resource.base import Base_Resource
from schema.lcp_schemas import LCPDescription
from marshmallow import ValidationError
from schema.response import Created_Response
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from utils.sequence import is_list, wrap
from lib.http import HTTP_Method
from schema.hardware_definitions import BaremetalServer as BaremetalServerSchema
from schema.hardware_definitions import VirtualServer as VirtualServerSchema
from schema.hardware_definitions import LXCContainer as LXCContainerSchema
import json
from falcon import HTTPError
import falcon

class BaremetalServer(Base_Resource):
    data = []
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/baremetal',

    @classmethod
    def update_data(cls, elem):
        updated = False
        for i in range(0, len(BaremetalServer.data)):
            if BaremetalServer.data[i]["id"] == elem["id"]:
                updated = True
                BaremetalServer.data[i] = elem
        if not updated:
            BaremetalServer.data.append(elem)

    def __init__(self):
        pass

    @docstring(source='BaremetalServer/GetBaremetalServer.yml')
    def on_get(self, req, resp):
        resp_Data, valid = BaremetalServerSchema(method=HTTP_Method.GET) \
            .validate(data={})

        resp.body = json.dumps(BaremetalServer.data)

    @docstring(source='BaremetalServer/PostBaremetalServer.yml')
    def on_post(self, req, resp):
        resp_data, valid = BaremetalServerSchema(method=HTTP_Method.POST) \
            .validate(data={})

        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            bm_schema = BaremetalServerSchema(many=True)
            bm_schema.load(payload)
            for e in payload:
                BaremetalServer.update_data(e)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            raise HTTPError(falcon.HTTP_406, 'Error', e.messages)


class VirtualServer(Base_Resource):
    data = []
    tag = {'name': 'hardware',
           'description': 'Returns description of a Baremetal Server.'}
    routes = '/virtualserver',

    @classmethod
    def update_data(cls, elem):
        updated = False
        for i in range(0, len(VirtualServer.data)):
            if VirtualServer.data[i]["id"] == elem["id"]:
                updated = True
                VirtualServer.data[i] = elem
        if not updated:
            VirtualServer.data.append(elem)

    def __init__(self):
        pass

    @docstring(source='VirtualServer/GetVirtualServer.yml')
    def on_get(self, req, resp):
        resp_Data, valid = VirtualServerSchema(method=HTTP_Method.GET) \
            .validate(data={})

        resp.body = json.dumps(VirtualServer.data)

    @docstring(source='VirtualServer/PostVirtualServer.yml')
    def on_post(self, req, resp):
        resp_data, valid = VirtualServerSchema(method=HTTP_Method.POST) \
            .validate(data={})

        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            bm_schema = VirtualServerSchema(many=True)
            bm_schema.load(payload)
            for e in payload:
                VirtualServer.update_data(e)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            raise HTTPError(falcon.HTTP_406, 'Error', e.messages)


class LXCContainer(Base_Resource):
    data = []
    tag = {'name': 'hardware',
           'description': 'Returns description of a LXCContainer.'}
    routes = '/lxc',

    @classmethod
    def update_data(cls, elem):
        updated = False
        for i in range(0, len(LXCContainer.data)):
            if LXCContainer.data[i]["id"] == elem["id"]:
                updated = True
                LXCContainer.data[i] = elem
        if not updated:
            LXCContainer.data.append(elem)


    @docstring(source='LXCContainer/GetLXCContainer.yml')
    def on_get(self, req, resp):
        resp_Data, valid = LXCContainerSchema(method=HTTP_Method.GET) \
            .validate(data={})

        resp.body = json.dumps(LXCContainer.data)

    @docstring(source='LXCContainer/PostLXCContainer.yml')
    def on_post(self, req, resp):
        resp_data, valid = LXCContainerSchema(method=HTTP_Method.POST) \
            .validate(data={})

        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            bm_schema = LXCContainerSchema(many=True)
            bm_schema.load(payload)
            for e in payload:
                LXCContainer.update_data(e)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            raise HTTPError(falcon.HTTP_406, 'Error', e.messages)


class SomethingToPost(Base_Resource):
    @docstring(source='LXCContainer/PostLXCContainer.yml')
    def on_post(self, req, resp):
        resp_data, valid = LXCContainerSchema(method=HTTP_Method.POST) \
            .validate(data={})

        payload = req.media if isinstance(req.media, list) else [req.media]

        try:
            bm_schema = LXCContainerSchema(many=True)
            bm_schema.load(payload)
            for e in payload:
                LXCContainer.update_data(e)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            raise HTTPError(falcon.HTTP_406, 'Error', e.messages)
