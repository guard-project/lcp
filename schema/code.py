from marshmallow.fields import Str

from schema.base import BaseSchema
from utils.schema import ListOrOne


# FIXME add missing required fields
class CodeRequestSchema(BaseSchema):
    """Request for code endpoint."""

    id = Str(required=True, example="firewall", description="Code id.")
    code = ListOrOne(Str, required=True, description="Code source")
