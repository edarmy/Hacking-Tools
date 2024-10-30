#!/bin/python
# @Time    : 30/10/2024
# @Author  : DEADARMY
# Version: 0.1
# Banner Grabbing
import optparse
import socket
from socket import *

# Function to scan a single port
def connScan(tgtHost, tgtPort):
    try:
        # Create a socket object and connect to the target host and port
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.settimeout(1)  # Set a timeout for the connection
        connSkt.connect((tgtHost, int(tgtPort)))  # Ensure tgtPort is cast to an integer
        connSkt.send(b'Violent Python \r\n')  # Send banner grabbing request as bytes
        results = connSkt.recv(100)  # Receive response (banner)
        
        print(f'[+] {tgtPort}/tcp open')  # Indicate the port is open
        print(f'[+] Banner: {results.decode("utf-8").strip()}')  # Display the banner
        connSkt.close()
    except Exception as e:
        print(f'[-] {tgtPort}/tcp closed or no response')  # Handle closed ports
        print(f'[!] Error: {str(e)}')  # Display error message (for debugging)

# Function to scan multiple ports
def portScan(tgtHost, tgtPorts):
    try:
        tgtIp = gethostbyname(tgtHost)  # Get the IP address of the target host
    except:
        print(f'[-] Cannot resolve "{tgtHost}": Unknown host')  # Handle unknown hosts
        return
    
    try:
        tgtName = gethostbyaddr(tgtIp)  # Attempt to get the hostname from the IP
        print(f'\n[+] Scan Results for: {tgtName[0]}')
    except:
        print(f'\n[+] Scan Results for: {tgtIp}')  # Fallback to IP if hostname isn't found

    setdefaulttimeout(1)  # Set a timeout for socket connections
    for tgtPort in tgtPorts:
        connScan(tgtHost, tgtPort)  # Scan each port

# Main function to parse arguments and start the scan
def main():
    parser = optparse.OptionParser('usage: %prog -H <target host> -p <target port[s]>')
    
    # Define command-line options
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by commas')
    
    (options, args) = parser.parse_args()  # Parse command-line arguments
    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort.split(',') if options.tgtPort else []  # Split ports by comma
    
    # Ensure host and ports are provided
    if not tgtHost or not tgtPorts:
        print('[-] You must specify a target host and port[s].')
        exit(0)
    
    portScan(tgtHost, tgtPorts)  # Start the port scan

# Entry point
if __name__ == '__main__':
    main()
