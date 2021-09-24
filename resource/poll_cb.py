from docstring import docstring
from resource.base import Base_Resource
from schema.full_security_context import SecurityContext
from extra.lcp_config import LCPConfig
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK, HTTP_ACCEPTED, HTTP_FAILED_DEPENDENCY
import json
from extra.cb_helpers.security_context_helper import SecurityContextHelper


class PollContextBroker(Base_Resource):
    tag = {'name': 'cb integration', 'description': 'Retrieves data from LCP to the Context Broker'}
    routes = '/poll'

    def __init__(self):
        pass

    def on_get(self, req, resp):
        try:
            helper = SecurityContextHelper(LCPConfig())
            resp.body = helper.getData()
        except KeyError:
            resp.body = json.dumps({"messages": "Unconfigured LCP"})
            resp.status = HTTP_NOT_FOUND





