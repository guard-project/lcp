from marshmallow.fields import DateTime, Str

from schema.base import BaseSchema
from utils.datetime import FORMAT


class StatusRequestSchema(BaseSchema):
    """Response for status endpoint."""

    id = Str(required=True, example='apache',
             description='ID of the execution environment.')


class StatusResponseSchema(BaseSchema):
    """Response for status endpoint."""

    id = Str(required=True, example='apache',
             description='ID of the execution environment.')
    started = DateTime(format=FORMAT, required=True,
                       example='2019/02/14 15:23:30',
                       description='Timestamp when the LCP is started')
    last_heartbeat = DateTime(format=FORMAT, required=True,
                              example='2019/02/14 15:23:33',
                              description='Timestamp of the expiration of the API access configuration.')  # noqa:E501
