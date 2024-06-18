import socket
from time import sleep

class F4t:

    def __init__(self, ip='10.10.1.8', port=5025):
        try:
            self.chamberSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.chamberSocket.connect((ip, port))
            self.chamber = 1
        except:
            self.chamber = 0
            print('Failed to stablish connection to Thermal Chamber')

    def set_temperature(self, temp):
        comm = ':SOURCE:CLOOP1:SPOINT ' + str(temp)
        self.chamberSocket.sendall(bytes(comm, encoding='ascii'))
        self.chamberSocket.recv(1024)
        sleep(6)

    def get_temperature(self):
        comm = ':SOURCE:CLOOP1:PVALUE?'
        self.chamberSocket.sendall(bytes(comm, encoding='ascii'))
        temp = self.chamberSocket.recv(1024)
        return temp.decode('ascii')