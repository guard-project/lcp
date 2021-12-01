from falcon.errors import (HTTPBadRequest, HTTPInternalServerError,
                           HTTPUnsupportedMediaType)

from lib.response import (BadRequestResponse, InternalServerErrorResponse,
                          UnsupportedMediaTypeResponse)


class BaseHandler(object):
    @classmethod
    def handler(cls, req, resp, ex, params):
        cls.response(exception=ex).apply(resp)
        resp.complete = True

    @classmethod
    def get(cls):
        return cls.error, cls.handler


class BadRequestHandler(BaseHandler):
    error = HTTPBadRequest
    response = BadRequestResponse


class InternalServerErrorHandler(BaseHandler):
    error = HTTPInternalServerError
    response = InternalServerErrorResponse


class UnsupportedMediaTypeHandler(BaseHandler):
    error = HTTPUnsupportedMediaType
    response = UnsupportedMediaTypeResponse
