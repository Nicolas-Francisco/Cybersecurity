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
    hex_msj = ''

    while True:
        conn, addr = sock_input.accept()

        actual_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("Fecha del log: {}".format(actual_time))
       
        while True:
            try:
                data = conn.recv(1024)

            except Exception as e:
                print(e)
                print("Closing...")
                input.close()
                break

            print("Texto en request recibida: {}".format(data.decode()))
            print("IP en request recibida: {}".format(addr[1]))
            conn.send("Mensaje recibido".encode())
            
            msj = formatMessage.format(data.decode(), SECRET)

            backend = default_backend()     # Configuración que la librería pide pero no usa por un problema de diseño
            key = os.urandom(32)            # Llave usada por el cifrador de bloque
            iv = os.urandom(16)             # Vector de inicialización usado por el modo
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            encryptor = cipher.encryptor() 
            ct = encryptor.update(msj.encode('utf-8')) + encryptor.finalize()

            print("Largo de respuesta no comprimida: {}".format(len(ct)))
            
            hex_msj = ct.hex()
            print("Mensaje en hexadecimal: {}".format(hex_msj))
            with gzip.open('ciphered.txt.gz', 'wb') as f:
                f.write(ct.hex())

            print("Largo de respuesta comprimida con gzip cifrada: {}".format())

        conn.close()
        print('Desconecta3')