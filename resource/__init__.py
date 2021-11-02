from resource.code import CodeResource
from resource.config import ConfigResource
from resource.status import StatusResource

from utils.log import Log
from utils.sequence import wrap

db = (CodeResource, ConfigResource, StatusResource)

tags = [Resource.tag for Resource in db]


def routes(api, spec):
    log = Log.get('resource')
    for res_class in db:
        res = res_class()
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            spec.path(resource=res)
            log.success(f'{route} endpoint configured')
