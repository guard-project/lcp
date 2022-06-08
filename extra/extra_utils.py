from urllib.parse import urlparse

HTTP_SCHEME = "http"
HTTPS_SCHEME = "https"


class UrlSchemaData:
    def __init__(self, url):
        r = urlparse(url)
        self.scheme = r.scheme
        self.netloc = r.netloc
        self.port = 0
        self.host = ""
        self.https = False
        self.get_port()
        self.path = r.path

    def get_port(self):
        try:
            self.host, port = self.netloc.split(":", 1)
            self.port = int(port)
        except ValueError:
            self.host = self.netloc
            if self.scheme == HTTPS_SCHEME:
                self.port = 443
            else:
                self.port = 80
            if self.scheme == HTTPS_SCHEME:
                self.https = True


if __name__ == "__main__":
    schema = UrlSchemaData("http://localhost:4000/lcp_endpoint")
    schema = UrlSchemaData("http://localhost:4000")
    print(schema)
