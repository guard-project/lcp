#!/usr/bin/env python

import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

from about import project, title, version
from api import api
from reader.arg import Arg_Reader
import waitress
from threading import Thread
from RestClients.LCPClient import *
import time
from lib.lcp_config import LCPConfig


def threadOp():
    time.sleep(3)  # Let Falkon start first...
    lcp_client = LCPClient()
    config = LCPConfig()
    for children_requested in config.children_requested:
        if children_requested not in config.parents:
            msg = LCPMessages(BetweenLCPMessages.PostLCPParent, children_requested)
            lcp_client.send(msg)

    for parent in config.parents:
        msg = LCPMessages(BetweenLCPMessages.PostLCPSon, {"url": parent})
        lcp_client.send(msg)

    lcp_client.qread()


db = Arg_Reader.read()

ident = f'{project} - {title} v:{version}'

if db.version is not None:
    print(db.version)
else:
    Thread(target=threadOp).start()

    waitress.serve(api(title=title, version=version,
                        dev_username=db.dev_username, dev_password=db.dev_password),
                   host=db.host, port=db.port, expose_tracebacks=False, ident=ident)

    # ssl_keyfile = "/home/jicg/GUARD/Development/Integration/certs/https_cert/httpscert.key"
    # ssl_certfile = "/home/jicg/GUARD/Development/Integration/certs/https_cert/httpscert.pem"
    # ssl_ca = "/home/jicg/GUARD/Development/Integration/certs/rootcertificate/jicg.root.crt"

    # ssl_cert_reqs = 1

    #
    #uvicorn.run(api(title=title, version=version,
    #               dev_username=db.dev_username, dev_password=db.dev_password),
    #           host=db.host, port=db.port,
    #           ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile, ssl_ca_certs=ssl_ca,
    #           ssl_cert_reqs=ssl.CERT_OPTIONAL, # worker_class="CustomWorker",
    #           interface="wsgi")
