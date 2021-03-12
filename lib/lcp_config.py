import os
import yaml

from schema.filiation import LCPSonDescription
from schema.filiation import ContextBrokerConnection
from urllib.parse import urlparse

class LCPConfig(object):
    class __LCPConfig:
        def __init__(self, filename):
            self.config = None
            self.filename = filename
            self.lcp = None
            self.sons = []
            self.parents = []
            self.contextBroker = None
            self.user = ""
            self.password = ""
            self.deployment = {}
            self.agents = []
            self.testing = False
            self.reload(self.filename)

        def save(self):
            if self.testing:
                return
            with open(self.filename, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)

        def reload(self, filename=None):
            if filename is not None:
                self.filename = os.path.expanduser(filename)
            else:
                default_file_config = os.path.expanduser("~/.guard_apis/LCPConfig.yaml")
                if os.path.exists(default_file_config):
                    self.filename = default_file_config
                else:
                    self.filename = "config/LCPConfig.yaml"

            with open(self.filename, "r") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)

            lcp_schema = LCPSonDescription(many=False)

            # Debe contener al menos los datos de este LCP
            lcp_schema.load(self.config['lcp'])
            self.lcp = self.config['lcp']

            # Parents:
            if 'lcp_parents' in self.config and len(self.config['lcp_parents']) > 0:
                # lcp_schema = LCPSonDescription(many=True)
                # lcp_schema.load(self.config['lcp_parents'])
                self.parents = self.config['lcp_parents']

            # Sons:
            if 'lcp_sons' in self.config and len(self.config['lcp_sons']) > 0:
                lcp_schema = LCPSonDescription(many=True)
                lcp_schema.load(self.config['lcp_sons'])
                self.sons = self.config['lcp_sons']

            self.lcp = self.config['lcp']

            # Context Broker
            if 'context_broker' in self.config and len(self.config['context_broker']) > 0:
                cb_schema = ContextBrokerConnection(many=False)
                cb_schema.load(self.config['context_broker'])
                self.contextBroker = self.config['context_broker']

            if 'agents' not in self.config:
                self.config['agents'] = []
                self.agents = self.config['agents']

            try:
                self.user = self.config['user']
                self.password = self.config['password']
            except KeyError:
                pass

            self.deployment = self.config['deployment'] if 'deployment' in self.config else {}


        def setDeployment(self, dictDeployment):
            self.config['deployment'] = dictDeployment
            self.save()


        def setAgent(self, elem):
            updated = False
            for i in range(0, len(self.agents)):
                if self.agents[i]["id"] == elem["id"]:
                    updated = True
                    self.agents[i] = elem
            if not updated:
                self.agents.append(elem)
            self.save()


        def dropAllAgents(self):
            self.config['agents'] = []
            self.agents = self.config['agents']
            self.save()


        def getDataForRegisterOnCB(self):
            parsed_uri = urlparse(self.lcp['url'])
            port = parsed_uri.port

            if port is None:
                port = 80 if parsed_uri.scheme == 'http' else 443

            hostname = parsed_uri.hostname
            enabled = "Yes"
            description = self.config['description'] if 'description' in self.config else None
            deployment_type = self.config['type'] if 'type' in self.config else None

            data = {
                "id": self.lcp['id'],
                "enabled": "yes",
                "hostname": hostname,
                "lcp": {
                    "port": port,
                    "username": self.user,
                    "password": self.password
                }
            }

            if description is not None:
                data['description'] = description
            if deployment_type is not None:
                data['type'] = deployment_type
            else:
                data['type'] = 'unknown'
            return data

    instance = None

    def __new__(cls, filename=None, *args, **kwargs):
        if LCPConfig.instance is None:
            LCPConfig.instance = LCPConfig.__LCPConfig(filename)
        return LCPConfig.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
