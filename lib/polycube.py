from json import loads

from falcon.errors import HTTPGatewayTimeout as HTTP_Gateway_Timeout
from falcon.errors import HTTPServiceUnavailable as HTTP_Service_Unavailable
from requests import HTTPError as HTTP_Error
from requests import delete as delete_req
from requests import get as get_req
from requests import post as post_req
from requests import put as put_req
from requests.exceptions import ConnectionError, Timeout

from reader.arg import ArgReader
from utils.log import Log

MSG_CONN_NOT_POSSIBLE = 'Connection to Polycube at {} not possible'
MSG_RESP_NOT_RECV = 'Timely response not received from polycube at {} in {} seconds.'  # noqa: E501


class Polycube:
    def __init__(self):
        self.host = ArgReader.db.polycube_host
        self.port = ArgReader.db.polycube_port
        self.timeout = ArgReader.db.polycube_timeout
        self.endpoint = f'http://{self.host}:{self.port}/polycube/v1'
        self.log = Log.get('polycube')

        self.log.info(f'Check connection to {self.endpoint}')
        try:
            resp_req = get_req(self.endpoint,
                               timeout=ArgReader.db.polycube_timeout)
            self.__manager(resp_req)
        except (ConnectionRequestError, HTTP_Error) as e:
            self.log.exception(f"""Connection with polycube at
                                   {self.host}:{self.port} not possible""", e)

    def get(self, cube):
        self.log.info(f'Get info of cube {cube}')
        try:
            resp_req = get_req(f'{self.endpoint}/dynmon/{cube}',
                               timeout=self.timeout)
            self.__manager(resp_req)
            return loads(resp_req.content)
        except HTTP_Error:
            return None

    def create(self, cube, code, interface, metrics):
        data = {'name': cube, 'code': code, 'interface': interface,
                'metrics': metrics}
        if self.get(cube) is None:
            self.log.info(f'Create cube {cube}.')
            attached_info = {}
            try:
                dp_cfg = self.__dataplane_config(cube, code, metrics)
                resp_req = put_req(f'{self.endpoint}/dynmon/{cube}',
                                   json={'dataplane-config': dp_cfg},
                                   timeout=self.timeout)
                attached_info = self.__attach(cube, interface)
                return dict(status='created', attached_info=attached_info,
                            detached_info={},
                            data=data, **self.__from_resp(resp_req))
            except Exception as e:
                self.log.exception(f'Cube {cube} not created', e)
                return dict(status='error', interface=attached_info,
                            detached_info={}, data=data,
                            **self.__from_resp(resp_req, error=True))
        else:
            return {'error': True, 'description': f'Cube {cube} found.',
                    'data': data}

    def delete(self, cube):
        data = {'cube': cube}
        if self.get(cube) is None:
            return {'error': True, 'description': f'Cube {cube} not found.',
                    'data': data}

        self.log.info(f'Delete cube {cube}.')
        try:
            resp_req = delete_req(f'{self.endpoint}/dynmon/{cube}',
                                  timeout=self.timeout)
            self.__manager(resp_req)
            return dict(status='deleted', data=data,
                        **self.__from_resp(resp_req))
        except Exception as e:
            self.log.exception(f'Cube {cube} not deleted', e)
            return dict(error=True, data=data,
                        **self.__from_resp(resp_req, error=True))

    def update(self, cube, code, interface, metrics):
        data = {'name': cube, 'code': code, 'interface': interface,
                'metrics': metrics}
        service = self.get(cube)
        if service is None:
            return {'error': True, 'description': f'Cube {cube} not found.',
                    'data': data}

        self.log.info(f'Update cube {cube}.')
        try:
            attached_iface = service.get('parent', None)
            attached_info = {}
            detached_info = {}
            if attached_iface is None:
                attached_info = self.__attach(cube, cube)
            elif attached_iface != interface:
                attached_info = self.__detach(cube, attached_iface)
                detached_info = self.__attach(cube, interface)
                req_path = 'dynmon/{cube}/dataplane-config'
            resp_req = put_req(f'{self.endpoint}/{req_path}',
                               json=self.__dataplane_config(cube, code,
                                                            metrics),
                               timeout=self.timeout)
            self.__manager(resp_req)
            return dict(status='updated', attached_info=attached_info,
                        detached_info=detached_info,
                        data=data, **self.__from_resp(resp_req))
        except Exception as e:
            self.log.exception(f'Cube {cube} not updated', e)
            return dict(status='error', attached_info=attached_info,
                        detached_info=detached_info,
                        data=data, **self.__from_resp(resp_req,
                                                      error=True))

    @staticmethod
    def __dataplane_config(cube, code, metrics):
        return {
            'ingress-path': {
                'name': cube,
                'code': code,
                'metric-configs': metrics
            },
            'egress-path': {}
        }

    def __from_resp(self, resp, error=None):
        error = error if error is not None else resp.status_code >= 400

        if not resp.content:
            return {'error': error}

        try:
            return loads(resp.content)
        except Exception:
            return {'error': error, 'message': resp.content.decode("utf-8")}

    def __detach(self, cube, interface):
        return self.__extracted_from___attach_2('/detach', cube,
                                                interface, 'detached')

    def __attach(self, cube, interface):
        return self.__extracted_from___attach_2('/attach', cube,
                                                interface, 'attached')

    # TODO Rename this here and in `__detach` and `__attach`
    def __extracted_from___attach_2(self, arg0, cube, interface, status):
        resp_req = post_req(
            f'{self.endpoint}{arg0}',
            json={'cube': cube, 'port': interface},
            timeout=self.timeout,
        )

        self.__manager(resp_req)
        return dict(
            status=status,
            data={'cube': cube, 'interface': interface},
            **self.__from_resp(resp_req)
        )

    def __manager(self, resp_req):
        try:
            resp_req.raise_for_status()
        except ConnectionError as e:
            _msg = MSG_CONN_NOT_POSSIBLE.format(self.endpoint)
            self.log.exception(_msg, e)
            if resp_req.content:
                self.log.error(f'Response: {resp_req.content}')
            raise HTTP_Service_Unavailable(title='Connection error',
                                           description=_msg)
        except Timeout as e:
            timeout = ArgReader.db.polycube_timeout
            _msg = MSG_RESP_NOT_RECV.format(self.endpoint, timeout)
            self.log.exception(_msg, e)
            if resp_req.content:
                self.log.error(f'Response: {resp_req.content}')
            raise HTTP_Gateway_Timeout(title='Polycube Unavailable',
                                       description=_msg)
