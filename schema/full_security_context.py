from schema.base import BaseSchema
from marshmallow import fields
from schema.hardware_definitions import ExecutionEnvironment
from schema.lcp_schemas import LCPDescription

SecurityContextEnum = ['SecurityContext']


class SecurityContext(BaseSchema):
    id = fields.Str(required=True, example="bc2e2eff-fda1-45be-b7f1-93485b756470",
                    description="This LCP ID.")
    type = fields.Str(required=True, example="SecurityContext", enum=SecurityContextEnum,
                      description="Class SecurityContext. The value must be 'SecurityContext'")
    hasExecutionEnvironment = fields.Nested(ExecutionEnvironment, required=False,
                                            description="Description of the Execution Environment type")
    executionEnvironment = fields.Nested(BaseSchema, required=False,
                                         description="Proper execution environment data in hardware terms")
    hasSons = fields.List(fields.Str, required=False,
                          description="List of the LCP sons. The Context Broker should provision these sons. These "
                                      "sons must be described in field lcpSons.")
    lcpSons = fields.List(fields.Nested(LCPDescription), required=False,
                          description="LCP Description of LCP sons to this LCP. So they can build a hierarchical scheme")


