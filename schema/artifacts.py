import marshmallow.validate
from marshmallow import fields
from schema.base import BaseSchema
from schema.software_definitions import SoftwareDefinition
from schema.response import OkResponse
from marshmallow.exceptions import ValidationError as Validation_Error

STORAGE_TYPES = ["S3", "NFS", "iSCSI", "Swift", "CEPH", "GlusterFS", "SSH-FS"]
ExternalStorageSchemaEnum = ["ExternalStorage"]


class ExternalStorageSchema(BaseSchema):
    """Class ExternalStorageSchema describing an external storage which is used by our system.
    """

    id = fields.Str(required=True, example="a406874b-dea7-4cd1-9d4e-b82a18ec993b",
                    description="ID of this external Storage type")
    type = fields.Str(required=True, example="ExternalStorage", enum=ExternalStorageSchemaEnum,
                      validate=marshmallow.validate.OneOf(ExternalStorageSchemaEnum),
                      description="Type of the document. It must be External Storage")
    storageType = fields.Str(required=True, example="NFS", enum=STORAGE_TYPES,
                             description="Type of storage type.")
    description = fields.Str(required=False, example="remote nfs drive",
                             description="High level description for this remote storage drive")
    url = fields.Str(required=True, example="nfs://192.168.10.245:2049/data",
                     description="URL for this remote resource")


class InteractsWithSchema(BaseSchema):
    """Class describing the external storage pieces and the Software Artifacts interacting with
    our LCP system"""

    externalStorage = fields.List(fields.Nested(ExternalStorageSchema), required=False,
                                  description="External storage devices description")
    softwareArtifacts = fields.List(fields.Nested(SoftwareDefinition), required=False,
                                    description="Software artifacts interacting with this LCP")
