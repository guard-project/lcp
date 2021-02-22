from marshmallow import fields, Schema, validate
from schema.base import Base_Schema

__all__ = [
    'SoftwareDefinition'
]

class SoftwareDefinition(Base_Schema):
    """Describe a Piece of Software in terms of name, vendor, version and opened ports"""
    id = fields.Str(required=True, example="a406874b-dea7-4cd1-9d4e-b82a18ec993b",
                    description="ID of this Software Instance")
    name = fields.Str(required=True, example="MySQL",
                      description="Name of this piece of Software instance")
    version = fields.Str(required=True, example="5.8+1.0.5ubuntu2",
                         description="Version of the Piece of Software installed")
    openTCPPorts = fields.List(fields.Int, required=False, example="[3306]",
                               description="List of opened TCP Ports")
    openUDPPorts = fields.List(fields.Int, required=False, example="[33066]",
                               description="List of opened UDP Ports")
    vendor = fields.Str(required=False, example="Oracle Coorporation",
                        description="Name of the Vendor for this software")
