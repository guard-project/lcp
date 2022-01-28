.. _api:


API
===

.. currentmodule:: api

.. autofunction:: api


Error Handler
-------------

.. currentmodule:: api.error_handler

.. autoclass:: BaseHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BadRequestHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: InternalServerErrorHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnsupportedMediaTypeHandler
    :members:
    :private-members:
    :inherited-members:


Media Handler
-------------

.. currentmodule:: api.media_handler

.. autoclass:: XMLHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: YAMLHandler
    :members:
    :private-members:
    :inherited-members:


Middleware
----------

.. currentmodule:: api.middleware

.. autoclass:: NegotiationMiddleware
    :members:
    :private-members:
    :inherited-members:


Spec
----

.. currentmodule:: api.spec

.. autoclass:: Spec
    :members:
    :private-members:
    :inherited-members:


Docstring
---------

.. currentmodule:: docstring

.. autodecorator:: docstring


Lib
---

.. currentmodule:: lib.http

.. autoclass:: HTTPMethod
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: HTTPStatus
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: lib.polycube

.. autoclass:: Polycube
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: lib.token

.. autofunction:: create_token


Response
--------

.. currentmodule:: lib.response

.. autoclass:: BaseResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BadRequestResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConflictResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ContentResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: CreatedResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: InternalServerErrorResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NoContentResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotAcceptableResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotFoundResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotModifiedResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: OkResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ResetContentResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnauthorizedResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnprocessableEntityResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnsupportedMediaTypeResponse
    :members:
    :private-members:
    :inherited-members:


Reader
------

.. currentmodule:: reader.arg

.. autoclass:: ArgReader
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: reader.config

.. autoclass:: ConfigReader
    :members:
    :private-members:
    :inherited-members:


Resource
--------

.. currentmodule:: resource

.. autofunction:: routes

.. currentmodule:: resource.base

.. autoclass:: BaseResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.code

.. autoclass:: CodeResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.config

.. autoclass:: ConfigResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.status

.. autoclass:: StatusResource
    :members:
    :private-members:
    :inherited-members:

Schema
------

.. currentmodule:: schema.validate

.. autoclass:: In
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UniqueList
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: schema.base

.. autoclass:: BaseSchema
    :members:
    :private-members:
    :inherited-members:


Code
^^^^
.. currentmodule:: schema.code

.. autoclass:: CodeRequestSchema
    :members:
    :private-members:
    :inherited-members:


Config
^^^^^^

.. currentmodule:: schema.config

Request
"""""""

.. autoclass:: ConfigRequestSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConfigActionRequestSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConfigParameterRequestSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConfigResourceRequestSchema
    :members:
    :private-members:
    :inherited-members:


Response
""""""""

.. autoclass:: ConfigActionResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConfigParameterResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConfigParameterValueResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConfigResourceResponseSchema
    :members:
    :private-members:
    :inherited-members:


Status
^^^^^^

.. currentmodule:: schema.status

.. autoclass:: StatusRequestSchema
    :members:
    :private-members:
    :inherited-members:


.. autoclass:: StatusResponseSchema
    :members:
    :private-members:
    :inherited-members:


Response
^^^^^^^^

.. currentmodule:: schema.response

.. autoclass:: ExceptionResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BaseResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BadRequestResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConflictResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ContentResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: CreatedResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NoContentResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotAcceptableResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotFoundResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotModifiedResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: OkResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ResetContentResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnauthorizedResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnprocessableEntityResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnsupportedMediaTypeResponseSchema
    :members:
    :private-members:
    :inherited-members:


Utils
-----

Datetime
^^^^^^^^

.. currentmodule:: utils.datetime

.. autodata:: FORMAT

.. autofunction:: datetime_from_str

.. autofunction:: datetime_to_str


Exception
^^^^^^^^^

.. currentmodule:: utils.exception

.. autofunction:: extract_info

.. autofunction:: to_str


JSON
^^^^

.. currentmodule:: utils.json

.. autofunction:: dumps

.. autofunction:: loads


Log
^^^

.. currentmodule:: utils.log

.. autoclass:: Log
    :members:
    :private-members:
    :inherited-members:


Sequence
^^^^^^^^

.. currentmodule:: utils.sequence

.. autofunction:: expand

.. autofunction:: format

.. autofunction:: is_dict

.. autofunction:: is_list

.. autofunction:: iterate

.. autofunction:: subset

.. autofunction:: table_to_dict

.. autofunction:: wrap


Signal
^^^^^^

.. currentmodule:: utils.signal

.. autofunction:: send_tree


String
^^^^^^

.. currentmodule:: utils.string

.. autoclass:: Formatter
    :members:
    :private-members:
    :inherited-members:

.. autofunction:: is_str

.. autodata:: format


Time
^^^^

.. currentmodule:: utils.time

.. autofunction:: get_seconds
