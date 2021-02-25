from marshmallow import fields, Schema, validate
from schema.base import Base_Schema
from utils.schema import List_or_One

__all__ = [
    'CloudSchema',
    'CloudController',
    'CloudCompute',
]


class CloudController(Base_Schema):
    type = fields.Str(required=True, example="BaremetalServer",
                    description="Type of server acting as CloudController")
    controller_id = fields.Str(required=True, example="3b3041bf-b2fb-47da-8e72-331a67ffd292",
                               description="ID of the Controller host")


class CloudCompute(Base_Schema):
    type = fields.Str(required=True, example="BaremetalServer",
                      description="Type of server acting as CloudController")
    controller_id = fields.Str(required=True, example="3b3041bf-b2fb-47da-8e72-331a67ffd292",
                               description="ID of the Compute host. The controller could act as compute")


class CloudSchema(Base_Schema):
    """
    Definition Schema for a Cloud. One Cloud is defined by a few values. It could also
    optionally include the Controllers of the Cloud and its compute nodes. However, this
    information could only be available when using a self-hosted cloud. We don't have
    this kind of information for other clouds like Amazon o Google Cloud.
    """
    id = fields.Str(required=True, example="f9e6ee65-517a-44da-854d-fdd058fcf2dd",
                    description="Cloud ID")
    name = fields.Str(required=True, example="Wolfsburg-FIWARE-Lab-Cloud",
                      description="Human readable Cloud name")
    vendor = fields.Str(required=True, example="Openstack",
                        description="Cloud Vendor Name")
    version = fields.Str(required=False, example="queens",
                         description="Cloud release code name")
    description = fields.Str(required=False, example="FIWARE Lab Wolfsburg node",
                             description="Some description of the Cloud")
    controllers = fields.List(fields.Nested(CloudController), required=False,
                              description="List of Cloud Controllers")
    compute_nodes = fields.List(fields.Nested(CloudCompute), required=False,
                                description="List of Cloud compute nodes")
