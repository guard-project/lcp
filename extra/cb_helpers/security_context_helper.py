import json


class SecurityContextHelper:
    def __init__(self, config):
        if config.lcp is None:
            raise KeyError('unconfigured LCP')

        self.security_context = {}
        self.security_context['executionEnvironmentType'] = config.exec_env_type
        self.security_context['lcp'] = config.lcp.copy()
        self.security_context['lcp']['executionEnvironmentType'] = config.exec_env_type

        if len(config.sons) > 0:
            self.security_context['lcpSons'] = config.sons.copy()
            self.security_context['lcp']['hasSons'] = []
            for son in self.security_context['lcpSons']:
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
