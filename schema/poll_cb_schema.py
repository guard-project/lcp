import marshmallow.validate
from marshmallow import fields
from schema.base import Base_Schema
from schema.hardware_definitions import *
from schema.software_definitions import ContainerSchema, SoftwareDefinition
from schema.artifacts import InteractsWithSchema
from schema.hardware_definitions import EXEC_ENV_TYPE

__all__ = [
    'PollSchema',
    'LCPConnection',
    'LCPContextBrokerDefinition'
]


class LCPConnection(Base_Schema):
    port: fields.Int(required=True, example=4000,
                     description="Port where the LCP is listening")
    https: fields.Boolean(required=True, example=True,
                          description="Defines the protocol to connect the LCP. HTTPS if true, HTTP if false")


class LCPContextBrokerDefinition(Base_Schema):
    id = fields.Str(required=True, example='15d41167-79d3-48bf-b8db-9db0c8cc8d54',
                    description="Unique ID for the Son LCP")
    description = fields.Str(required=False, example="Testing LCP in localhost",
                             description="A Human readable description, so it is easy to identify")
    enabled = fields.Boolean(required=True, example=True,
                         description="Describes if the LCP is enabled or not")
    lcp = fields.Nested(LCPConnection, required=True)
    type_id = fields.Str(required=True, example="bare-metal", enum=EXEC_ENV_TYPE,
                                          description="Type of execution environment",
                                          validate=marshmallow.validate.OneOf(EXEC_ENV_TYPE))
    hostname = fields.Str(required=True, example="localhost",
                          description="Hostname of the Host where the LCP can be contacted. If a proxy is behind the LCP, the value should be the proxy host")
    hasSons = fields.List(fields.Str, required=False, example=["lpc:son:id:1", "lcp:son:id:2"])


class PollSchema(Base_Schema):
    executionEnvironmentType = fields.Str(required=True, example="bare-metal", enum=EXEC_ENV_TYPE,
                                          description="Type of execution environment",
                                          validate=marshmallow.validate.OneOf(EXEC_ENV_TYPE))
    lcp = fields.Nested(LCPContextBrokerDefinition, required=True,
                        description="LCP Description as required by the CB")
    lcpSons = fields.List(fields.Nested(LCPContextBrokerDefinition), required=False)
    lcpParent = fields.URL(required=True, example="http://lcpapi.example.com:4000",
                     description="URL where the parent LCP Listens.")
    executionEnvironment = fields.Nested(BaremetalServer, required=False,
                                         description="One of BaremetalServer, VirtualServer, DockerContainer or LXCContainer schemas")
    container = fields.List(fields.Nested(ContainerSchema), required=False)
    software = fields.List(fields.Nested(SoftwareDefinition), required=False)
    interactions = fields.Nested(InteractsWithSchema, required=False)
