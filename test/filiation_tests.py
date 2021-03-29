from falcon import testing, HTTP_ACCEPTED
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
from schema.filiation import LCPDescription
from marshmallow import ValidationError
from pprint import pprint
import json
from utils.sequence import is_list, wrap
from resource import SonLCPIdentification
from test_utils import *
from RestClients.LCPClient import LCPClient, LCPMessages, BetweenLCPMessages
from queue import Empty
import requests

class FiliationTesting(testing.TestCase):
    def setUp(self):
        super(FiliationTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                        dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(FiliationTesting):
    def _getAuthorizationHeaders(self):
        return {"Authorization": "Basic bGNwOmd1YXJk"}

    def _getFiliationData(self):
        uuid = "94216230-ae26-464c-9541-cc0ca62cd1ce"
        url = "https://example.url.com:4443"
        name = "lcp:example"
        body_dict = {"id": uuid, "url": url, "name": name}
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
            cfg.setSon({"id": uuids[i], "url": urls[i], "name": names[i]})

    def test_get_sons(self):
        headers = self._getAuthorizationHeaders()
        SonLCPIdentification.data = {}
        config = getLCPConfig()
        config.deleteAllSons()

        # No Authorization for request:
        result = self.simulate_get("/lcp_son")
        assert (result.status == "401 Unauthorized")

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
        headers = self._getAuthorizationHeaders()

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

        # Test Unauthorized. -- Expected 401 Unauthorized
        result = self.simulate_post("/lcp_son", body=json.dumps(body))
        # assert(result.status == "401 Unauthorized")

        # With Authorization header + OK data -- Expected: 201 Created
        headers = self._getAuthorizationHeaders()
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
        assert result.status == "201 Created"

        result = self.simulate_get("/lcp_son", headers=headers)
        print(result)

    def test_delete_message(self):
        uuid, url, body_dict = self._getFiliationData()
        headers = self._getAuthorizationHeaders()
        cfg = getLCPConfig()

        # Try delete without authorization:
        result = self.simulate_delete("/lcp_son/1324")
        assert(result.status == "401 Unauthorized")

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

        result = self.simulate_post("/lcp_parent", headers=headers, body=json.dumps(parent))
        assert result.status == "202 Accepted"
        try:
            message = lcp_client.q.get(timeout=3)
            assert message.message_type == BetweenLCPMessages.PostLCPSon
            assert message.data['url'] == parent['url']
            assert len(cfg.parents) == 1
            assert cfg.parents[0] == parent['url']
        except Empty:
            assert False

    def test_send_parent_message_to_lcp(self):
        """
        This summulate that we are an LCP parent with our own http server on localhost:4884
        1. Simulate sending a message to LCPSon as a parent to it
        2. Reads within 5 seconds if the LCPSon, after recieving the simulated messages sends a /lcp_son
           op to the parent url (localhost:4884)
        3. Compares if the SON LCP's data is what we expected.
        4. Assert that
        :return:
        """
        cfg = getLCPConfig()
        parent = "http://localhost:4884"
        lcp_client = LCPClient()
        start_http_server()
        try:
            message = LCPMessages(BetweenLCPMessages.PostLCPSon, parent)
            lcp_client.postLcpSon(message.data)
            try:
                d = TestHttpServer.q.get(timeout=6000)
                assert d['id'] == cfg.lcp['id']
                assert d['url'] == cfg.lcp['url']
                resp_message = lcp_client.q.get(timeout=3)
                assert resp_message.data['url'] == d['url']
                assert resp_message.data['id'] == d['id']
                assert resp_message.message_type == BetweenLCPMessages.PostLCPSon
            except Empty:
                assert False
        finally:
            requests.get("http://localhost:4884/terminate")
        assert True

    def test_http_server(self):
        headers = getAuthorizationHeaders()
        headers['content-type'] = "application/json"
        print(headers)
        start_http_server()
        requests.post("http://localhost:4884/terminate",json=json.dumps({"hola":"mundo"}),
                      headers=headers, )

        try:
            # Tests that the Http server is closed...
            requests.get("http://localhost:4884/")
            assert False
        except requests.exceptions.ConnectionError:
            assert True


    def test_other(self):
        body_fake = '{"whatever": "something wrong", "other_thing": "just_fail_this"}'
        try:
            lcp = LCPDescription().load(body_fake)
        except ValidationError as err:
            #  pprint(err.messages)
            pass

        body_fake = 'tara ri que te vi'
        try:
            lcp = LCPDescription(many=is_list(body_fake)).load(body_fake)
        except ValidationError as err:
            # pprint(err.messages)
            pass
