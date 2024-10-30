#!/usr/bin/env python3
# @Time    : 30/10/2024
# @Author  : DEADARMY
# Version: 2.0
# Favicon icon hashes Generator
# install requrments.txt {pip install -r requrments.txt}

import mmh3
import sys
import codecs
import requests

try:
    response = requests.get(sys.argv[1])
    favicon = codecs.encode(response.content, 'base64')
    hash = mmh3.hash(favicon)
    print(f"Favicon Hash: {hash}")
except Exception as e:
    print(f"Error occured as: {e}", file=sys.stderr)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [Favicon URL]")
    sys.exit(0)

    