#!/usr/bin/env python3
# @Time    : 30/10/2024
# @Author  : DEADARMY
# Version: 2.0
# # geo locating ip address programe
# install requrments.txt {pip install -r requrments.txt}

import ipinfo
import sys

try:
    ip_address=sys.argv[1]
except IndexError:
    ip_address=None
access_token="fbfd711e68140f" # input your access token
handler=ipinfo.getHandler(access_token)
details=handler.getDetails(ip_address)
for key, value in details .all.items():
    print(f'{key}: {value}')


