import multiprocessing
import platform
import psutil
import subprocess
import json
from pathlib import Path
from extra.hw_helpers.network_information import NetworkInterfacesInfo

import distro

MEMINFO = "/proc/meminfo"
bytes2Gb = 1024**3


VM_TYPES = ["qemu", "kvm", "zvm", "vmware", "microsoft", "oracle", "powervm", "xen", "bochs",
            "uml", "parallels", "bhyve", "qnx", "acrn"]
CONTAINER_TYPES = ["openvz", "lxc", "lxc-libvirt", "systemd-nspawn", "docker", "podman",
                   "rkt", "wsl", "proot", "pouch"]

class HostInformation:
    def __init__(self):
        self.is_container = False
        self.environment = self.get_execution_environment()
        self.cpus = self.cpu_count()
        self.ram = self.mem()
        self.distro = self._linux_distribution()
        self.operating_system = self.distro[0] + " " + self.distro[1]
        self.hostname = platform.node()
        self.disk_devices = []
        if not self.is_container:
            self.retrieve_disk_info()



    def cpu_count(self):
        self.cpus = multiprocessing.cpu_count()
        return self.cpus

    def mem(self):
        with open(MEMINFO) as mif:
            all_mem_data = mif.readlines()

        for line in all_mem_data:
            field, size_with_units = line.strip().split(':')
            field = field.strip()

            if field == "MemTotal":
                s_size, units = size_with_units.split()
                self.ram = int(s_size)
                break;

        return self.ram

    def _linux_distribution(self):
        self.distro = distro.linux_distribution()
        return self.distro

    def os_info(self):
        if Path("/etc/lsb-release").exists():
            file = "/etc/lsb-release"
        elif Path("/etc/os-release").exists():
            file = "/etc/os-release"

        with open(file) as f:
            lines = f.readlines()
        self._os_info_release(lines)


    def _os_info_release(self, lines):
        for ln in lines:
            var, info = ln.strip().split('=')
            if var == "DISTRIB_DESCRIPTION":
                self.distrib_description=info.replace('"', '', 2)
            elif var == "DISTRIB_CODENAME":
                self.code_name=info
            elif var == "DISTRIB_RELEASE":
                self.distrib_release=info
            elif var == "NAME":
                pass

        # print(os.name)
        # print(f"System: {platform.system()}")
        # print(f"Release: {platform.release()}")
        # print(f"Version: {platform.version()}")
        # print(f"uname: {platform.uname()}")
        # print(f"distro: {distro.linux_distribution()}")
        # print(f"processor: {platform.uname().processor}")
        # print(f"machine: {platform.uname().machine}")

    def partition_info(self):
        partitions = psutil.disk_partitions()
        disks = psutil.d

        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"    Mountpoint: {partition.mountpoint}")
            try:
                print(f"    Filesystem: {partition.filesystem}")
            except Exception:
                print(f"    Filesystem: unknown")
            try:
                print(f"   Usage: {psutil.disk_usage(partition.mountpoint).total}")
            except Exception:
                pass

    def retrieve_disk_info(self):
        command_str = ["lsblk","-Jb"]
        cmd_res = subprocess.run(command_str, capture_output=True)
        js_str_data = cmd_res.stdout.decode('utf-8')

        dict_partitions = json.loads(js_str_data)

        bd = dict_partitions['blockdevices']

        disk_devices = []
        for disk in bd:
            dev_name = disk['name']
            if dev_name.startswith('zram') or dev_name.startswith('loop'):
                continue
            dev_size = round(float(disk['size'])/bytes2Gb, 2)

            id = "urn:HardiskDevice:"+dev_name
            diskPartitions = []

            dd = {"name": dev_name, "size": dev_size, "id":id}
            dd['partitions'] = diskPartitions
            if 'children' in disk:
                for partition in disk['children']:
                    part_name = partition['name']
                    part_size = round(float(partition['size'])/bytes2Gb, 2)
                    diskPartitions.append({"name": part_name, "size": part_size})
            disk_devices.append(dd)

        self.disk_devices = disk_devices

    def get_execution_environment(self):
        if Path("/.dockerenv").exists():
            self.is_container = True
            return "docker-container"

        command_str = ["systemd-detect-virt"]
        cmd_res = subprocess.run(command_str, capture_output=True)
        js_str_data = cmd_res.stdout.decode('utf-8').strip()


        if js_str_data == "none":
            return "bare-metal"
        if js_str_data in CONTAINER_TYPES:
            self.is_container = True
            if js_str_data in ["lxc", "lxc-libvirt"]:
                return "lxc-container"
        if js_str_data in VM_TYPES:
            return "vm"

        return js_str_data


class HostInfoToLcpHelper:
    def __init__(self):
        self.host_info = HostInformation()
        self.hostname = self.host_info.hostname
        self.operating_system = self.host_info.operating_system
        self.cpus = self.host_info.cpus
        self.js_info = {}
        self.get_execution_environment()

    def dumps(self):
        return json.dumps(self.js_info)

    def get_execution_environment(self):
        self.js_info['type'] = self.host_info.environment
        self.deployment={ 'hostname': self.hostname,
                          'operatingSystem': self.host_info.operating_system,
                          'cpus': self.cpus,
                          'ram': self.host_info.ram,
                          'networkInterfaces': NetworkInterfacesInfo().net_info(),
                          }
        if len(self.host_info.disk_devices) > 0 and not self.host_info.is_container:
            self.deployment['diskDevices'] = self.host_info.disk_devices
        self.js_info['environment'] = self.deployment


if __name__ == "__main__":
     print(HostInfoToLcpHelper().dumps())
