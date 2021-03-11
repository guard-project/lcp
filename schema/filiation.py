# from marshmallow.fields import Bool, DateTime as Date_Time, Nested, Str, URL
from marshmallow import fields, Schema
from schema.base import Base_Schema
from utils.datetime import FORMAT
from utils.schema import List_or_One

__all__ = [
    'LCPSonDescription',
    'ContextBrokerConnection'
]


class LCPSonDescription(Base_Schema):
    """Basic description of a LCP to be communicated to the CB as next Link for this LCP in
    the Business Chain. Further information could be requested by a Son LCP."""
    id = fields.Str(required=True, example='15d41167-79d3-48bf-b8db-9db0c8cc8d54',
                    description="Unique ID for the Son LCP")
    url = fields.URL(required=True, example="http://lcpapi.example.com:4000",
                     description="URL where the Son LCP Listens")
    name = fields.Str(required=True, example="lcp:node1",
                      description="A Human readable name which could be depicted in graphs")


class ContextBrokerConnection(Base_Schema):
    """ Basic connection Description for LCPs to connect to Context Broker"""
    url = fields.URL(required=True, example="http://cb.example.com:5000",
                     description="URL where the ContextBroker Listens")
    user = fields.Str(required=True, example="cb",
                      description="Context Broker user with rights to set new exec-envs")
    password = fields.Str(required=True, example="cbsecretpassword",
                      description="Context Broker password for the user")
