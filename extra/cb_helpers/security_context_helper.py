import json
from extra.extra_utils import UrlSchemaData


class SecurityContextHelper:
    def __init__(self, config):
        if config.lcp is None:
            raise KeyError('unconfigured LCP')

        self.security_context = {}
        self.security_context['executionEnvironmentType'] = config.exec_env_type
        self.security_context['lcp'] = self.setLcpData(config.lcp)

        if len(config.sons) > 0:
            self.security_context['lcp']['hasSons'] = []
            self.security_context['lcpSons'] = []
            for son in config.sons:
                print(son)
                self.security_context['lcpSons'].append(self.setLcpData(son))
                self.security_context['lcp']['hasSons'].append(son['id'])
        if len(config.parents) > 0:
            self.security_context['lcpParent'] = config.parents[0]

        if len(config.self_software) > 0:
            self.security_context['software'] = config.self_software.copy()

        self.security_context['executionEnvironment'] = config.deployment.copy()

        if len(config.self_containers) > 0:
            self.security_context['container'] = config.self_containers.copy()

        if len(config.agent_types) > 0:
            self.security_context['agentType'] = config.agent_types.copy()
            if len(config.agents) > 0:
                self.security_context['agentInstance'] = config.agents.copy()


    def getData(self):
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
        d['lcp'] = lcp_info
        # d['partner'] = "FIWARE Foundation e.V."
        if "exec_env_type" in lcp:
            d['type_id'] = lcp['exec_env_type']
        print("Testing URL:", lcp['url'])
        usd = UrlSchemaData(lcp['url'])
        lcp_info['port'] = usd.port
        lcp_info['https'] = usd.https
        d['hostname'] = usd.host

        return d

