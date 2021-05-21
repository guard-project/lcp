from test.testbase import LCPTestBase
from test_utils import *


class TestMyApp(LCPTestBase):
    def test_start_stop_mock_server(self):
        start_mock_http_server()
        # request.post("http://localhost:4884/exec-env/12345")
        # request.post("http://localhost:4884/exec-env")
        stop_mock_http_server()

    def test_post_agent_type(self):
        headers = getAuthorizationHeaders()
        body = loadExampleFile("agent-type-example.json")

        cb_info = {"url": 'http://localhost:4884',
                   "auth_header": "Basic Z3VhcmQ6cGFzc3dvcmQK"
                   }

        cfg = LCPConfig()
        cfg.setContextBroker(cb_info)

        # Start a mock https server -- Need a post there
        start_mock_http_server()
        from extra.clients_starter import startup_client_threads
        startup_client_threads()
        time.sleep(3)

        try:
            result = self.simulate_post("/agent/type", headers=headers,
                               body=json.dumps(body))
            assert result.status_code == 201

            agent_info = TestHttpServer.q.get(timeout=3000)
            print(agent_info)

        except Exception as e:
            assert False
        finally:
            stop_mock_http_server()
            # from extra.clients_starter import end_client_threads
            # end_client_threads()



