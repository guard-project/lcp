import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

import waitress  # noqa: E402
from rich import pretty, traceback  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402

from RestClients.LCPClient import *
import time
from lib.lcp_config import LCPConfig


pretty.install()
traceback.install(show_locals=False)

from about import project, title, version  # noqa: E402
from api import api  # noqa: E402
from reader.arg import Arg_Reader  # noqa: E402
from utils.log import Log  # noqa: E402


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

if db.version is not None:
    print(db.version)
else:
    ident = f'{project} - {title} v:{version}'
    console = Console()
    console.print(Panel.fit(ident))
    Log.init(config=db.log_config)
    api_instance = api(title=title, version=version)
    Log.get('api').success(f'Accept requests at {db.host}:{db.port}')

    Thread(target=threadOp).start()

    waitress.serve(api_instance, host=db.host, port=db.port, expose_tracebacks=False, ident=ident, _quiet=True)
