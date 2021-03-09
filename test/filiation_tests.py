from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
from schema.filiation import LCPSonDescription
from marshmallow import ValidationError
from pprint import pprint
import json
from utils.sequence import is_list, wrap
from resource import Filiation
from test_utils import *

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
        Filiation.data[uuid] = body_dict
        return uuid, url, body_dict

    def _setMultiFiliationData(self):
        uuids = ["49157b82-1962-4054-9862-989d61c4ff02", "04400853-c48d-47f7-9472-efdb8e877991", "066c121c-279d-4877-9e0b-ccd5f2a2d858"]
        urls = ["http://hst1.domain1.com", "http://hst2.domain2.com", "http://hst3.domain3.com"]
        names = ["lcp:host01", "lcp:host02", "lcp:host03"]
        for i in range(3):
            Filiation.data[uuids[i]] = {"id": uuids[i], "url": urls[i], "name": names[i]}

    def test_get_messages(self):
        headers = self._getAuthorizationHeaders()
        Filiation.data = {}

        # No Authorization for request:
        result = self.simulate_get("/filiation")
        # assert (result.status == "401 Unauthorized")

        # With Authorization header, get empy list:
        result = self.simulate_get("/filiation", headers=headers)
        assert (result.status == "200 OK")
        sons = result.json
        assert type(sons) is list
        assert len(sons) == 0

        uuid, url, body_dict = self._setFiliationData()
        result = self.simulate_get("/filiation", headers=headers)
        assert (result.status == "200 OK")
        sons = result.json
        assert len(sons) == 1
        assert sons[0]['id'] == uuid
        assert sons[0]['url'] == url

        self._setMultiFiliationData()
        result = self.simulate_get("/filiation", headers=headers)
        assert (result.status == "200 OK")
        sons = result.json
        assert len(sons) == 4


    def test_get_messages_by_id(self):
        headers = self._getAuthorizationHeaders()

        result = self.simulate_get("/filiation/134", headers=headers)
        assert (result.status == "404 Not Found")

        uuid, url, body_dict = self._setFiliationData()
        result = self.simulate_get(f"/filiation/{uuid}", headers=headers)
        assert (result.status == "200 OK")
        payload = result.json
        assert(payload['id'] == uuid)
        assert(payload['url'] == url)


    def test_post_message(self):
        # No Authorization for request:
        id, url, body_dict = self._getFiliationData()
        lcp_info = LCPSonDescription()
        body = lcp_info.dump(body_dict)

        # Test Unauthorized. -- Expected 401 Unauthorized
        result = self.simulate_post("/filiation", body=json.dumps(body))
        # assert(result.status == "401 Unauthorized")

        # With Authorization header + OK data -- Expected: 201 Created
        headers = self._getAuthorizationHeaders()
        print(body)
        result = self.simulate_post("/filiation", headers=headers, body=json.dumps(body))
        print(result.status)
        print(result.json)
        assert(result.status == "201 Created")

        # Fake thing. Not a correct data -- Expected: 406 Not Acceptable
        body_fake = '{"whatever": "something wrong", "other_thing": "just_fail_this"}'
        result = self.simulate_post("/filiation", headers=headers, body=body_fake)
        assert(result.status == "406 Not Acceptable")

        # Bad URL. Not correct URL.
        body_dict["url"] = "this is not an url"
        body = lcp_info.dump(body_dict)
        result = self.simulate_post("/filiation", headers=headers, body=json.dumps(body))
        assert(result.status == "406 Not Acceptable")

    def test_post_multi(self):
        body = loadExampleFile("FiliatedLCPs.json")
        headers = getAuthorizationHeaders()

        result = self.simulate_post("/filiation", headers=headers,
                                    body=json.dumps(body))
        assert result.status == "201 Created"

        result = self.simulate_get("/filiation", headers=headers)
        print(result)

    def test_delete_message(self):
        uuid, url, body_dict = self._getFiliationData()
        headers = self._getAuthorizationHeaders()

        # Try delete without authorization:
        result = self.simulate_delete("/filiation/1324")
        assert(result.status == "401 Unauthorized")

        # Try delete with authorization, but non existent
        result = self.simulate_delete(f"/filiation/{uuid}", headers=headers)
        assert (result.status == "404 Not Found")

        self._setMultiFiliationData()
        self._setFiliationData()
        assert (uuid in Filiation.data)
        result = self.simulate_delete(f"/filiation/{uuid}", headers=headers)
        assert (result.status == "200 OK")
        assert (uuid not in Filiation.data)


    def test_other(self):
        body_fake = '{"whatever": "something wrong", "other_thing": "just_fail_this"}'
        try:
            lcp = LCPSonDescription().load(body_fake)
        except ValidationError as err:
            #  pprint(err.messages)
            pass

        body_fake = 'tara ri que te vi'
        try:
            lcp = LCPSonDescription(many=is_list(body_fake)).load(body_fake)
        except ValidationError as err:
            # pprint(err.messages)
            pass

    def testFoo(self):
        uuid, url, body = self._getFiliationData()
        print(uuid)
        print(url)
        print(body)
