# from marshmallow.fields import Bool, DateTime as Date_Time, Nested, Str, URL
from marshmallow import fields, Schema
from schema.base import Base_Schema
from utils.datetime import FORMAT
from utils.schema import List_or_One


__all__ = [
    'Filiation'
]

class LCPBasics(Base_Schema):
    """Basic description of a LCP to be communicated to the CB as next Link for this LCP in
    the Business Chain. Further information could be requested by a Son LCP."""
    id = fields.Str(required=True, example='15d41167-79d3-48bf-b8db-9db0c8cc8d54',
             description="Unique ID for the Son LCP")
    url = fields.URL(required=True, example="http://lcpapi:4000",
              description="URL where the Son LCP Listens")


# FIXME add missing required fields
#class Filiation(Base_Schema):
#    """Request for code endpoint."""
#    List_or_One(LCPBasics, required=True,
#                description='A single or a list of LCPs linked as Filiated',
#                example='{"id": "15d41167-79d3-48bf-b8db-9db0c8cc8d54", "url": "http://lcpapi:4000"}')
