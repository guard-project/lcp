from schema.security_functions import Agent as AgentSchema
from schema.security_functions import AgentType
from docstring import docstring
from resource.base import Base_Resource
import json
from marshmallow.exceptions import ValidationError
from falcon import HTTP_CREATED, HTTP_NOT_ACCEPTABLE, HTTP_NOT_FOUND
from extra.lcp_config import LCPConfig
from extra.cb_client import CBClient, ToContextBrokerMessages, CBMessages


class SecurityFunction(Base_Resource):
    tag = {'name': 'software',
           'description': 'Returns description of a Baremetal Server.'}
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

            d = ag_schema.load(payload)

            config = LCPConfig()

            for e in payload:
                type = e['type']
                agent_type = config.get_agent_type_by_id(type)
                if agent_type is None:
                    resp.body = '{"error": "agent_type "' + type + ' not found"}'
                    resp.status = HTTP_NOT_FOUND
                    return

                config.setAgent(e)
                message = CBMessages(ToContextBrokerMessages.AddAgentInstance, e)
                CBClient().send(message)


            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE


class AgentTypeResource(Base_Resource):
    tag = {'name': 'software',
           'description': 'Sets/Returns description of a type of Agent.'}
    routes = '/agent/type',

    @docstring(source="Agents/GetAgentTypeResource.yml")
    def on_get(self, req, resp):
        resp.body = json.dumps(LCPConfig().agent_types)

    @docstring(source="Agents/PostAgentTypeResource.yml")
    def on_post(self, req, resp):
        payload = req.media if isinstance(req.media, list) else [req.media]
        config = LCPConfig()

        try:
            at_schema = AgentType(many=True)
            d = at_schema.validate(payload)
            for e in payload:
                config.setAgentType(e)
                message = CBMessages(ToContextBrokerMessages.AddAgentType, e)
                CBClient().send(message)

            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.body = e.data
            req.status = HTTP_NOT_ACCEPTABLE
