import os
from socket import *
host = 'localhost' # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
def data_to_send(string):
    data = string.encode()
    UDPSock.sendto(data, addr)
