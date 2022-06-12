from docstring import docstring
from resource.base import BaseResource
from schema.poll_cb_schema import PollSchema
from extra.lcp_config import LCPConfig
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK, HTTP_ACCEPTED, HTTP_FAILED_DEPENDENCY
import json
from extra.cb_helpers.security_context_helper import SecurityContextHelper
import traceback


class PollContextBroker(BaseResource):
    tag = {'name': 'cb integration', 'description': 'Retrieves data from LCP to the Context Broker'}
    routes = '/poll'

    def __init__(self):
        pass

    @docstring(source="poll/get_poll.yml")
    def on_get(self, req, resp):
        try:
            helper = SecurityContextHelper(LCPConfig())
            resp.body = helper.getData()
        except ValueError as ve:
            resp.status = HTTP_FAILED_DEPENDENCY
            resp.body = json.dumps(ve.messages)
        except KeyError as e:
            resp.body = json.dumps({"messages": "Unconfigured LCP"})
            resp.status = HTTP_NOT_FOUND





