import multiprocessing
import platform
import psutil
import subprocess
from subprocess import PIPE
import json
from pathlib import Path
from extra.hw_helpers.network_information import NetworkInterfacesInfo
from schema.hardware_definitions import *
import distro
from uuid import uuid4
from extra.hw_helpers.host_info import *

if __name__ == "__main__":
    h = HostInfoToLcpHelper().js_info
    # print(json.dumps(h['environment']['diskDevices']))
    ExecutionEnvironment(many=False).load(h)
