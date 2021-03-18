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
    time.sleep(3) # Let Falkon start first...
    lcp_client = LCPClient()
    config = LCPConfig
    for p in config.parents:
        msg = LCPMessages(BetweenLCPMessages.ConnectLCPParent, {"url": p})
        lcp_client.send(msg)

    lcp_client.__qread()


db = Arg_Reader.read()

ident = f'{project} - {title} v:{version}'
print(ident)

if db.version is not None:
    print(db.version)
else:
    print(db)

    Thread(target=threadOp).start()

    waitress.serve(api(title=title, version=version,
                        dev_username=db.dev_username, dev_password=db.dev_password),
                    host=db.host, port=db.port, expose_tracebacks=False, ident=ident)
