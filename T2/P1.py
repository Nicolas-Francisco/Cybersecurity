import socket
import gzip
import time
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

CONNECTION_ADDR = ('localhost', 5327)
# CONNECTION_ADDR = ("172.17.69.107", 5327)

formatMessage = "GET {} HTTP/1.1\nCookie: secret={}\nHost: cc5325.dcc\n\n"
SECRET = "H0LAaaa3ST03SUNS3CRE70MUYS3CR3T0"

if __name__ == "__main__":
    sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_output = sock_input.makefile(errors="ignore")

    sock_input.bind(CONNECTION_ADDR)
    sock_input.listen(5)

    while True:
        conn, addr = sock_input.accept()

        actual_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("Fecha del log: {}".format(actual_time))
       
        while True:
            try:
                data = conn.recv(16)

            except Exception as e:
                print(e)
                print("Closing...")
                input.close()
                break

            print("Texto en request recibida: {}".format(data.decode()))
            print("IP en request recibida: {}".format(addr[1]))
            conn.send("Mensaje recibido".encode())

            # Primer gezeo (gzip) el msj
            print("Largo de respuesta no comprimida: {}".format(len(data)))
            t=gzip.compress(data)
            print("Largo de respuesta comprimida con gzip: {}".format(len(t)))
 
            # Segundo aeseo (AES-CBC) 
            backend = default_backend()     # Configuración que la librería pide pero no usa por un problema de diseño
            key = os.urandom(16)            # Llave usada por el cifrador de bloque
            iv = os.urandom(16)             # Vector de inicialización usado por el modo

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            encryptor = cipher.encryptor() 
            ct = encryptor.update(t*16) # Entrega parte de lo encriptado
            ct += encryptor.finalize() # Devuelve todo lo encriptado, en caso de haber quedado datos sin devolver anteriormente
            
            

            #Por ultimo, hexagoneo (hexstring)
            msj = formatMessage.format(ct, SECRET)
            hex_msj = msj.encode('utf-8').hex()
            print("Largo de respuesta comprimida con gzip cifrada: {}".format(len(hex_msj)/2))
            
        

        conn.close()
        print('Desconecta3')