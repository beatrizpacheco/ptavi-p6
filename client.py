#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

if len(sys.argv) != 3:
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

METHOD = sys.argv[1]
MESSAGE = sys.argv[2]
IP = MESSAGE.split('@')[1].split(':')[0]
PORT = int(MESSAGE.split('@')[1].split(':')[1])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))

    if METHOD == 'INVITE':
        my_socket.send(bytes('INVITE sip:' + MESSAGE.split(':')[0] + 
                             ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    
    if METHOD == 'BYE':
        my_socket.send(bytes('BYE sip:' + MESSAGE.split(':')[0] + 
                             ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))
    message_receive = data.decode('utf-8').split(' ')
    for element in message_receive:
        if element == '200':
            my_socket.send(bytes('ACK sip:' + MESSAGE.split(':')[0] + 
                                 ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    print("Terminando socket...")

print("Fin.")
