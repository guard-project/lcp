from marshmallow import fields, Schema, validate
from schema.base import Base_Schema


CONTAINER_TECHNOLOGY = ["lxc", "docker", "k8s", "rkt"]

__all__ = [
    'SoftwareDefinition',
    'ContainerSchema'
]

class SoftwareDefinition(Base_Schema):
    """Describe a Piece of Software in terms of name, vendor, version and opened ports"""
    id = fields.Str(required=True, example="a406874b-dea7-4cd1-9d4e-b82a18ec993b",
                    description="ID of this Software Instance")
    product = fields.Str(required=True, example="MySQL",
                      description="Name of this piece of Software instance")
    version = fields.Str(required=True, example="5.8.1",
                         description="Version of the Piece of Software installed")
    openTCPPorts = fields.List(fields.Int, required=False, example="[3306]",
                               description="List of opened TCP Ports")
    openUDPPorts = fields.List(fields.Int, required=False, example="[33066]",
                               description="List of opened UDP Ports")
    vendor = fields.Str(required=False, example="Oracle Coorporation",
                        description="Name of the Vendor for this software")
    connections = fields.List(fields.Str, required=False, example="[]",
                            description="List of Known connected/related Software")
    # vendor = fields.Str(required=True, example="Oracle Coorporation",
    #                    description="Name of the Vendor for this software"),

class ContainerSchema(Base_Schema):
    id = fields.Str(required=True, example="413216e3-169f-4638-830e-ef0607732fde",
                    description="Id of the Container.")
    technology = fields.Str(required=True, enum=CONTAINER_TECHNOLOGY, example="docker",
                            description="Description of the Container")
    software = fields.List(fields.Nested(SoftwareDefinition), required=True,
                           description="Description of the Software contained in the container")
