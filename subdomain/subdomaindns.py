#!/bin/python
# @Time    : 30/10/2024
# @Author  : DEADARMY
# Version: 1.0
# Subdomain scanner 

import requests

domain="google.com"

with open("../../../wordlist/10000sud.txt") as file: # input your wordlist
    line=file.read()
    subdomain=line.splitlines()
    print(subdomain)

discover_subdomains=[]
for sub in subdomain:
    url=f"http://{sub}.{domain}"
    try:
        requests.get(url)
    except requests.ConnectionError:
        pass
    else:
        print("[++] Discover subdomain: ",url)
        discover_subdomains.append(url)    
# save discover subdomain as a new file
with open("discover_subdomain.txt", "w") as f:
    for subdomain in discover_subdomains:
        print(subdomain,file=f)