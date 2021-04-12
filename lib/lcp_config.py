import os
import yaml

from schema.filiation import LCPDescription
from schema.filiation import ContextBrokerConnection
from urllib.parse import urlparse

CONTEXT_BROKER='context_broker'

class LCPConfig(object):
    class __LCPConfig:
        def __init__(self, filename):
            self.filename = filename
            self.reset()

        def save(self):
            if self.testing:
                return
            with open(self.filename, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)

        def reset(self):
            self.config = None
            self.lcp = None
            self.sons = []
            self.parents = []
            self.contextBroker = None
            self.user = ""
            self.password = ""
            self.deployment = {}
            self.agents = []
            self.testing = False
            self.children_requested = []
            self.self_software = []
            self.self_containers = []
            self.reload(self.filename)


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

            lcp_schema = LCPDescription(many=False)

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
                lcp_schema = LCPDescription(many=True)
                lcp_schema.load(self.config['lcp_sons'])
                self.sons = self.config['lcp_sons']

            self.lcp = self.config['lcp']

            # Context Broker
            if CONTEXT_BROKER in self.config and len(self.config[CONTEXT_BROKER]) > 0:
                cb_schema = ContextBrokerConnection(many=False)
                cb_schema.load(self.config[CONTEXT_BROKER])
                self.contextBroker = self.config[CONTEXT_BROKER]

            if 'agents' not in self.config:
                self.config['agents'] = []
                self.agents = self.config['agents']
            else:
                self.agents = self.config['agents']

            try:
                self.user = self.config['user']
                self.password = self.config['password']
            except KeyError:
                pass

            try:
                self.self_software = self.config["self_software"]
            except KeyError:
                self.config["self_software"] = self.self_software

            try:
                self.self_containers = self.config["self_containers"]
            except KeyError:
                self.config["self_containers"] = self.self_containers

            try:
                self.children_requested = self.config['lcp_request_as_sons']
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

        def setSoftware(self, elem):
            updated = False
            for i in range(0, len(self.self_software)):
                if self.self_software[i]["id"] == elem["id"]:
                    updated = True
                    self.self_software[i] = elem
                    break
            if not updated:
                self.self_software.append(elem)
            self.save()


        def setContainers(self, elem):
            updated = False
            for i in range(0, len(self.self_containers)):
                if self.self_containers[i]["id"] == elem["id"]:
                    updated = True
                    self.self_containers[i] = elem
                    break
            if not updated:
                self.self_containers.append(elem)
            self.config["self_containers"] = self.self_containers
            self.save()


        def setParent(self, elem):
            updated = False
            if not elem['url'] in self.parents:
                self.parents.append(elem['url'])
                self.config['lcp_parents'] = self.parents
                updated = True
            self.save()

        def setSon(self, elem):
            updated = False
            for i in range(0, len(self.sons)):
                if self.sons[i]["id"] == elem["id"]:
                    updated = True
                    self.sons[i] = elem
            if not updated:
                self.sons.append(elem)
            self.config['lcp_sons'] = self.sons
            self.save()

        def getSonById(self, son_id):
            for i in range(0, len(self.sons)):
                if self.sons[i]["id"] == son_id:
                    d = self.sons[i]
                    return d
            return None

        def deleteSonById(self, son_id):
            d = self.getSonById(son_id)
            if d is not None:
                self.sons.remove(d)
                self.save()
            return d

        def deleteAllSons(self):
            self.sons = []
            self.save()


        def dropAllAgents(self):
            self.config['agents'] = []
            self.agents = self.config['agents']
            self.save()

        def setContextBroker(self, data):
            self.config[CONTEXT_BROKER] = data
            self.contextBroker = self.config[CONTEXT_BROKER]
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
