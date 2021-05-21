# from marshmallow.fields import Bool, DateTime as Date_Time, Nested, Str, URL
from marshmallow import fields, Schema
from schema.base import Base_Schema
from utils.datetime import FORMAT
from utils.schema import List_or_One

__all__ = [
    'LCPDescription',
    'ContextBrokerConnection',
    'LCPFatherConnection',
    'InitialConfigurationSchema'
]


class LCPDescription(Base_Schema):
    """Basic description of a LCP to be communicated to the CB as next Link for this LCP in
    the Business Chain. Further information could be requested by a Son LCP."""
    id = fields.Str(required=True, example='15d41167-79d3-48bf-b8db-9db0c8cc8d54',
                    description="Unique ID for the Son LCP")
    url = fields.URL(required=True, example="http://lcpapi.example.com:4000",
                     description="URL where the Son LCP Listens")
    description = fields.Str(required=False, example="Testing LCP in localhost",
                             description="A Human readable description, so it is easy to identify")


class LCPFatherConnection(Base_Schema):
    """Father sends the URL to their sons so they can send their "filiation" requests """
    url = fields.URL(required=True, example="http://lcpapi.example.com:4000",
                 description="URL where the Son LCP Listens")
    authMethod = fields.Str(required=False, example="none",
                            description="validation Method for this LCP")


class ContextBrokerConnection(Base_Schema):
    """ Basic connection Description for LCPs to connect to Context Broker"""
    url = fields.URL(required=True, example="http://cb.example.com:5000",
                     description="URL where the ContextBroker Listens")
    auth_header = fields.Str(required=False,
                             example="Basic Z3VhcmQ6cGFzc3dvcmQK")
    # user = fields.Str(required=True, example="cb",
    #                   description="Context Broker user with rights to set new exec-envs")
    # password = fields.Str(required=True, example="cbsecretpassword",
    #                  description="Context Broker password for the user")



class InitialConfigurationSchema(Base_Schema):
    lcp = fields.Nested(LCPDescription, required=True,
                        description="Initial LCP configuration. Requisite to enable extra_features")
    context_broker = fields.Nested(ContextBrokerConnection, required=False,
                                   description="Connection to Context broker if one required")
