import sys
import socket
import tqdm
import os
import ipaddress

SEPARATOR = " "



if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1:3]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
printf("connecting to...", host, " ", port)
client.connect_ex((host, int(port)))
printf("connected...")
client.sendall(b"download chat history")

recieve = client.recv(4096).decode('ascii')
filename, filesize = receive.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:

        bytes_read = client_socket.recv(4096)
        if not bytes_read:
            break
        f.write(bytes_read)

        progress.update(len(bytes_read))


client.close()
