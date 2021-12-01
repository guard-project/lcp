from docstring import docstring
from resource.base import BaseResource
from marshmallow import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_OK, HTTP_NOT_FOUND, HTTP_204
import json
from extra.lcp_config import LCPConfig
from schema.artifacts import InteractsWithSchema
from schema.artifacts import SoftwareDefinition, ExternalStorageSchema
from utils.log import Log


class Interacts(BaseResource):
    tag = {'name': 'interacts', 'description': 'Describes interactions with other external resources.'}
    routes = '/interactions',

    def __init__(self):
        super().__init__()
        self.log = Log.get('Interacts')

    @docstring(source="interacts/postInteractsWith.yml")
    def on_post(self, req, resp):
        self.log.notice("POST /interacts -- ")
        payload = req.media
        cfg = LCPConfig()

        try:
            sch = InteractsWithSchema()
            sch.load(payload, many=False)
            for d in payload:
                if d == 'externalStorage':
                    for elem in payload['externalStorage']:
                        cfg.add_external_storage_interaction(elem)
                elif d == 'softwareArtifacts':
                    for elem in payload['softwareArtifacts']:
                        cfg.add_external_software_interaction(elem)
            resp.status = HTTP_CREATED
        except ValidationError as ve:
            resp.body = json.dumps(ve.messages)
            resp.status = HTTP_NOT_ACCEPTABLE

    @docstring(source="interacts/getInteractsWith.yml")
    def on_get(self, req, resp):
        cfg = LCPConfig()
        resp.body = json.dumps(cfg.interactions)
        resp.status = HTTP_OK


class InteractsById(BaseResource):
    tag = {'name': 'interacts', 'description': 'Describes interactions with other external resources.'}
    routes = '/interactions/{id}',

    def __init__(self):
        super().__init__()
        self.log = Log.get('Interactions')

    @docstring(source="interacts/deleteInteractsWithById.yml")
    def on_delete(self, req, resp, id):
        resp.status = HTTP_NOT_FOUND
        config = LCPConfig()
        if config.delete_external_software_interaction(id) or config.delete_external_storage_interaction(id):
            resp.status = HTTP_204

    @docstring(source="interacts/putInteractsWithById.yml")
    def on_put(self, req, resp, id):
        self.log.notice("PUT /interacts -- ")
        data = req.media
        if 'id' in data:
            if id != data['id']:
                resp.status = HTTP_NOT_ACCEPTABLE
                resp.body = {"message": "id can't be updated"}
        config = LCPConfig()
        interaction = config.getInteractionById(id)
        if interaction is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.status = HTTP_204
            try:
                if 'softwareArtifacts' in interaction:
                    sa = interaction['softwareArtifacts']
                    sa.update(data)
                    SoftwareDefinition().load(sa)
                    config.add_external_software_interaction(sa)
                if 'externalStorage' in interaction:
                    es = interaction['externalStorage']
                    es.update(data)
                    ExternalStorageSchema().load(es)
                    config.add_external_storage_interaction(es)
            except ValidationError as ve:
                resp.status = HTTP_NOT_ACCEPTABLE
                resp.body = json.dumps(ve.messages)


    @docstring(source="interacts/getInteractsWithById.yml")
    def on_get(self, req, resp, id):
        config = LCPConfig()
        interaction = config.getInteractionById(id)
        if interaction is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.status = HTTP_OK
            resp.body = json.dumps(interaction)
