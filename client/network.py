import socket
import json
import struct


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(2048))
        except Exception as e:
            self.disconnect(e)

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            
            raw_len_msg = self.recv_all(self.client, 4)
            len_msg = struct.unpack('>I', raw_len_msg)[0]
          
            d = self.recv_all(self.client, len_msg)

            keys = [key for key in data.keys()]
            return json.loads(d.decode())[str(keys[0])]
        except socket.error as e:
            self.disconnect(e)

    def recv_all(self, client, n):
        data = bytearray()
        while len(data) < n:
            packet = client.recv(n - len(data))
            if not packet:
                break
            data.extend(packet)
        return data


    def disconnect(self, msg):
        print("[EXCEPTION] Disconnected from server:", msg)
        self.client.close()