import socket
import gzip
import time
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding 

CONNECTION_ADDR = ('localhost', 5327)
# CONNECTION_ADDR = ("172.17.69.107", 5327)

# header solicitado
formatMessage = "GET {} HTTP/1.1\nCookie: secret={}\nHost: cc5325.dcc\n\n"

# mensaje secreto
SECRET = "H0LAaaa3ST03SUNS3CRE70MUYS3CR3T0"

if __name__ == "__main__":
    sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_output = sock_input.makefile(errors="ignore")

    sock_input.bind(CONNECTION_ADDR)
    sock_input.listen(1)

    while True:
        conn, addr = sock_input.accept()
        actual_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
       
        while True:
            try:
                data = conn.recv(4096)

            except Exception as e:
                print(e)
                print("Closing...")
                break

            # log solicitado
            # print("-----------------------------------------------------")
            # print("Fecha del log: {}".format(actual_time))
            print("Texto en request recibida:\n{}".format(data.decode()))
            # print("IP en request recibida: {}".format(addr[1]))

            # se dan los datos recibidos por el servidor y el mensaje secreto
            # al header para proceder con el cifrado
            msj = formatMessage.format(data.decode(), SECRET)

            # print("Largo de respuesta no comprimida: {}".format(len(msj)))

            # se comprime el mensaje en bytes
            t = gzip.compress(msj.encode())
            # print("Largo de respuesta comprimida con gzip: {}".format(len(t)))

            backend = default_backend()     # Configuración que la librería pide pero no usa por un problema de diseño
            key = os.urandom(16)            # Llave usada por el cifrador de bloque
            iv = os.urandom(16)             # Vector de inicialización usado por el modo

            # Se crea el cifrador de bloque AES CBC
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            encryptor = cipher.encryptor() 

            # Se crea un padder para el mensaje, ya que se requiere que tenga multiplo de 16
            padder = padding.PKCS7(algorithms.AES.block_size).padder()

            # Se le aplica el padder al mensaje
            t_padded = padder.update(t)
            t_padded += padder.finalize()

            # print("Largo de respuesta comprimida con gzip padeado: {}".format(len(t_padded)))
            # Se cifra el mensaje con padding
            ct = encryptor.update(t_padded)     # Entrega parte de lo encriptado
            ct += encryptor.finalize()          # Devuelve todo lo encriptado
            
            # Se pasa el mensaje cifrado a hexadecimal
            hex_msj = ct.hex()
            # print("Largo de respuesta comprimida con gzip cifrada: {}".format(len(hex_msj)//2))

            # Se envia el mensaje cifrado. En este caso no es necesario
            conn.send(hex_msj.encode())

        conn.close()
        print('Closing Server...')