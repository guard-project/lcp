from marshmallow.fields import Bool, DateTime as Date_Time, Nested, Str
from schema.base import Base_Schema
from utils.datetime import FORMAT
from utils.schema import List_or_One

__all__ = [
    'FooThing'
]


# FIXME add missing required fields
class FooThing(Base_Schema):
    """Request for code endpoint."""

    id = Str(required=True, example='firewall',
               description='Foothing for testing id.')
    code = List_or_One(Str, required=True,
                       description='Code source')
