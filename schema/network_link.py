from schema.base import BaseSchema
from marshmallow import fields, validate


NetworkLinkEnum = ["NetworkLink"]
NetworkLinkTypeEnum = ["multi-pnt", "network-slice", "pnt2pnt", "wifi", "hosted"]


class NetworkLink(BaseSchema):
    """Define the Network link schema needed for Context Broker"""
    type = fields.Str(required=True, example="NetworkLink", enum=NetworkLinkEnum)
    id = fields.Str(required=True, example="a12bc576-b55d-4392-b613-f3babd1cb77f",
                    description="ID of the Network link")
    networkLinkType = fields.Str(required=True, enum=NetworkLinkTypeEnum,
                                 description="network link type for this link")
    remoteExecutionEnvironmentId = fields.Str(required=False,
                                              description="Remote execution environment linked")
    remoteArtifactId = fields.Str(required=False, description="Remote artifact connected")


class NetworkLInkCB(BaseSchema):
    id = fields.Str(required=True, example="a12bc576-b55d-4392-b613-f3babd1cb77f",
                    description="ID of the Network link")
    type_id = fields.Str(required=True, enum=NetworkLinkTypeEnum,
                         description="network link type for this link")
    description = fields.Str(required=False,
                              description="Human readable description for the Network link")
