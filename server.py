#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    lista = ['INVITE', 'ACK', 'BYE']
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion \r\n")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print(line.decode('utf-8'))
            
            if line.decode('utf-8').split(' ')[0] == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n"+
                                 b"SIP/2.0 180 Ringing\r\n\r\n"+
                                 b"SIP/2.0 200 OK\r\n\r\n")
            
            elif line.decode('utf-8').split(' ')[0] == 'ACK':
                #ENVIA LA CANCION
                pass
            
            elif line.decode('utf-8').split(' ')[0] == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

            if line.decode('utf-8').split(' ')[0] not in lista:
            #REVISAR ESTO, NO LO HACE BIEN
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            
            else:
            #REVISAR ESTO, NO LO HACE BIEN. 
            #CUANDO NO SEA UN 405 Y ESTÉ MAL
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                   
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')
    #COMPROBAR SI EL AUDIO EXISTE CON OS.PATH
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', 6001), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
