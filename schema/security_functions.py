import marshmallow.validate
from marshmallow import fields, Schema, validate
from schema.base import BaseSchema
from utils.schema import ListOrOne

__all__ = [
    'Agent',
    'AgentType',
    'AgentParameter',
    'AgentActionSchema',
    'AgentResource'
]

AGENT_STATUS = ['started', 'stopped', 'unknown']
PARAMETER_SCHEMAS = ['properties', 'json', 'xml', 'yaml']
PARAMETER_TYPES = ['binary', 'boolean', 'choice',
                   'integer', 'number', 'time-duration', 'string']

AgentTypeEnum = ['AgentType']
AgentInstanceEnum = ['AgentInstance']


class AgentParameter(BaseSchema):
    path = fields.Str(required=True, example="HeartbeatTime",
                      description="Name of the Parameter")
    type = fields.Str(required=True, example="integer",
                      description="Type of the Parameter: Int, Number, String...")
    # value = fields.Str(required=True, example="30",
    #                   description="Value of the Parameter to be configured")
    description = fields.Str(required=False, example="Time between Heartbeats",
                             description="Some description explaining the parameter")
    list = fields.Boolean(required=False, example="true",
                          description="Marks whether a parameter is list or not")


class AgentActionSchema(BaseSchema):
    id = fields.Str(required=True, example='start',
                    description='Action name')
    cmd = fields.Str(required=True, example='service filebeat start',
                     description='Action command.')
    status = fields.Str(enum=AGENT_STATUS, example=AGENT_STATUS[0],
                        description='Update the status the of the agent-instance according to cmd condition')


class AgentResource(BaseSchema):
    path = fields.Str(required=True, example="/etc/myagent/config.yaml",
                      description="Path of the Agent config file")
    description = fields.Str(required=False, example="This is the config file for an agent",
                             description="Description of the Resource")
    example = fields.Str(required=False, example="points to an example config file",
                         description="Config file example")


class AgentType(BaseSchema):
    id = fields.Str(required=True, example="5db06770-8c64-4693-9724-ff318b02f897",
                    description="Agent Type ID.")
    type = fields.Str(required=True, enum=AgentTypeEnum, example="AgentType",
                      validate=marshmallow.validate.OneOf(AgentTypeEnum),
                      description="Data type AgentType. Must be 'AgentType'")
    description = fields.Str(required=False, example="Example agent",
                             description="Description of the Agent type")
    parameters = ListOrOne(fields.Nested(AgentParameter), required=False,
                             description="List of configuration parameters used")
    partner = fields.Str(required=True, example="guard-partner",
                         description="Name of the Partner who created the resource")
    schema = fields.Str(required=True, example="yaml",
                        description="Type of configuration file (json, yaml, etc.)")
    source = fields.Str(required=True, example="/etc/example_agent/config.yaml",
                        description="The config file where parameters are configured")
    actions = ListOrOne(fields.Nested(AgentActionSchema), required=True,
                          description="List of actions and expected result fro this agent")
    resources = ListOrOne(fields.Nested(AgentResource), required=False,
                            description="List of agents Resources that could be used")
    jsonSchema = fields.Str(required=False, example="https://json-schema.org/draft/2020-12/schema",
                                  description="Pointer for the json describing the data from this kind of agents")


class Agent(BaseSchema):
    id = fields.Str(required=True, example="5db06770-8c64-4693-9724-ff318b02f897",
                    description="Security Function ID.")
    type = fields.Str(required=True, enum=AgentInstanceEnum, example="AgentInstance",
                      description="Data type AgentInstance. Must be 'AgentInstance'",
                      validate=marshmallow.validate.OneOf(AgentInstanceEnum))
    hasAgentType = fields.Str(required=True, example="PROBE",
                      description="Id of the Agent Type Associated with this Agent Instance")
    # name = fields.Str(required=False, example="VM Sensor Probe",
    #                  description="Name of the Agent Catalog")
    version = fields.Str(required=False, example="1.0.1",
                         description="Version of the Security Property associated")
    vendor = fields.Str(required=False, example="FIWARE Foundation e.V.",
                        description="Name of the vendor providing the security Function")
    description = fields.Str(required=False, example="Example agent",
                             description="Description of the Agent")
    partner = fields.Str(required=False, example="Guard Project",
                         description="Name of the partner/owner of the Agent")
    endpoint_url = fields.URL(required=False,
                              example="http://example.com:4250/v1/config",
                              description="URL if some to configure the Parameters.")
    status = fields.Str(required=True, enum=AGENT_STATUS, example=AGENT_STATUS[0],
                        description='Update the status the of the agent-instance if the command is executed correctly.',
                        validate=validate.OneOf(AGENT_STATUS))
