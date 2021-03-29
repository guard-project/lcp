from marshmallow import fields, Schema, validate
from schema.base import Base_Schema
from utils.schema import List_or_One

__all__ = [
    'SecurityFunction',
    'AgentParameter',
    'AgentActionSchema'
]

AGENT_STATUS = ['started', 'stopped', 'unknown']
PARAMETER_SCHEMAS = ['properties', 'json', 'xml', 'yaml']
PARAMETER_TYPES = ['binary', 'boolean', 'choice',
                   'integer', 'number', 'time-duration', 'string']


class AgentParameter(Base_Schema):
    name = fields.Str(required=True, example="HeartbeatTime",
                      description="Name of the Parameter")
    type = fields.Str(required=True, example="integer",
                      description="Type of the Parameter: Int, Number, String...")
    value = fields.Str(required=True, example="30",
                       description="Value of the Parameter to be configured")
    description = fields.Str(required=False, example="Time between Heartbeats",
                             description="Some description explaining the parameter")


class AgentActionSchema(Base_Schema):
    id = fields.Str(required=True, example='start',
             description='Action name')
    cmd = fields.Str(required=True, example='service filebeat start',
              description='Action command.')
    # args = fields.Str(many=True, example='-v',
    #           description='Action command argument')
    # daemon = fields.Bool(default=False, example=True,
    #              description='Execute the command as daemon.')
    ## parameters = fields.Nested(AgentParameter)
    status = fields.Str(enum=AGENT_STATUS, example=AGENT_STATUS[0],
                        description='Update the status the of the agent-instance according to cmd condition')


class SecurityFunction(Base_Schema):
    id = fields.Str(required=True, example="5db06770-8c64-4693-9724-ff318b02f897",
                    description="Security Function ID.")
    type = fields.Str(required=True, example="PROBE",
                      description="Type of the Security Function Associated with the LCP")
    name = fields.Str(required=True, example="VM Sensor Probe",
                      description="Name of the Agent Catalog")
    version = fields.Str(required=True, example="1.0.1",
                         description="Version of the Security Property associated")
    vendor = fields.Str(required=True, example="FIWARE Foundation e.V.",
                        description="Name of the vendor providing the security Function")
    parameters = List_or_One(fields.Nested(AgentParameter), required=False,
                             description="List of configuration parameters used")
    endpoint_url = fields.URL(required=False,
                              example="http://example.com:4250/v1/config",
                              description="URL if some to configure the Parameters.")
    status = fields.Str(enum=AGENT_STATUS, example=AGENT_STATUS[0],
                        description='Update the status the of the agent-instance if the command is executed correctly.',
                        validate=validate.OneOf(AGENT_STATUS))
    actions = List_or_One(fields.Nested(AgentActionSchema), required=False)
