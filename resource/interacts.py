from docstring import docstring
from resource.base import Base_Resource
from marshmallow import ValidationError
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_OK
import json
from extra.lcp_config import LCPConfig
from schema.artifacts import InteractsWithSchema
from utils.log import Log


class Interacts(Base_Resource):
    tag = {'name': 'interacts', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/interacts',

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
            req.status = HTTP_NOT_ACCEPTABLE

    @docstring(source="interacts/getInteractsWith.yml")
    def on_get(self, req, resp):
        cfg = LCPConfig()
        resp.body = json.dumps(cfg.interactions)
        resp.status = HTTP_OK

