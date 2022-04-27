from schema.security_functions import Agent as AgentSchema
from schema.security_functions import AgentType
from docstring import docstring
from resource.base import BaseResource
import json
from marshmallow.exceptions import ValidationError
from falcon import HTTP_CREATED, HTTP_NOT_ACCEPTABLE, HTTP_NOT_FOUND, HTTP_PRECONDITION_FAILED
from falcon import HTTP_204, HTTP_NO_CONTENT
from extra.lcp_config import LCPConfig
from extra.controller import LCPController


class SecurityFunction(BaseResource):
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
            resp.status = HTTP_NOT_ACCEPTABLE


class SecurityFunctionbyId(BaseResource):
    tag = {'name': 'Agents',
           'description': 'Describes the Agent types and Agent instances.'}
    routes = '/agent/instance/{id}',

    def __init__(self):
        pass

    @docstring(source='Agents/GetAgentInstanceResource.yml')
    def on_get(self, req, resp, id):
        a = LCPConfig().get_agent_instance_by_id(id)

        if a is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = json.dumps(a)

    @docstring(source='Agents/PutAgentInstanceResource.yml')
    def on_put(self, req, resp, id):
        a = LCPConfig().get_agent_instance_by_id(id)
        if a is None:
            resp.status = HTTP_NOT_FOUND
            return

        payload = req.media

        if 'id' in payload and payload['id'] != id:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = '{"message": "Id is a read-only field"}'
            return

        if 'hasAgentType' in payload and payload['hasAgentType'] != a['hasAgentType']:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = '{"message": "hasAgentType is a read-only field"}'
            pass

        a.update(payload)

        try:
            agent_schema = AgentSchema(many=False)
            agent_schema.load(a)
            resp.status = HTTP_204
            LCPController().set_agent_instance(a)
        except KeyError:
            resp.body = '{"error": "agent_type "' + a['type'] + ' not found"}'
            resp.status = HTTP_NOT_FOUND
            return

    @docstring(source='Agents/DeleteAgentInstanceResource.yml')
    def on_delete(self, req, resp, id):
        r = LCPConfig().delete_agent_instance_by_id(id)
        resp.status = HTTP_NO_CONTENT if r else HTTP_NOT_FOUND


class AgentTypeResource(BaseResource):
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
            resp.status = HTTP_NOT_ACCEPTABLE


class AgentTypeResourcebyId(BaseResource):
    tag = {'name': 'Agents',
           'description': 'Describes the Agent types and Agent instances.'}
    routes = '/agent/type/{id}',

    def __init__(self):
        pass

    @docstring(source="Agents/PutAgentTypeResource.yml")
    def on_put(self, req, resp, id):
        cfg = LCPConfig()
        at = LCPConfig().get_agent_type_by_id(id)
        if at is None:
            resp.status = HTTP_NOT_FOUND
            return

        data = req.media

        if 'id' in data and data['id'] != id:
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = '{"message": "Agent Type id is a read-only property"}'
            return

        at.update(data)
        cfg.set_agent_type(at)

        resp.status = HTTP_NO_CONTENT
        resp.body = ''

    @docstring(source="Agents/DeleteAgentTypeResource.yml")
    def on_delete(self, req, resp, id):
        cfg = LCPConfig()
        if cfg.exists_agent_instance_by_type(id):
            resp.status = HTTP_NOT_ACCEPTABLE
            resp.body = '{"message": "Agent Instance of this type exists yet. Remote them first"}'
            return

        at_deleted = cfg.delete_agent_type_by_id(id)

        resp.status = HTTP_NO_CONTENT if at_deleted else HTTP_NOT_FOUND
        pass

    @docstring(source="Agents/GetAgentTypeResource.yml")
    def on_get(self, req, resp, id):
        cfg = LCPConfig()
        agent = cfg.get_agent_type_by_id(id)
        if agent is None:
            resp.status = HTTP_NOT_FOUND
            resp.body = '{"message": "Agent Instance not found"}'
        else:
            resp.body = json.dumps(agent)
