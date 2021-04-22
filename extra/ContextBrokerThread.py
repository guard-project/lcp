from extra.lcp_config import LCPConfig
import requests
from requests.exceptions import Timeout
import json

AUTH_HEADER = {"Authorization": "GUARD eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                ".eyJpYXQiOiIxNjE2NzgxMDU4IiwiZXhwIjoiMTY0ODMxNzA1OCIsIm5iZiI6MTYxNjc4MTA1OH0.4jC0t"
                                "-VJwKR4e--LT-QU36hATUUbf530UL-fHj_bssE",
               "content-type": "application/json"}
CB_URL ="http://localhost:5000"
# CB_URL = "http://testbed.guard-project.eu:5000"


class ContextBrokerThread(object):
    class __ContextBrokerThread:
        def __init__(self):
            self.cfg = LCPConfig()

        def is_lcp_registered(self):
            # query = CB_URL + "/exec-env/" + self.cfg.lcp['id']
            query = CB_URL + "/exec-env/frontend"
            try:
                resp = requests.get(query, headers=AUTH_HEADER)
            except (Timeout):
                pass

            if resp.status_code != 200:
                return True

            return False

        def lcp_post_register(self):
            if self.is_lcp_registered():
                return
            data = self.cfg.exec_env_register_data()
            query = CB_URL + "/exec-env/"
            try:
                resp = requests.post(query, data=json.dumps(data), headers=AUTH_HEADER)
            except (Timeout):
                pass
            print(json.dumps(data))
            print("Status! ", resp.status_code)

        def agents_register(self):
            print(self.cfg.agents)

    instance = None

    def __new__(cls, *args, **kwargs):
        if ContextBrokerThread.instance is None:
            ContextBrokerThread.instance = ContextBrokerThread.__ContextBrokerThread()
        return ContextBrokerThread.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


if __name__ =="__main__":
    cb = ContextBrokerThread()
    cb.agents_register()
