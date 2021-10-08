import marshmallow.validate
from marshmallow import fields
from schema.base import Base_Schema

__all__ = [
    'LCPDescription',
    'LCPFatherConnection'
]

LCPDescriptionEnum = ['LCPDescription']


class LCPDescription(Base_Schema):
    """Basic description of a LCP to be communicated to the CB as next Link for this LCP in
    the Business Chain. Further information could be requested by a Son LCP."""
    id = fields.Str(required=True, example='15d41167-79d3-48bf-b8db-9db0c8cc8d54',
                    description="Unique ID for the Son LCP")
    url = fields.URL(required=True, example="http://lcpapi.example.com:4000",
                     description="URL where the Son LCP Listens")
    name = fields.Str(required=True, example="lcp-example",
                      description="Name for the LCP in readable human format")
    description = fields.Str(required=False, example="Testing LCP in localhost",
                             description="A Human readable description, so it is easy to identify")
    type = fields.Str(required=True, enum=LCPDescriptionEnum, example="LCPDescription",
                      validate=marshmallow.validate.OneOf(LCPDescriptionEnum),
                      description="FIWARE's type for this class: LCPDescription")
    exec_env_type = fields.Str(required=False, enum=LCPDescriptionEnum, example="bare-metal",
                      description="execution environment type")


class LCPFatherConnection(Base_Schema):
    """Father sends the URL to their sons so they can send their "filiation" requests """
    url = fields.URL(required=True, example="http://lcpapi.example.com:4000",
                     description="URL where the Son LCP Listens")
    # authMethod = fields.Str(required=False, example="none",
    #                        description="validation Method for this LCP")
