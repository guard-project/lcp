from schema.network_link import NetworkLink
from test_utils import *
from test.testbase import LCPTestBase


class TestMyNetworkLink(LCPTestBase):
    def test_config_network_links(self):
        lcp_config = getLCPConfig()
        assert lcp_config.network_links == []

    def add_son_lcps(self, lcp_config):
        son_lcps = loadExampleFile("FiliatedLCPsNetworkLink.json")

        for son in son_lcps:
            lcp_config.setSon(son)

    def test_network_link_to_sons(self):
        lcp_config = getLCPConfig()

        self.add_son_lcps(lcp_config)

        assert len(lcp_config.network_links) == 2

        assert 'remoteExecutionEnvironmentId' in lcp_config.network_links[0]
        assert 'remoteExecutionEnvironmentId' in lcp_config.network_links[1]


    def add_remote_config(self, lcp_config):
        remote_artifacts = loadExampleFile("interactions.json")

        if 'externalStorage' in remote_artifacts:
            for ext_con in remote_artifacts['externalStorage']:
                lcp_config.add_external_storage_interaction(ext_con)
        if 'softwareArtifacts' in remote_artifacts:
            for ext_sw in remote_artifacts['softwareArtifacts']:
                lcp_config.add_external_software_interaction(ext_sw)


    def test_network_link_to_remote_artifact(self):
        lcp_config = getLCPConfig()

        self.add_remote_config(lcp_config)
        assert len(lcp_config.network_links) == 2
        assert 'remoteArtifactId' in lcp_config.network_links[0]
        assert 'remoteArtifactId' in lcp_config.network_links[1]


    def test_poll_query(self):
        lcp_config = getLCPConfig()
        self.add_remote_config(lcp_config)
        self.add_son_lcps(lcp_config)

        headers = getAuthorizationHeaders()
        result = self.simulate_get("/poll", headers=headers)

        nl = result.json['exec_env']['network_links']
        print(type(nl))

        assert result.status == "200 OK"
        assert len(nl) == 4


    def test_parent_lcp(self):
        lcp_config = getLCPConfig()
        parent = loadExampleFile("FiliatedLCPsNetworkLink.json")

        lcp_config.set_parent_lcp_data(parent[1])
        assert len(lcp_config.network_links) == 1

        assert lcp_config.network_links[0]['exec_env_id'] == parent[1]['id']
        assert lcp_config.network_links[0]['remoteExecutionEnvironmentId'] == lcp_config.lcp['id']
