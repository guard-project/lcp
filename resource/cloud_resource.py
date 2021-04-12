from docstring import docstring
from resource.base import Base_Resource
from schema.cloudschema import CloudSchema
import json
from lib.http import HTTP_Method
from marshmallow.exceptions import ValidationError
from falcon import HTTP_CREATED, HTTP_NOT_ACCEPTABLE


class CloudInfrastructure(Base_Resource):
    data = []

    tag = {'name': 'hardware',
           'description': 'Description of a Cloud Infrastructure'}
    routes = "/cloud"

    def __init__(self):
        pass

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
        resp_Data, valid = CloudSchema(method=HTTP_Method.GET) \
        .validate(data={})

        resp.body = json.dumps(CloudInfrastructure.data)

    @docstring(source="Cloud/PostCloudInfrastructure.yml")
    def on_post(self, req, resp):
        resp_data, valid = CloudSchema(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media if isinstance(req.media, list) else [req.media]

        try:
            cl_schema = CloudSchema(many=True)
            cl_schema.load(payload)
            for e in payload:
                CloudInfrastructure.update_data(e)
        except ValidationError as ve:
            resp.body = ve.data
            req.status = HTTP_NOT_ACCEPTABLE



