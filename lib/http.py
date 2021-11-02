from http import HTTPStatus

from utils.log import Log


class HTTPMethod(object):
    """Constants representing various HTTP request methods."""

    GET = 'get'
    PUT = 'put'
    POST = 'post'
    DELETE = 'delete'


code_priority_order = cpo = {
    HTTPStatus.OK: 1,
    HTTPStatus.CREATED: 2,
    HTTPStatus.RESET_CONTENT: 2,
    HTTPStatus.NOT_MODIFIED: 0,
    HTTPStatus.NOT_FOUND: 3,
    HTTPStatus.NO_CONTENT: 4,
    HTTPStatus.CONFLICT: 4,
    HTTPStatus.NOT_ACCEPTABLE: 4,
    HTTPStatus.UNPROCESSABLE_ENTITY: 4
}


def __lt(code_a, code_b):
    pa = __get(code_a)
    pb = __get(code_b)
    return pa is not None and pb is not None and pa < pb


def __lte(code_a, code_b):
    pa = __get(code_a)
    pb = __get(code_b)
    return pa is not None and pb is not None and pa <= pb


def __gt(code_a, code_b):
    pa = __get(code_a)
    pb = __get(code_b)
    return pa is not None and pb is not None and pa > pb


def __gte(code_a, code_b):
    pa = __get(code_a)
    pb = __get(code_b)
    return pa is not None and pb is not None and pa >= pb


def __eq(code_a, code_b):
    pa = __get(code_a)
    pb = __get(code_b)
    return pa is not None and pb is not None and pa == pb


def __get(code):
    po = cpo.get(code, None)
    if po is None:
        Log.get('http-lib').warn(f'{code} without priority order.')


HTTPStatus.lt = __lt
HTTPStatus.lte = __lte
HTTPStatus.gt = __gt
HTTPStatus.gte = __gte
HTTPStatus.eq = __eq
