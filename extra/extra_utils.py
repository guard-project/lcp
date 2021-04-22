from urllib.parse import urlparse

HTTP_SCHEME  = "http"
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


