from resource.base import Base_Resource
from docstring import docstring
from schema.software_definitions import SoftwareDefinition as SoftwareDefinitionSchema
from schema.software_definitions import ContainerSchema
from marshmallow.exceptions import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED
import json
from extra.lcp_config import LCPConfig
import traceback


class SoftwareDefinition(Base_Resource):
    tag = {'name': 'software',
           'description': 'Returns the description of software installed'}
    routes = '/self/software'

    def __init__(self):
        pass

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
            resp.status = HTTP_CREATED

            for e in payload:
                LCPConfig().setSoftware(e)

        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = e.messages


class ContainerDefinition(Base_Resource):
    tag = {'name': 'software',
           'description': 'Returns the description of software installed in containers'}
    routes = "/self/container"

    def __init__(self):
        pass

    @docstring(source="Software/GetSoftware.yml")
    def on_get(self, req, resp):
        resp.body = json.dumps(LCPConfig().self_containers)

    @docstring(source="Software/PostSoftware.yml")
    def on_post(self, req, resp):
        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            software_schema = ContainerSchema(many=True)
            software_schema.load(payload)
            resp.status = HTTP_CREATED

            for e in payload:
                LCPConfig().setContainers(e)

        except ValidationError as e:
            traceback.print_exc()
            resp.body = e.messages
            resp.status = HTTP_NOT_ACCEPTABLE
