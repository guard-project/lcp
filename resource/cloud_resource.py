from docstring import docstring
from resource.base import BaseResource
from schema.cloudschema import CloudSchema
import json
from lib.http import HTTPMethod
from marshmallow.exceptions import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE


class CloudInfrastructure(BaseResource):
    data = []

    tag = {'name': 'hardware',
           'description': 'Description of a Cloud Infrastructure'}
    routes = "/cloud"

    def __init__(self):
        super().__init__()

    @classmethod
    def update_data(cls, elem):
        updated = False
        for i in range(0, len(CloudInfrastructure.data)):
            if CloudInfrastructure.data[i]["id"] == elem["id"]:
                updated = True
                CloudInfrastructure.data[i] = elem
        if not updated:
            CloudInfrastructure.data.append(elem)

    @docstring(source="Cloud/GetCloudInfrastructure.yml")
    def on_get(self, req, resp):
        resp_data, valid = CloudSchema(method=HTTPMethod.GET) \
        .validate(data={})

        resp.body = json.dumps(CloudInfrastructure.data)

    @docstring(source="Cloud/PostCloudInfrastructure.yml")
    def on_post(self, req, resp):
        resp_data, valid = CloudSchema(method=HTTPMethod.POST) \
            .validate(data={})
        payload = req.media if isinstance(req.media, list) else [req.media]

        try:
            cl_schema = CloudSchema(many=True)
            cl_schema.load(payload)
            for e in payload:
                CloudInfrastructure.update_data(e)
        except ValidationError as ve:
            resp.body = json.dumps(ve.messages)
            req.status = HTTP_NOT_ACCEPTABLE
