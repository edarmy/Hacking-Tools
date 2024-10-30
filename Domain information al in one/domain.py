#!/bin/python
# @Time    : 30/10/2024
# @Author  : DEADARMY
# Version: 2.0
#Domain information finder


import requests 
import dns.resolver
import argparse 
import whois 

def is_registered(domain_name):
    try:
        whois_info= whois.whois ( domain_name )
    except Exception:
        return False
    else:
        return bool(whois_info.domain_name)


def get_discovered_subdomains ( domain , subdomain_list , timeout = 2 ):    
    discover_subdomains=[]
    for sub in subdomain_list:
        url=f"http://{sub}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[++] Discover subdomain: ",url)
            discover_subdomains.append(url) 
        return discover_subdomains
def resolve_dns_records ( target_domain ):
    record_types=["A", "AAAA" , "CNAME" , "MX" , "NS" , "SOA" , "TXT", "PTR", "CAA","DNSKEY", "DS","NSEC", "NSEC3", "KX","KEY","NSEC3PARAM", "RRSIG","TLSA", "SPF", "LOC", "HINFO", "RP","APL","AFSDB", "DNAME", "NAPTR", "SSHFP", "URI", "DHCID", "DNSSEC"]
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

if __name__ == "__main__":
    parser = argparse . ArgumentParser ( description = "Domainame information extractor, uses WHOIS db and scans for subdomains" )
    parser . add_argument ( "domain" , help = "The domain name without http(s)" )
    parser . add_argument ( "-t" , "--timeout" , type = int , default = 2 ,  help = "The timeout in seconds for prompting the connection, default is 2" )
    parser . add_argument ( "-s" , "--subdomains" , default = "../../../wordlist/10000sud.txt",  help = "The file path that contains the list of subdomains to scan, default is subdomains.txt" ) 
    parser . add_argument ( "-o" , "--output" , help = "The output file path resulting the discovered subdomains, default is {domain} -subdomains.txt" )
    args = parser . parse_args ()
    if is_registered ( args.domain):
         whois_info = whois . whois ( args .domain)
         print ( "Domain registrar:" , whois_info .registrar)
         print ( "WHOIS server:" , whois_info .whois_server)
         print ( "Domain creation date:" , whois_info.creation_date)
         print ( whois_info )
         print ( "=" * 50 , "DNS records" , "=" * 50 ) 
         resolve_dns_records ( args .domain)
         print ( "=" * 50 , "Scanning subdomains" , "=" * 50 )
         with open ( args.subdomains) as file :
             content = file . read ()
             subdomains = content . splitlines () 
             discovered_subdomains = get_discovered_subdomains ( args .domain, subdomains )
             discovered_subdomains_file = f" { args .domain } - subdomains.txt"
         with open ( discovered_subdomains_file , "w" ) as f :
            for subdomain in discovered_subdomains :
                print ( subdomain , file = f )

