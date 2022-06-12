import time

from schema.lcp_schemas import LCPDescription
from resource import SonLCPIdentification
from test_utils import *
from extra.lcp_client import LCPClient, LCPMessages, BetweenLCPMessages
from queue import Empty
import requests
from test.testbase import LCPTestBase


class TestMyApp(LCPTestBase):
    def _getFiliationData(self):
        uuid = "94216230-ae26-464c-9541-cc0ca62cd1ce"
        url = "https://example.url.com:4443"
        name = "lcp:example"
        d_type = "LCPDescription"
        description = "Some descriptiont goes here"
        body_dict = {"id": uuid, "type": d_type, "url": url, "name": name, "description": description}
        return uuid, url, body_dict

    def _setFiliationData(self):
        uuid, url, body_dict = self._getFiliationData()
        cfg = getLCPConfig()
        cfg.setSon(body_dict)
        return uuid, url, body_dict

    def _setMultiFiliationData(self):
        uuids = ["49157b82-1962-4054-9862-989d61c4ff02", "04400853-c48d-47f7-9472-efdb8e877991", "066c121c-279d-4877-9e0b-ccd5f2a2d858"]
        urls = ["http://hst1.domain1.com", "http://hst2.domain2.com", "http://hst3.domain3.com"]
        names = ["lcp:host01", "lcp:host02", "lcp:host03"]
        cfg = getLCPConfig()
        for i in range(3):
            cfg.setSon({"id": uuids[i], "url": urls[i], "name": names[i], "type": "LCPDescrition"})

    def test_get_sons(self):
        headers = getAuthorizationHeaders()
        SonLCPIdentification.data = {}
        config = getLCPConfig()
        config.deleteAllSons()

        # With Authorization header, get empy list:
        result = self.simulate_get("/lcp_son", headers=headers)
        assert (result.status == "200 OK")
        sons = result.json
        assert type(sons) is list
        assert len(sons) == 0

        uuid, url, body_dict = self._setFiliationData()
        result = self.simulate_get("/lcp_son", headers=headers)
        assert (result.status == "200 OK")
        sons = result.json
        assert len(sons) == 1
        assert sons[0]['id'] == uuid
        assert sons[0]['url'] == url

        self._setMultiFiliationData()
        result = self.simulate_get("/lcp_son", headers=headers)
        assert (result.status == "200 OK")
        sons = result.json
        assert len(sons) == 4

    def test_get_filiation_by_id(self):
        headers = getAuthorizationHeaders()

        result = self.simulate_get("/lcp_son/134", headers=headers)
        assert (result.status == "404 Not Found")

        uuid, url, body_dict = self._setFiliationData()
        result = self.simulate_get(f"/lcp_son/{uuid}", headers=headers)
        assert (result.status == "200 OK")
        payload = result.json
        assert(payload['id'] == uuid)
        assert(payload['url'] == url)

    def test_post_filiation(self):
        # No Authorization for request:
        id, url, body_dict = self._getFiliationData()
        lcp_info = LCPDescription()
        body = lcp_info.dump(body_dict)

        # With Authorization header + OK data -- Expected: 201 Created
        headers = getAuthorizationHeaders()
        print(body)
        result = self.simulate_post("/lcp_son", headers=headers, body=json.dumps(body))
        print("STATUS:", result.status)
        print("JSON:", result.json)
        assert(result.status == "201 Created")

        # Fake thing. Not a correct data -- Expected: 406 Not Acceptable
        body_fake = '{"whatever": "something wrong", "other_thing": "just_fail_this"}'
        result = self.simulate_post("/lcp_son", headers=headers, body=body_fake)
        assert(result.status == "406 Not Acceptable")

        # Bad URL. Not correct URL.
        body_dict["url"] = "this is not an url"
        body = lcp_info.dump(body_dict)
        result = self.simulate_post("/lcp_son", headers=headers, body=json.dumps(body))
        assert(result.status == "406 Not Acceptable")

    def test_post_multi(self):
        body = loadExampleFile("FiliatedLCPs.json")
        headers = getAuthorizationHeaders()

        result = self.simulate_post("/lcp_son", headers=headers,
                                    body=json.dumps(body))
        print(result.status)
        assert result.status == "201 Created"

        result = self.simulate_get("/lcp_son", headers=headers)
        assert result.status == "200 OK"

    def test_delete_message(self):
        uuid, url, body_dict = self._getFiliationData()
        headers = getAuthorizationHeaders()
        cfg = getLCPConfig()

        # Try delete with authorization, but non existent
        result = self.simulate_delete(f"/lcp_son/12345", headers=headers)
        assert (result.status == "404 Not Found")

        self._setMultiFiliationData()
        self._setFiliationData()
        assert cfg.getSonById(uuid) is not None
        result = self.simulate_delete(f"/lcp_son/{uuid}", headers=headers)
        assert (result.status == "200 OK")
        assert cfg.getSonById(uuid) is None

    def test_post_parent(self):
        parent = {"url": "http://example.com"}
        lcp_client = LCPClient()
        headers = getAuthorizationHeaders()
        cfg = getLCPConfig()

        lcp_client.q.queue.clear()

        result = self.simulate_post("/lcp_parent", headers=headers, body=json.dumps(parent))
        assert result.status == "202 Accepted"
        try:
            message = lcp_client.q.get(timeout=3)
            print("Message.message_type:",message.message_type)
            assert message.message_type == BetweenLCPMessages.PostLCPSon
            assert message.data['url'] == parent['url']
            assert len(cfg.parents) == 1
            assert cfg.parents[0] == parent['url']
        except Empty:
            assert False

    def test_send_parent_message_to_lcp(self):
        """
        This summulate that we are an LCP parent with our own http server on localhost:8448
        1. Simulate sending a message to LCPSon as a parent to it
        2. Reads within 5 seconds if the LCPSon, after recieving the simulated messages sends a /lcp_son
           op to the parent url (localhost:8448)
        3. Compares if the SON LCP's data is what we expected.
        4. Assert that
        :return:
        """
        cfg = getLCPConfig()
        parent = {"url": "http://localhost:8448"}
        lcp_client = LCPClient()
        start_mock_http_server()

        try:
            message = LCPMessages(BetweenLCPMessages.PostLCPParent, parent)
            lcp_client.postLcpSon(message.data)
            try:
                d = TestHttpServer.q.get(timeout=10)
                # So, the LCP Son has called our mock server?
                assert d['id'] == cfg.lcp['id']
                assert d['url'] == cfg.lcp['url']
            except Empty:
                assert False
        finally:
            stop_mock_http_server()
            # from extra import end_client_threads
            # end_client_threads()
        assert True

    def test_post_parent_message_to_lcp(self):
        """
        This summulate that we are an LCP parent with our own http server on localhost:8448
        This simulates the complete loop parent -> son , son -> parent
        1. Simulate http POST to LCPSon as a parent to it
        2. Reads within 5 seconds if the LCPSon, after the POST method is triggered sends a /lcp_son
           op to the parent url (localhost:8448)
        3. Compares if the SON LCP's data is what we expected.
        4. Assert that
        :return:
        """
        cfg = getLCPConfig()
        parent = {"url": "http://localhost:8448"}
        lcp_client = LCPClient()
        start_mock_http_server()
        headers = getAuthorizationHeaders()
        from extra.clients_starter import startup_client_threads
        startup_client_threads()

        try:
            result = self.simulate_post("/lcp_parent", headers=headers,
                                        body=json.dumps(parent))
            try:
                d = TestHttpServer.q.get(timeout=10)
                # So, the LCP Son has called our mock server?
                assert d['id'] == cfg.lcp['id']
                assert d['url'] == cfg.lcp['url']
            except Empty:
                assert False
        finally:
            stop_mock_http_server()
            # from extra.clients_starter import end_client_threads
            # end_client_threads()
            info = self.simulate_get("/poll", headers=headers)
            print(json.dumps(info.json))
        assert True


    def test_http_server(self):
        headers = getAuthorizationHeaders()
        headers['content-type'] = "application/json"
        print(headers)
        start_mock_http_server()
        stop_mock_http_server()

        try:
            # Tests that the Http server is closed...
            requests.get("http://localhost:8448/")
            assert False
        except requests.exceptions.ConnectionError:
            assert True

    def test_delete_parent(self):
        headers = getAuthorizationHeaders()
        cfg = getLCPConfig()

        d={"params_csv": "i=sdfassss"}

        r = self.simulate_delete("/lcp_parent", headers=headers, **d)
        print(r)
