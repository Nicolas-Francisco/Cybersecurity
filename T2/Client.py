import socket
import random
import time
import os
import sys

if len(sys.argv) != 2:
    print('Use valid IPv4_ADDRESS')
    sys.exit(1)

CONNECTION_ADDR = (sys.argv[1], 5327)
f = open('Cliente_Logs', 'w')

def COMPRESSION_ORACLE(MSJ):
    # nos conectamos con el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    
    # enviamos el mensaje para su compresión
    s.sendall(MSJ.encode())
    # recibimos lo entregado por el servidor
    data = s.recv(4096)
    s.close()
    return len(data)


def ALGORITHM(KNOWN):
    # computamos el padding para el mensaje con el NO_W
    PADDING = COMPUTE_PADDING(KNOWN + NO_W)
    POSSIBLE = []       # arreglo vacío con todas las respuestas posibles
    
    for c in W:         # recorremos todos los caracteres de w
        print("-----------------------------------------------------")
        f.write("-----------------------------------------------------")
        BASE_MSJ = PADDING + KNOWN + NO_W + c
        BASE_LENGTH = COMPRESSION_ORACLE(BASE_MSJ)
        print("Texto BASE en request enviada = {}".format(BASE_MSJ))
        f.write("Texto BASE en request enviada = {}".format(BASE_MSJ))
        print("Largo de texto BASE en request = {}".format(BASE_LENGTH))
        f.write("Largo de texto BASE en request = {}".format(BASE_LENGTH))
        
        C_MSJ = PADDING + KNOWN + c + NO_W
        C_LENGTH = COMPRESSION_ORACLE(C_MSJ)
        print("Texto C en request enviada = {}".format(C_MSJ))
        f.write("Texto C en request enviada = {}".format(C_MSJ))
        print("Largo de texto C en request = {}".format(C_LENGTH))
        f.write("Largo de texto C en request = {}".format(C_LENGTH))
        print("-----------------------------------------------------")
        f.write("-----------------------------------------------------")

        if C_LENGTH < BASE_LENGTH:
            POSSIBLE.append(c)
    return POSSIBLE


def COMPUTE_PADDING(KNOWN):
    # computamos un padding para que el largo calce con el largo del bloque
    BASE_LENGTH = COMPRESSION_ORACLE(KNOWN)
    NEW_LENGTH = BASE_LENGTH
    BASURA = ''
    while NEW_LENGTH == BASE_LENGTH:
        NEW_LENGTH = COMPRESSION_ORACLE(BASURA + KNOWN)
        if NEW_LENGTH <= BASE_LENGTH:
            BASURA += random.choice(W)
    return BASURA[:-1]


def CRIME_ATTACK(IKNOW):
    # computamos la respuesta por primera vez con lo que sabemos
    RESPONSE = ALGORITHM(IKNOW)

    left = 32
    while left > 0:
        POSSIBLES = []
        for p in RESPONSE:
            POSSIBLE = ALGORITHM(IKNOW + p)
            for j in POSSIBLE:
                POSSIBLES.append(p+j)
        RESPONSE = POSSIBLES
        left -= 1
    return "".join(RESPONSE)


if __name__ == "__main__":
    W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    NO_W = '#$&![]/'    # conjunto de caracteres que no están en w
    key = os.urandom(16)  
    iv = os.urandom(16)  
    IKNOW = 'Cookie: secret='
    actual_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    

    print("Fecha del log: {}".format(actual_time))
    f.write("Fecha del log: {}".format(actual_time))

    print("-----------------------------------------------------")
    f.write("-----------------------------------------------------")
    print("-------------------- CRIME ATTACK -------------------")
    f.write("-------------------- CRIME ATTACK -------------------")

    secret = CRIME_ATTACK(IKNOW)

    print("-----------------------------------------------------")
    f.write("-----------------------------------------------------")
    print("[FINAL SECRET] \"{}\"".format(secret))
    f.write("[FINAL SECRET] \"{}\"".format(secret))
    print("-----------------------------------------------------")
    f.write("-----------------------------------------------------")

    # nos conectamos con el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    
    # enviamos el mensaje para su compresión
    s.sendall("$quit".encode())
    s.close()