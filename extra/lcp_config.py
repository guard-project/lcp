import os
import yaml
from pathlib import Path

from schema.lcp_schemas import LCPDescription
from urllib.parse import urlparse
from extra.extra_utils import UrlSchemaData

from utils.log import Log

CONTEXT_BROKER = 'context_broker'


class LCPConfig(object):
    class __LCPConfig:
        def __init__(self, filename):
            self.filename = filename
            self.log = Log.get('LCPConfig')
            self.reset()

        def save(self):
            if self.testing:
                return
            if not os.path.exists(self.filename):
                try:
                    os.mkdir(os.path.dirname(self.filename))
                except FileExistsError:
                    pass

            with open(self.filename, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)

        def purge(self):
            self.config = {}
            self.lcp = None
            self.sons = []
            self.parents = []
            self.user = ""
            self.password = ""
            self.deployment = {}
            self.agents = []
            self.testing = False
            self.children_requested = []
            self.self_software = []
            self.self_containers = []
            self.exec_env_type = None
            self.agent_types = []
            self.interactions = {"softwareArtifacts": [], "externalStorage": []}
            self.parent_lcp_data = {}
            self.cloud = {}
            self.network_links = []

            self.save()
            self.reload(self.filename)


        def reset(self):
            self.config = {}
            self.lcp = None
            self.sons = []
            self.parents = []
            self.user = ""
            self.password = ""
            self.deployment = {}
            self.agents = []
            self.testing = False
            self.children_requested = []
            self.self_software = []
            self.self_containers = []
            self.exec_env_type = None
            self.agent_types = []
            self.interactions = {"softwareArtifacts": [], "externalStorage": []}
            self.parent_lcp_data = {}
            self.cloud = {}
            self.network_links = []

            # Reload the configuration.
            self.reload(self.filename)

        def merge_dicts(d1, d2):
            if d1 == d2:
                return False
            d1.update(d2)
            return True

        def has_extra_features(self):
            if self.lcp is not None and 'lcp' in self.lcp:
                return True
            return False

        def reload(self, filename=None):
            if filename is not None:
                self.filename = os.path.expanduser(filename)
            else:
                default_file_config = os.path.expanduser("~/.guard_apis/LCPConfig.yaml")
                if os.path.exists(default_file_config):
                    self.filename = default_file_config
                else:
                    self.filename = "config/LCPConfig.yaml"

            try:
                with open(self.filename, "r") as f:
                    self.config = yaml.load(f, Loader=yaml.FullLoader)
            except Exception:
                return

            # Should at least contain some lcp info
            if self.config is None:
                self.config = {}

            if 'lcp' not in self.config:
                return

            lcp_schema = LCPDescription(many=False)
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

            try:
                self.exec_env_type = self.config['type']
            except KeyError:
                pass

            try:
                self.agent_types = self.config['agent_types']
            except KeyError:
                pass

            try:
                self.parent_lcp_data = self.config['parent_lcp_data']
                if len(self.parents) > 1:
                    self.parents[0] = self.parent_lcp_data['url']
            except KeyError:
                pass

            try:
                if 'interactions' in self.config:
                    self.interactions = self.config['interactions']
            except KeyError:
                pass

            try:
                if 'cloud' in self.config:
                    self.cloud = self.config['cloud']
            except KeyError:
                pass

            try:
                if 'network_links' in self.config:
                    self.network_links = self.config['network_links']
            except KeyError:
                pass

            self.deployment = self.config['deployment'] if 'deployment' in self.config else {}

        def add_external_storage_interaction(self, storage):
            updated = False
            for s in self.interactions['externalStorage']:
                if s['id'] == storage['id']:
                    s.update(storage)
                    updated = True
            if not updated:
                self.interactions['externalStorage'].append(storage)
                self.setNetworkLink(self.lcp['id'], storage['id'], as_son=False)
            self.config['interactions'] = self.interactions
            self.save()

        def delete_external_storage_interaction(self, id):
            found = False
            for s in self.interactions['externalStorage']:
                if s['id'] == id:
                    self.interactions['externalStorage'].remove(s)
                    found = True
                    break
            self.save()
            return found

        def add_external_software_interaction(self, software):
            updated = False
            for s in self.interactions['softwareArtifacts']:
                if s['id'] == software['id']:
                    s.update(software)
                    updated = True
            if not updated:
                self.interactions['softwareArtifacts'].append(software)
                self.setNetworkLink(self.lcp['id'], software['id'], as_son=False)
            self.config['interactions'] = self.interactions
            self.save()

        def delete_external_software_interaction(self, id):
            found = False
            for s in self.interactions['softwareArtifacts']:
                if s['id'] == id:
                    self.interactions['softwareArtifacts'].remove(s)
                    found = True
                    break
            self.save()
            return found

        def getInteractionById(self, id):
            for s in self.interactions['softwareArtifacts']:
                if s['id'] == id:
                    res = {'softwareArtifacts':  s.copy()}
                    return res

            for s in self.interactions['externalStorage']:
                if s['id'] == id:
                    res = {'externalStorage':  s.copy()}
                    return res
            return None


        def setInitialConfiguration(self, dict_cfg):
            should_start_thread = False
            if self.lcp is None:
                self.lcp = {}
            d = dict_cfg
            self.lcp = {**self.lcp, **d}
            self.config['lcp'] = self.lcp

            self.save()
            return should_start_thread

        def setDeployment(self, dictDeployment):
            self.deployment = dictDeployment['environment']
            self.config['deployment'] = self.deployment
            self.config['type'] = dictDeployment['executionType']
            self.exec_env_type = dictDeployment['executionType']
            self.save()

        def set_agent_type(self, elem):
            updated = False
            for i in range(0, len(self.agent_types)):
                if self.agent_types[i]['id'] == elem['id']:
                    updated = True
                    self.agent_types[i] = elem
            if not updated:
                self.agent_types.append(elem)
                self.config['agent_types'] = self.agent_types

            self.save()

        def get_agent_type_by_id(self, id):
            for a in self.agent_types:
                if a['id'] == id:
                    return a
            return None

        def delete_agent_type_by_id(self, id):
            for a in range(0, len(self.agent_types)):
                if self.agent_types[a]['id'] == id:
                    self.agent_types.pop(a)
                    return True
            return False

        def find_agent_type(self, id):
            for i in range(0, len(self.agent_types)):
                if self.agent_types[i]['id'] == id:
                    return self.agent_types[i]
            return None

        def set_agent(self, elem):
            updated = False
            for i in range(0, len(self.agents)):
                if self.agents[i]["id"] == elem["id"]:
                    updated = True
                    self.agents[i] = elem
            if not updated:
                self.agents.append(elem)
            self.save()

        def get_agent_instance_by_id(self, a_id):
            for a in range(0, len(self.agents)):
                if self.agents[a]["id"] ==  a_id:
                    return self.agents[a]

            return None

        def delete_agent_instance_by_id(self, a_id):
            for a in range(0, len(self.agents)):
                if self.agents[a]["id"] == a_id:
                    self.agents.pop(a)
                    return True

            return False

        def exists_agent_instance_by_type(self, a_type):
            for a in self.agents:
                if a['hasAgentType'] == a_type:
                    return True
            return False


        def set_software(self, elem):
            updated = False
            for i in range(0, len(self.self_software)):
                if self.self_software[i]["id"] == elem["id"]:
                    updated = True
                    self.self_software[i] = elem
                    break
            if not updated:
                self.self_software.append(elem)
            self.save()


        def set_containers(self, elem):
            updated = False
            if self.self_containers is None:
                self.self_containers = []

            for i in range(0, len(self.self_containers)):
                if self.self_containers[i]["id"] == elem["id"]:
                    updated = True
                    self.self_containers[i] = elem
                    break
            if not updated:
                self.self_containers.append(elem)
            self.config["self_containers"] = self.self_containers
            self.save()


        def get_container_by_id(self, c_id):
            if self.self_containers is None:
                self.self_containers = []

            for i in self.self_containers:
                if i["id"] == c_id:
                    return i

            return None

        def delete_container_by_id(self, c_id):
            if self.self_containers is None:
                self.self_containers = []

            for i in range(0, len(self.self_containers)):
                if self.self_containers[i]["id"] == c_id:
                    self.self_containers.pop(i)
                    return True

            return False

        def setParent(self, elem):
            updated = False
            if len(self.parents) > 0 and not elem['url'] == self.parents[0]:
                return False
            if not elem['url'] in self.parents:
                self.parents.append(elem['url'])
                self.config['lcp_parents'] = self.parents
                updated = True
            self.save()
            return True


        def removeParent(self, elem):
            found = False
            if not elem in self.parents:
                print(f"{elem} -- NOT FOUND")
                return False
            else:
                print(f"{elem} -- YES FOUND")
                self.parents=[]
                self.parent_lcp_data = {}
                self.network_links = []
                self.generate_network_links()
                return True
            return False


        def setNetworkLink(self, exec_env_id, a_id, as_son=True):
            nl_id = f"{exec_env_id}-{a_id}"

            for m in self.network_links:
                if m['id'] == nl_id:
                    return

            nl = {"type": "NetworkLink",
                  "exec_env_id": exec_env_id,
                  "id": nl_id,
                  "networkLinkType": "pnt2pnt"}

            if as_son:
                nl["remoteExecutionEnvironmentId"] = a_id
            else:
                nl["remoteArtifactId"] = a_id

            self.network_links.append(nl)
            self.config['network_links'] = self.network_links


        def generate_network_links(self):
            if not self.network_links == []:
                return

            if len(self.sons) > 0:
                for son in self.sons:
                    self.setNetworkLink(self.lcp['id'], son['id'])

            if not self.parent_lcp_data == {}:
                self.setNetworkLink(self.parent_lcp_data['id'], self.lcp['id'])

            if not self.interactions['softwareArtifacts'] == []:
                for i in self.interactions['softwareArtifacts']:
                    self.setNetworkLink(self.lcp['id'], i[id], as_son=False)

            if not self.interactions['externalStorage'] == []:
                for i in self.interactions['externalStorage']:
                    self.setNetworkLink(self.lcp['id'], i[id], as_son=False)

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
            self.setNetworkLink(self.lcp['id'], elem['id'])
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
                self.network_links = []
                self.generate_network_links()
                self.save()
            return d

        def deleteAllSons(self):
            self.sons = []
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

        def get_software_by_id(self, id):
            for s in self.self_software:
                if s['id'] == id:
                    return s.copy()
            return None

        def delete_software_by_id(self, id):
            found = False
            for s in self.self_software:
                if s['id'] == id:
                    self.self_software.remove(s)
                    found = True
                    break
            self.save()
            return found


        def exec_env_register_data(self):
            d = {}
            lcp_info = {}
            d['id'] = self.lcp['id']
            d['description'] = self.lcp['description']
            d['enabled'] = True
            # d['hostname'] = self.deployment['hostname']
            # TODO - Change the partner!
            d['stage'] = ""
            d['lcp'] = lcp_info
            d['partner'] = "FIWARE Foundation e.V."
            d['type_id'] = self.exec_env_type

            usd = UrlSchemaData(self.lcp['url'])
            lcp_info['port'] = usd.port
            lcp_info['https'] = usd.https
            d['hostname'] = usd.host

            return d

        def dump(self):
            pass

        def agent_register_data(self):
            res = []
            if not len(self.agents) > 0:
                return []

            for a in self.agents:
                agent = {}
                if 'description' in a:
                    agent['description'] = a['description']
                agent['id'] = a['id']

        def agent_catalog_register(self):
            res = []
            if not len(self.agents) > 0:
                return []

        def set_parent_lcp_data(self, data):
            self.parent_lcp_data = data
            self.config['parent_lcp_data'] = self.parent_lcp_data
            self.setNetworkLink(self.parent_lcp_data['id'], self.lcp['id'], True)
            self.save()

        def set_cloud(self, data):
            self.cloud = data
            self.config['cloud'] = self.cloud
            self.save()


    instance = None

    def __new__(cls, filename=None):
        if LCPConfig.instance is None:
            LCPConfig.instance = LCPConfig.__LCPConfig(filename)
        return LCPConfig.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    @classmethod
    def __drop_it__(self, filename):
        if LCPConfig.instance is None:
            LCPConfig(filename)
        LCPConfig.instance.filename
        LCPConfig.instance.reload
