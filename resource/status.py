from docstring import docstring
from lib.http import HTTPMethod
from lib.response import ContentResponse
from schema.status import StatusRequestSchema, StatusResponseSchema
from utils.datetime import datetime_to_str
from utils.log import Log


class StatusResource(object):
    auth = {'exempt_methods': ['POST']}
    tag = {'name': 'status', 'description': 'Status data of the LCP.'}
    routes = '/status',

    def __init__(self):
        """Set the data and logger."""
        self.data = {'id': False, 'started': datetime_to_str(),
                     'last_heartbeat': False}
        self.log = Log.get('status')

    @docstring(source='status/get.yaml')
    def on_get(self, req, resp):
        ContentResponse(self.data).apply(resp)

    @docstring(source='status/post.yaml')
    def on_post(self, req, resp):
        req_data = req.media or {}
        resp_data, valid = (StatusRequestSchema(method=HTTPMethod.POST)
                            .validate(data=req_data))
        if valid:
            now = datetime_to_str()
            id = req_data.get('id')
            self.data['id'] = id
            self.data['last_heartbeat'] = now
            self.log.notice(f'Hearbeating from CB at {now}')
            resp_data, valid = (StatusResponseSchema(method=HTTPMethod.POST)
                                .validate(data=self.data))
            if valid:
                ContentResponse(self.data).apply(resp)
            else:
                resp_data.apply(resp)
        else:
            resp_data.apply(resp)
