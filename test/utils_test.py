from extra.extra_utils import UrlSchemaData

from test.testbase import LCPTestBase


class TestMyApp(LCPTestBase):
    def test_url_scheme(self):
        url = "http://www.example.com"
        data = UrlSchemaData(url)
        assert data.port == 80
        assert data.host == "www.example.com"

        url = "https://www.example.com"
        data = UrlSchemaData(url)
        assert data.port == 443
        assert data.host == "www.example.com"

        url = "https://www.example.com:5000"
        data = UrlSchemaData(url)
        print(data.port, type(data.port))
        assert data.host == "www.example.com"
        assert data.port == 5000


