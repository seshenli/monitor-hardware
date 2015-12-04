# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lihuiyw'

import commands
import socket

brand = commands.getoutput("dmidecode | grep Vendor|awk -F: '{p^Cnt $2}'")
BASE_SERVER_INFO = brand
_server_ip = socket.gethostbyname(socket.gethostname())


# {编号，从1顺序执行：[Connector Name]，[status],[Type],[size]}
# {1：{'DIMM_B1':ok,"size":'8G'}}
# {
#     "ip": {
#         "memory": [
#             {
#                 "location": 9,
#                 "type": "ddr3",
#                 "size": 4096,
#                 "pl": 1333
#             },
#             {
#                 "location": 9,
#                 "type": "ddr3",
#                 "size": 4096,
#                 "pl": 1333
#             }
#         ],
#        "disk":[]
#     }
# }
def get_memory():
    mem_details = []
    cmd = "omreport chassis memory"
    status, outputs = commands.getstatusoutput(cmd)
    info_list = outputs.splitlines()
    if status != 0:
        return "error" + outputs
    for line in info_list:
        result = {}
        if 'Index' in line and line.split(':')[1] != ' ':
            idx = info_list.index(line)
            result['location'] = line.split(':')[1].strip()
            result['Connector Name'] = info_list[idx + 2].split(':')[1].strip()
            result['type'] = info_list[idx + 3].split(':')[1].strip().split(' ')[0]
            result['size'] = info_list[idx + 4].split(':')[1].strip()
            mem_details.append(result)
    return mem_details


def dellget_disk():
    dell_diskret = {}
    disk_datils = []
    dellraid_cmd = commands.getoutput("omreport storage vdisk")
    dell_diskret['Layout'] = [raid_key.split(':')[1].strip() for raid_key in dellraid_cmd.splitlines() if 'Layout' in raid_key][0]
    disk_datils.append(''.join(dell_diskret))
    return disk_datils


def get_disk_details():
    disk_detail = []
    result = {}
    cmd = "omreport storage pdisk controller=0"
    status, disk_details = commands.getstatusoutput(cmd)
    detail_list = disk_details.splitlines()
    if status != 0:
        return "error"
    for line in detail_list:
        if 'State' in line:
            result['state'] = line.split(':')[1].strip()
        if 'Status' in line:
            result['status'] = line.split(':')[1].strip()
        if 'Capacity' in line:
            result['size'] = line.split(':')[1].strip().split(' ')[0]
            disk_detail.append(result)
            result = {}
    return disk_detail


def get_fans_status():
    result = {}
    fans_detail = []
    cmd = "omreport chassis fans"
    status, fans_details = commands.getstatusoutput(cmd)
    if status != 0:
        return "error"
    for line in fans_details.splitlines():
        if 'Index' in line:
            result['Index'] = line.split(':')[1].strip()
        if 'Status' in line:
            result['Status'] = line.split(':')[1].strip()
        if 'Reading' in line:
            result['Reading'] = line.split(':')[1].strip()
            fans_detail.append(result)
            result = {}
    return fans_detail

if __name__ == "__main__":
    ret = {_server_ip: {'memory': get_memory(),
                        'disk': dellget_disk(),
                        'disk_detail': get_disk_details(),
                        'fans_status': get_fans_status()}}
    print ret
