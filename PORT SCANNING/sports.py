import socket 
from colorama import init, Fore

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

def is_port_open (host, port):
    s=socket.socket()
    try:
        s.connect((host,port))
        s.timeout(0.2)
    except :
        return False
    else:
        return True
host=input("Enter The host: ")
for port in range (1, 1025):

    if is_port_open(host,port):
        print(f"{GREEN}[+] {host}: {port} is open{RESET}")
    else:
        print(f"{GRAY}[!] {host}: {port} is closed{RESET}", end="\r")