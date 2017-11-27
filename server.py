#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import os
import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    lista = ['INVITE', 'ACK', 'BYE']

    def error(self, line):
        lista_errores = line.split(' ')
        fail = False
        try:
            if len(lista_errores) != 3:
                fail = True
            if lista_errores[1][0:4] != 'sip:':
                fail = True
            if '@' not in lista_errores[1]:
                fail = True
            if ':' not in lista_errores[1]:
                fail = True
            if 'SIP/2.0\r\n\r\n' not in lista_errores[2]:
                fail = True
        except IndexError:
            fail = True
        return fail

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion \r\n")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print(line.decode('utf-8'))
            if not line:
                break
            if self.error(line.decode('utf-8')):
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            elif line.decode('utf-8').split(' ')[0] == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n" +
                                 b"SIP/2.0 180 Ringing\r\n\r\n" +
                                 b"SIP/2.0 200 OK\r\n\r\n")

            elif line.decode('utf-8').split(' ')[0] == 'ACK':
                aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO_FILE
                print('Vamos a ejecutar', aEjecutar)
                os.system(aEjecutar)

            elif line.decode('utf-8').split(' ')[0] == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

            elif line.decode('utf-8').split(' ')[0] not in self.lista:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")


if __name__ == "__main__":
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    AUDIO_FILE = sys.argv[3]
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')
    if not os.path.exists(AUDIO_FILE):
        sys.exit("Audio_file doesn't exists")
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('servidor finalizado')
