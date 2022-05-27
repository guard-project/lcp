from marshmallow import validate
from marshmallow.fields import Boolean
from marshmallow.fields import DateTime as Date_Time
from marshmallow.fields import Float, Integer, List, Nested, Raw, Str

from schema.base import BaseSchema
from utils.datetime import FORMAT
from utils.schema import ListOrOne

_all__ = [
    "ConfigRequestSchema",
    "ConfigActionResponseSchema",
    "ConfigParameterResponseSchema",
    "ConfigResourceResponseSchema",
]

OUTPUT_FORMATS = ["plain", "lines", "json"]
PARAMETER_SCHEMAS = ["json", "properties", "xml", "yaml"]
RESPONSE_TYPES = ["action", "parameter", "resource"]

EXAMPLE_FILENAME = "firewall.xml"


class ConfigActionRequestSchema(BaseSchema):
    """Action part in a single item of the code request."""

    id = Str(required=True, example="start", description="Id of the action.")
    cmd = Str(required=True, description="Command.")
    args = ListOrOne(
        Str,
        many=True,
        example="-al",
        description="Command argument."
    )
    daemon = Boolean(
        default=False,
        example=True,
        description="Execute the command as daemon.",
    )
    output_format = Str(
        enum=OUTPUT_FORMATS,
        default=OUTPUT_FORMATS[0],
        example=OUTPUT_FORMATS[1],
        description="Format of the output of the command.",
    )


class ConfigParameterRequestSchema(BaseSchema):
    """Parameter part in a single item of the code request."""

    id = Str(
        required=True, example="period", description="Id of the parameter."
    )
    schema = Str(
        required=True,
        enum=PARAMETER_SCHEMAS,
        example="yaml",
        description="Scheme.",
        validate=validate.OneOf(PARAMETER_SCHEMAS),
    )
    source = Str(
        required=True, example=EXAMPLE_FILENAME, description="Source filename."
    )
    path = ListOrOne(Str, required=True, example="period", description="Key path.")
    value = Raw(
        required=True, example="10s", description="Parameter new value."
    )


class ConfigResourceRequestSchema(BaseSchema):
    """Resource part in a single item of the code request."""

    id = Str(
        required=True,
        example="filebeat-config",
        description="Id of the resource.",
    )
    path = Str(
        required=True, example=EXAMPLE_FILENAME, description="File path"
    )
    content = Str(required=True, description="Resource content.")


class ConfigRequestSchema(BaseSchema):
    """Request for config endpoint."""

    actions = Nested(
        ConfigActionRequestSchema,
        many=True,
        unknown="INCLUDE",
        description="List of actions.",
    )
    parameters = Nested(
        ConfigParameterRequestSchema,
        many=True,
        unknown="INCLUDE",
        description="List of parameters.",
    )
    resources = Nested(
        ConfigResourceRequestSchema,
        many=True,
        unknown="INCLUDE",
        description="List of resources.",
    )


class ConfigResponseSchema(BaseSchema):
    """Response for config endpoint."""

    id = Str(required=True, example="start", description="Config id.")
    data = Raw(description="Configuration data.")
    timestamp = Date_Time(
        format=FORMAT,
        required=True,
        description="Timestamp when the configuration is done.",
    )  # noqa:E501
    type = Str(
        enum=RESPONSE_TYPES,
        example=RESPONSE_TYPES[0],
        description="Type of the response.",
        validate=validate.OneOf(RESPONSE_TYPES),
    )
    error = Boolean(
        default=False,
        example=True,
        description="Indicate the presence of an error.",
    )


class ConfigActionResponseSchema(ConfigResponseSchema):
    """Action part in a single item of the config response."""

    stdout = Raw(description="Standard output of the execution.")
    stderr = Raw(description="Standard error output of the execution.")
    duration = Float(description="Execution time of the action (in seconds")
    return_code = Integer(
        required=True,
        example=0,
        description="Exit code of the execution (0: no error).",
    )  # noqa:E501


class ConfigParameterValueResponseSchema(BaseSchema):
    """Parameter value part in a single item of the config response."""

    new = Raw(required=True, example="5s", description="New value.")
    old = Raw(
        required=True, example="10s", description="Old value", allow_none=True
    )


class ConfigParameterResponseSchema(ConfigResponseSchema):
    """Parameter part in a single item of the config response."""

    value = Nested(ConfigParameterValueResponseSchema)
    note = Str(example="No change needed.", description="Additional note.")


class ConfigResourceResponseSchema(ConfigResponseSchema):
    """Resource part in a single item of the config response."""

    pass
