from http import HTTPStatus

from utils.exception import extract_info
from utils.log import Log
from utils.sequence import expand, is_list
from utils.stack import info


class BaseResponse(object):
    error = False
    log_level = "info"

    def __init__(self, message, error=False, exception=None, **kwargs):
        self.log = Log.get(self.__class__.__name__)
        self.data = {"message": message}
        if exception is not None:
            self.data.update(exception=extract_info(exception))
        self.data.update(kwargs)

    def __data(self):
        return expand(
            dict(status=self.status(), code=self.code, error=self.error),
            **self.data
        )

    def __str__(self):
        return self.status()

    def __int__(self):
        return self.code

    def __dict__(self):
        return self.__data()

    def __log(self):
        if self.log_level is not None:
            e = self.data.get("exception", None)
            i = info(level=3)
            self.log.notice(f"@{i.filename}:{i.lineno}")
            msg = self.data.get("message", "No message")
            if e is not None:
                self.log.exception(msg, e)
            else:
                getattr(self.log, self.log_level)(msg)

    @classmethod
    def status(cls):
        return cls.code.phrase

    def apply(self, resp):
        self.__log()
        resp.media = self.__data()
        resp.status = f"{self.code} {self}"

    def add(self, resp):
        self.__log()
        if is_list(resp):
            resp.append(self.__data())
        else:
            if not is_list(resp.media):
                resp.media = []
            resp.media.append(self.__data())
            resp_code = int(resp.status.split()[0])
            if self.code is not None and HTTPStatus.gt(resp_code, self.code):
                resp.status = f"{self.code} {self.status()}"

    def update(self, **kwargs):
        self.data.update(kwargs)


class BadRequestResponse(BaseResponse):
    code = HTTPStatus.BAD_REQUEST
    error = True
    log_level = "error"

    def __init__(self, exception=None, **kwargs):
        title = (
            exception.title if exception is not None else "Request not valid"
        )
        super().__init__(title, exception=exception, **kwargs)


class ConflictResponse(BaseResponse):
    code = HTTPStatus.CONFLICT
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class CreatedResponse(BaseResponse):
    code = HTTPStatus.CREATED
    log_level = "success"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class InternalServerErrorResponse(BaseResponse):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error = True
    log_level = "error"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class NotAcceptableResponse(BaseResponse):
    code = HTTPStatus.NOT_ACCEPTABLE
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class NoContentResponse(BaseResponse):
    code = HTTPStatus.NO_CONTENT
    log_level = "warning"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class NotFoundResponse(BaseResponse):
    code = HTTPStatus.NOT_FOUND
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class NotModifiedResponse(BaseResponse):
    code = HTTPStatus.NOT_MODIFIED
    log_level = "warning"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class OkResponse(BaseResponse):
    code = HTTPStatus.OK
    log_level = "success"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class ContentResponse(OkResponse):
    log_level = None

    def __init__(self, content):
        self.data = content

    def apply(self, resp):
        resp.media = self.data
        resp.status = f"{self.code} {self}"


class ResetContentResponse(BaseResponse):
    code = HTTPStatus.RESET_CONTENT
    log_level = "warn"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class UnauthorizedResponse(BaseResponse):
    code = HTTPStatus.UNAUTHORIZED
    error = True
    log_level = "error"

    def __init__(self):
        super().__init__(message="Authentication failed")

    def apply(self, resp):
        super().apply(resp)
        resp.complete = True


class UnprocEntityResponse(BaseResponse):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class UnsupportedMediaTypeResponse(BaseResponse):
    code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    error = True
    log_level = "error"

    def __init__(self, exception=None, **kwargs):
        title = (
            exception.title
            if exception is not None
            else "Unsupported media type"
        )
        super().__init__(title, exception=exception, **kwargs)
