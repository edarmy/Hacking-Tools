# DNS Enmaration tool using dnspython
#!/bin/python
# Author: DEADARMY
# Date: 30/10/2024
# Version: 2.0

import dns.resolver #resolve all record
import dns.reversename

target_domain="yalamanchili.in"
service = "ldap"
protocol = "tcp"

Arecord=[]

def get_srv_records(domain, service, protocol):
    query_name = f"_{service}._{protocol}.{domain}"
    try:
        answers = dns.resolver.resolve(query_name, 'SRV')
        for answer in answers:
            print(f'\n[++]DNS Record Found {domain}: SRV\n===========================================================')
            print(f"Priority: {answer.priority}, Weight: {answer.weight}, Port: {answer.port}, Target: {answer.target}")
    except dns.resolver.NoAnswer:
        print(f"No SRV record found for {query_name}")
    except Exception as e:
       print(f"An error occurred: {e}")

def get_ptr_from_ip(ip_address):
    try:
        rev_name = dns.reversename.from_address(ip_address)
        answers = dns.resolver.resolve(rev_name, 'PTR')
        ptr_records = [str(record) for record in answers]
        return ptr_records
    except:
       return None

        


# DNS record type
record_types = [ "A", "AAAA" , "CNAME" , "MX" , "NS" , "SOA" , "TXT", "PTR", "CAA","DNSKEY", "DS","NSEC", "NSEC3", "KX","KEY","NSEC3PARAM", "RRSIG","TLSA", "SPF", "LOC", "HINFO", "RP","APL","AFSDB", "DNAME", "NAPTR", "SSHFP", "URI", "DHCID", "DNSSEC" ]

# Create DNS resolver
resolver = dns.resolver.Resolver()
for record_type in record_types:
    try:
       answers = resolver.resolve(target_domain, record_type)
       
    except dns.resolver.NoAnswer:
        continue
    except Exception as e:
       continue
    print(f'\n[++]DNS Record Found {target_domain}: {record_type}\n===========================================================')
    for rdata in answers:
        print(f'{rdata}')
        # return only A record from dns
        if record_type == "A":
            Arecord.append(str(rdata))

get_srv_records(target_domain, service, protocol)

ptr_records = get_ptr_from_ip(Arecord[0])
for record in ptr_records:
    print(f'\n[++]DNS Record Found: {target_domain}:PTR\n===========================================================')
    print(record)

print(f"\n[--] NO More Records Found")


