from schema.security_functions import Agent as AgentSchema
from schema.security_functions import AgentType
from docstring import docstring
from resource.base import Base_Resource
import json
from marshmallow.exceptions import ValidationError
from falcon import HTTP_CREATED, HTTP_NOT_ACCEPTABLE, HTTP_NOT_FOUND, HTTP_PRECONDITION_FAILED
from extra.lcp_config import LCPConfig
from extra.controller import LCPController


class SecurityFunction(Base_Resource):
    tag = {'name': 'Agents',
           'description': 'Describes the Agent types and Agent instances.'}
    routes = '/agent/instance',

    def __init__(self):
        pass

    @docstring(source='Agents/GetAgentInstanceResource.yml')
    def on_get(self, req, resp):
        # resp_data, valid = SecurityFunctionSchema(method=HTTP_Method.GET) \
        #    .validate(data={})
        resp.body = json.dumps(LCPConfig().agents)

    @docstring(source='Agents/PostAgentInstanceResource.yml')
    def on_post(self, req, resp):
        # resp_data, valid = AgentSchema(method=HTTP_Method.POST) \
        #    .validate(data={})

        payload = req.media if isinstance(req.media, list) else [req.media]
        try:
            ag_schema = AgentSchema(many=True)
            ag_schema.load(payload)

            controller = LCPController()

            for e in payload:
                try:
                    controller.set_agent_instance(e)
                except KeyError:
                    resp.body = '{"error": "agent_type "' + e['type'] + ' not found"}'
                    resp.status = HTTP_NOT_FOUND
                    return

            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = json.dumps(e.messages)
            req.status = HTTP_NOT_ACCEPTABLE


class SecurityFunctionbyId(Base_Resource):
    tag = {'name': 'Agents',
           'description': 'Describes the Agent types and Agent instances.'}
    routes = '/agent/instance/{id}',

    def __init__(self):
        pass

    @docstring(source='Agents/PutAgentInstanceResource.yml')
    def on_put(self, req, resp, id):
        req.status = HTTP_NOT_FOUND

    @docstring(source='Agents/DeleteAgentInstanceResource.yml')
    def on_delete(self, req, resp, id):
        req.status = HTTP_NOT_FOUND


class AgentTypeResource(Base_Resource):
    tag = {'name': 'Agents',
           'description': 'Describes the Agent types and Agent instances.'}
    routes = '/agent/type',

    @docstring(source="Agents/GetAgentTypeResource.yml")
    def on_get(self, req, resp):
        resp.body = json.dumps(LCPConfig().agent_types)

    @docstring(source="Agents/PostAgentTypeResource.yml")
    def on_post(self, req, resp):
        payload = req.media if isinstance(req.media, list) else [req.media]
        controller = LCPController()

        try:
            at_schema = AgentType(many=True)
            d = at_schema.validate(payload)
            if d[1] == False:
                raise ValidationError("Not acceptable")
            for e in payload:
                controller.set_agent_type(e)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = json.dumps(e.messages)
            req.status = HTTP_NOT_ACCEPTABLE

class AgentTypeResourcebyId(Base_Resource):
    tag = {'name': 'Agents',
           'description': 'Describes the Agent types and Agent instances.'}
    routes = '/agent/type/{id}',

    def __init__(self):
        pass


    @docstring(source="Agents/PutAgentTypeResource.yml")
    def on_put(self, req, resp, id):
        req.status = HTTP_NOT_FOUND

    @docstring(source="Agents/DeleteAgentTypeResource.yml")
    def on_delete(self, req, resp, id):
        req.status = HTTP_NOT_FOUND
