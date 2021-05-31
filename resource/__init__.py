from resource.code import Code_Resource
from resource.config import Config_Resource
from resource.status import Status_Resource
from resource.software_definition import SoftwareDefinition, ContainerDefinition
from resource.lcp_resources import SonRequestIdentificationById, SonLCPIdentification, ParentLCPIdentification
from resource.hardware_definitions import LXCContainer
from resource.cloud_resource import CloudInfrastructure
from resource.security_functions import SecurityFunction, AgentTypeResource
from resource.self_data import DescribeDeployment, DescribeSelf, InitialSelfConfiguration
from utils.log import Log
from utils.sequence import wrap


db = (Code_Resource, Config_Resource, Status_Resource,
      SoftwareDefinition, ContainerDefinition,
      SonRequestIdentificationById, SonLCPIdentification, ParentLCPIdentification,
      CloudInfrastructure,
      SecurityFunction, AgentTypeResource,
      SoftwareDefinition,
      DescribeDeployment, DescribeSelf, InitialSelfConfiguration)

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
