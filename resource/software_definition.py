from resource.base import BaseResource
from docstring import docstring
from schema.software_definitions import SoftwareDefinition as SoftwareDefinitionSchema
from schema.software_definitions import ContainerSchema
from marshmallow.exceptions import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_204, HTTP_OK, HTTP_NO_CONTENT
import json
from extra.lcp_config import LCPConfig
# import traceback


class SoftwareDefinition(BaseResource):
    tag = {'name': 'software',
           'description': 'Returns the description of software installed'}
    routes = '/self/software'

    def __init__(self):
        super().__init__()

    @docstring(source="Software/GetSoftware.yml")
    def on_get(self, req, resp):
        resp.body = json.dumps(LCPConfig().self_software)

    @docstring(source="Software/PostSoftware.yml")
    def on_post(self, req, resp):
        payload = req.media
        try:
            many = isinstance(payload, list)
            if not many:
                payload = [payload]
            software_schema = SoftwareDefinitionSchema(many=True)
            software_schema.load(payload)
            resp.status = HTTP_CREATED

            for e in payload:
                LCPConfig().set_software(e)

        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = json.dumps(e.messages)


class SoftwareDefinitionById(BaseResource):
    tag = {'name': 'software',
           'description': 'Returns the description of software installed'}
    routes = '/self/software/{id}'

    def __init__(self):
        super().__init__()

    @docstring(source="Software/GetSoftware.yml")
    def on_get(self, req, resp, id):
        s = LCPConfig().get_software_by_id(id)
        if s is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = json.dumps(s)

    @docstring(source="Software/GetSoftware.yml")
    def on_delete(self, req, resp, id):
        found = LCPConfig().delete_software_by_id(id)
        if not found:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.status = HTTP_204

    @docstring(source="Software/PostSoftware.yml")
    def on_put(self, req, resp, id):
        payload = req.media

        s = LCPConfig().get_software_by_id(id)
        if s is None:
            resp.status = HTTP_NOT_FOUND
            return

        if 'id' in payload and payload['id'] != id:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = '{"message": "ID is a read-only field"}'
            return

        s.update(payload)

        try:
            software_schema = SoftwareDefinitionSchema(many=False)
            software_schema.load(s)
            resp.status = HTTP_204
            LCPConfig().set_software(s)
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = json.dumps(e.messages)


class ContainerDefinition(BaseResource):
    tag = {'name': 'software',
           'description': 'Returns the description of software installed in containers'}
    routes = "/self/container"

    def __init__(self):
        super().__init__()

    @docstring(source="Software/GetContainer.yml")
    def on_get(self, req, resp):
        resp.body = json.dumps(LCPConfig().self_containers)

    @docstring(source="Software/PostContainer.yml")
    def on_post(self, req, resp):
        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            software_schema = ContainerSchema(many=True)
            software_schema.load(payload)
            resp.status = HTTP_CREATED

            for e in payload:
                LCPConfig().set_containers(e)

        except ValidationError as e:
            resp.body = json.dumps(e.messages)
            resp.status = HTTP_NOT_ACCEPTABLE


class ContainerDefinitionById(BaseResource):
    tag = {'name': 'software',
           'description': 'Returns the description of software installed in containers'}
    routes = "/self/container/{id}"

    @docstring(source="Software/GetContainer.yml")
    def on_get(self, req, resp, id):
        d = LCPConfig().get_container_by_id(id)
        if d is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = json.dumps(d)
            resp.status = HTTP_OK

    @docstring(source="Software/GetContainer.yml")
    def on_delete(self, req, resp, id):
        d = LCPConfig().delete_container_by_id(id)
        resp.status = HTTP_NO_CONTENT if d else HTTP_NOT_FOUND

