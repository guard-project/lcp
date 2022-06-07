import json
from extra.extra_utils import UrlSchemaData
from schema.poll_cb_schema import LCPConnectionAsInCB, LCPContextBrokerDefinition, PollSchema
from schema.hardware_definitions import ExecutionEnvironment


class SecurityContextHelper:
    def __init__(self, config):
        if config.lcp is None:
            raise KeyError('unconfigured LCP')

        self.security_context = {}
        # self.security_context['executionEnvironmentType'] = config.exec_env_type
        self.security_context['exec_env'] = self.setLcpData(config.lcp)

        if len(config.sons) > 0:
            self.security_context['exec_env']['lcp']['sons'] = []
            self.security_context['lcpSons'] = []
            for son in config.sons:
                self.security_context['lcpSons'].append(self.setLcpData(son))
                self.security_context['exec_env']['lcp']['sons'].append(son['id'])
        if len(config.parents) > 0:
            self.security_context['exec_env']['lcp']['father'] = config.parent_lcp_data['id']

        if len(config.self_software) > 0:
            self.security_context['exec_env']['sw_info'] = config.self_software.copy()

        self.security_context['exec_env']['hw_info'] = config.deployment.copy()

        if len(config.self_containers) > 0:
            self.security_context['exec_env']['container'] = config.self_containers.copy()

        if len(config.agent_types) > 0:
            d = config.agent_types.copy()
            self.security_context['agentType'] = []
            for a in d:
                if a['schema'] != 'cb-defined':
                    self.security_context['agentType'].append(a)
            if len(config.agents) > 0:
                self.security_context['agentInstance'] = config.agents.copy()

        self.security_context['exec_env']['interactions'] = config.interactions
        self.security_context['exec_env']['network_links'] = self.get_network_links(config)

        if config.cloud:
            self.security_context['cloud'] = config.cloud

    def get_network_links(self, config):
        r = []
        for f in config.network_links:
            if 'remoteExecutionEnvironmentId' in f:
                r.append({
                    "id": f['id'],
                    "type_id": f['networkLinkType'],
                    "description": f"link from exec-env {f['exec_env_id']} to exec-env {f['remoteExecutionEnvironmentId']}"
                })
            elif 'remoteArtifactId' in f:
                r.append({
                    "id": f['id'],
                    "type_id": f['networkLinkType'],
                    "description": f"link from exec-env {config.lcp['id']} to remote artifact {f['remoteArtifactId']}"
                })
        return r

    def getData(self):
        PollSchema(many=False).load(self.security_context)
        return json.dumps(self.security_context)


    def setLcpData(self, lcp):
        d = {}
        lcp_info = {}
        d['id'] = lcp['id']
        d['description'] = lcp['description']
        d['enabled'] = True

        # d['hostname'] = self.deployment['hostname']
        # TODO - Change the partner!
        # d['stage'] = ""
        d['lcp'] = {}
        # d['partner'] = "FIWARE Foundation e.V."
        # if "exec_env_type" in lcp:
        d['type_id'] = lcp['exec_env_type']
        usd = UrlSchemaData(lcp['url'])
        d['lcp']['port'] = usd.port
        d['lcp']['https'] = usd.https

        d['hostname'] = usd.host

        return d
