from operator import itemgetter as item_getter
from resource.base import BaseResource

from docstring import docstring
from lib.http import HTTPMethod
from lib.polycube import Polycube
from lib.response import (CreatedResponse, NoContentResponse, OkResponse,
                          ResetContentResponse, UnprocEntityResponse)
from schema.code import CodeRequestSchema
from utils.sequence import is_list, wrap

MSG_OK = 'Code with the id={} correctly {}'
MSG_NOT_POSSIBLE = 'Not possible to {} code with the id={}'
MSG_NO_CONTENT = 'No content to {} code with the {{request}}'


class CodeResource(BaseResource):
    tag = {'name': 'code', 'description': 'Code injection at run-time.'}
    routes = '/code', '/code/{id}',

    def __init__(self):
        self.polycube = Polycube()

    @docstring(source='code/post.yaml')
    def on_post(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = (CodeRequestSchema(many=is_list(req_data),
                                              unknown='INCLUDE',
                                              method=HTTPMethod.POST)
                            .validate(data=req.media, id=id))
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for data in req_data_wrap:
                    id, code, interface, metrics = item_getter('id', 'code',
                                                               'interface',
                                                               'metrics')(data)
                    if all([id, code, interface]):
                        if is_list(code):
                            code = '\n'.join(code)
                        pc = self.polycube.create(cube=id, code=code,
                                                  interface=interface,
                                                  metrics=metrics)
                        if not pc.get('error', False):
                            resp_data = CreatedResponse(
                                MSG_OK.format(id, 'created'))
                        else:
                            resp_data = UnprocEntityResponse(
                                MSG_NOT_POSSIBLE.format('create', id))
                        resp_data.update(**pc)
                    else:
                        resp_data = UnprocEntityResponse(
                            MSG_NOT_POSSIBLE.format('create', id))
                    resp_data.apply(resp)
            else:
                NoContentResponse(MSG_NO_CONTENT.format(
                    'create'), request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    @docstring(source='code/put.yaml')
    def on_put(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = (CodeRequestSchema(many=is_list(req_data),
                                              partial=True,
                                              method=HTTPMethod.PUT)
                            .validate(data=req.media, id=id))
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for data in req_data_wrap:
                    id, code, interface, metrics = item_getter('id', 'code',
                                                               'interface',
                                                               'metrics')(data)
                    if all([id, code, interface]):
                        if is_list(code):
                            code = '\n'.join(code)
                        pc = self.polycube.update(cube=id, code=code,
                                                  interface=interface,
                                                  metrics=metrics)
                        if not pc.get('error', False):
                            resp_data = OkResponse(
                                MSG_OK.format(id, 'updated'))
                        else:
                            resp_data = UnprocEntityResponse(
                                MSG_NOT_POSSIBLE.format('update', id))
                        resp_data.update(**pc)
                    else:
                        resp_data = UnprocEntityResponse(
                            MSG_NOT_POSSIBLE.format('update', id))
                    resp_data.apply(resp)
            else:
                NoContentResponse(MSG_NO_CONTENT.format(
                    'update'), request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    @ docstring(source='code/post.yaml')
    def on_delete(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = (CodeRequestSchema(many=is_list(req_data),
                                              partial=True,
                                              method=HTTPMethod.DELETE)
                            .validate(data=req.media, id=id))
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for data in req_data_wrap:
                    id = data.get('id', None)
                    if id is not None:
                        pc = self.polycube.delete(cube=id)
                        if not pc.get('error', False):
                            resp_data = ResetContentResponse(
                                MSG_OK.format(id, 'deleted'))
                        else:
                            resp_data = UnprocEntityResponse(
                                MSG_NOT_POSSIBLE.format('delete', id))
                        resp_data.update(**pc)
                    else:
                        resp_data = UnprocEntityResponse(
                            MSG_NOT_POSSIBLE.format('update', id))
                    resp_data.apply(resp)
            else:
                NoContentResponse(MSG_NO_CONTENT.format(
                    'delete'), request=req_data).apply(resp)
        else:
            resp_data.apply(resp)
