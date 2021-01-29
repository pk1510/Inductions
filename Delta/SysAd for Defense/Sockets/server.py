#!/usr/bin/env python3
import threading
import sys
import socket
import selectors
import types
import tqdm
import os
from datetime import date
from datetime import timedelta
import ipaddress

SEPARATOR = " "
header_size = 2
online = {}


groups = {'soldierArmy': ["ArmyGeneral", "ChiefCommander"], 'soldierNavy': ["NavyMarshal", "ChiefCommander"], 'soldierAirForce': ["AirForceChief", "ChiefCommander"], 'heads': ["ArmyGeneral", "NavyMarshal", "AirForceChief", "ChiefCommander"]}
offline_buffer = {'ArmyGeneral': b"", 'NavyMarshal': b"", 'AirForceChief': b"", 'ChiefCommander': b""}
chatHistory = {'ArmyGeneral': {}, 'NavyMarshal': {}, 'AirForceChief': {}, 'ChiefCommander': {}}

for i in range(1, 50):
    groups['soldierArmy'].append(f'Army{i}')
    offline_buffer.update({f"Army{i}": b""})
    chatHistory[f'Army{i}'] = {}

    groups['soldierNavy'].append(f'Navy{i}')
    offline_buffer.update({f"Navy{i}": b""})
    chatHistory[f"Navy{i}"] = {}

    groups['soldierAirForce'].append(f'AirForce{i}')
    offline_buffer.update({f"AirForce{i}": b""})
    chatHistory[f'AirForce{i}'] = {}

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    online[sock] = socket.gethostbyaddr(addr[0])
    print("accepted connection from ", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", user_name='', recv_len = 0)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def groupProtocol(sock, data, user_name):
    for group in groups.values():
        if data.user_name in group and data.user_name != "ChiefCommander" and user_name in group:
            print("echoing to corresponding people")
            for members in group:
                if members == user_name and members in online.values():
                    sent = sock.send(f'{datetime.now()} {user_name} (me) : ' + data.outb[:data.recv_len])

                elif members == user_name and not members in online.values():          # Should be ready to write
                    print("buffering message to ", members)
                    offline_buffer[members] += f'{datetime.now()} {user_name} (me) : ' + data.outb[:data.recv_len]

                elif members != user_name:
                    offline_buffer[members] += f'{datetime.now()} {data.user_name}  : ' + data.outb[:data.recv_len]

                chatHistory.get(members)[datetime.now()] = f'{datetime.now()} {data.user_name}  : ' + data.outb[:data.recv_len]

            data.outb = data.outb[sent:]

    if data.user_name == "ChiefCommander" and user_name in groups.get('heads'):
        print("echoing to corresponding people")
        for members in groups.get('heads'):
            if members == user_name and members in online.values():
                sent = sock.send(f'{datetime.now()} {user_name} (me) : ' + data.outb[:data.recv_len])
            elif members == user_name and not members in online.values():          # Should be ready to write
                print("buffering message to ", members)
                offline_buffer[members] += f'{datetime.now()} {user_name} (me) : ' + data.outb[:data.recv_len]

            elif members != user_name:
                offline_buffer[members] += f'{datetime.now()} {data.user_name}  : ' + data.outb[:data.recv_len]

            chatHistory.get(members)[datetime.now()] = f'{datetime.now()} {data.user_name}  : ' + data.outb[:data.recv_len]

        data.outb = data.outb[sent:]

def send_file(recv_data, data, sock):
    f = open("sendHistory.txt", "wb")
    for chats in chatHistory.get(data.user_name):
        for msgs in chats.values():
            f.write(msgs)
    filename = "sendHistory.txt"
    filesize = os.path.getsize(filename)
    sock.send(f"{filename}{SEPARATOR}{filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            s.sendall(bytes_read)

            progress.update(len(bytes_read))

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    user_name = socket.gethostbyaddr(data.addr[0])
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)  # Should be ready to read

            if recv_data and recv_data[header_size:] == "Chat History".encode():
                send_file(recv_data, data, sock)
                sock.close()
            elif recv_data:
                data.recv_len = int(recv_data[:header_size])
                recv_data = recv_data[header_size:]
                data.user_name = user_name
                data.outb += recv_data[:data.recv_len]
        except:
            print("closing connection to ", data.addr)
            del online[sock]
            sock.close()
    if mask & selectors.EVENT_WRITE:
        try:
            if offline_buffer.get(user_name):
                sent = sock.sendall(offline_buffer.get(user_name))
                offline_buffer[user_name] = b""
            if data.outb:
                groupProtocol(sock, data, user_name)
        except:
            print("closing connection to ", data.addr)
            del online[sock]
            sock.close()

def modify():
    while True:
        for chats in chatHistory.values():
            for time in chats.keys():
                for  i in range(0,7):
                    list_days = list(today - timedelta(days=i))
                if time.strftime("%d %m %y") not in list_days:
                    del chats[time]




if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)
host, port = sys.argv[1], int(sys.argv[2])    
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
modify = threading.Thread(modify)
modify.start()
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
