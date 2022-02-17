from resource.code import CodeResource
from resource.config import ConfigResource
from resource.status import StatusResource
from resource.software_definition import SoftwareDefinition, SoftwareDefinitionById, ContainerDefinition
from resource.lcp_resources import SonRequestIdentificationById, SonLCPIdentification, ParentLCPIdentification
from resource.cloud_resource import CloudInfrastructure
from resource.security_functions import SecurityFunction, AgentTypeResource, SecurityFunctionbyId, AgentTypeResourcebyId
from resource.self_data import DescribeDeployment, DescribeSelf, InitialSelfConfiguration
from resource.poll_cb import PollContextBroker
from resource.interacts import Interacts, InteractsById
from utils.log import Log
from utils.sequence import wrap

db = (CodeResource, ConfigResource, StatusResource,
      SoftwareDefinition, SoftwareDefinitionById, ContainerDefinition,
      SonRequestIdentificationById, SonLCPIdentification, ParentLCPIdentification,
      CloudInfrastructure,
      SecurityFunction, AgentTypeResource, SecurityFunctionbyId, AgentTypeResourcebyId,
      SoftwareDefinition,
      DescribeDeployment, DescribeSelf, InitialSelfConfiguration,
      Interacts, InteractsById, PollContextBroker)

tags = [Resource.tag for Resource in db]


def routes(api, spec):
    log = Log.get("resource")
    for res_class in db:
        res = res_class()
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            spec.path(resource=res)
            log.success(f"{route} endpoint configured")
