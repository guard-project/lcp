from resource.code import *
from resource.config import *
from resource.status import *
from resource.filiation import *
from resource.hardware_definitions import *
from utils.log import Log
from utils.sequence import wrap

__all__ = [
    'routes'
]

db = (
    Code_Resource,
    Config_Resource,
    Status_Resource,
    FiliationById,
    Filiation,
    BaremetalServer
)

tags = []
for Resource in db:
    print("** - tags.append:", Resource.tag)
    tags.append(Resource.tag)


def routes(api, spec):
    log = Log.get('resource')
    for res_class in db:
        res = res_class()
        print("...",res_class.routes)
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            print("... SPEC:",spec)
            print("... RES :",res)
            spec.path(resource=res)
            log.success(f'{route} endpoint configured')
