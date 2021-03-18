from resource.code import *
from resource.config import *
from resource.status import *
from resource.filiation import *
from resource.hardware_definitions import *
from resource.software_definition import *
from resource.security_functions import *
from resource.cloud_resource import *
from resource.self_data import *
from utils.log import Log
from utils.sequence import wrap

__all__ = [
    'routes'
]

db = (
    Code_Resource,
    Config_Resource,
    Status_Resource,
    SonRequestIdentificationById,
    SonLCPIdentification,
    BaremetalServer,
    VirtualServer,
    SoftwareDefinition,
    SecurityFunction,
    CloudInfrastructure,
    DescribeDeploymentBareMetal,
    DescribeDeploymentVM,
    DescribeSelf,
    ParentLCPIdentification
)

tags = []
for Resource in db:
    tags.append(Resource.tag)


def routes(api, spec):
    log = Log.get('resource')
    for res_class in db:
        res = res_class()
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            spec.path(resource=res)
            log.success(f'{route} endpoint configured')
