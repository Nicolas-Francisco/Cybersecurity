import socket
import random
import gzip
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding 

CONNECTION_ADDR = ('localhost', 5327)

# # mensaje secreto
# SECRET = "H0LAaaa3ST03SUNS3CRE70MUYS3CR3T0"

def COMPRESSION_ORACLE(socket, MSJ):
    # enviamos el mensaje para su compresión
    socket.send(MSJ.encode())
    return socket.recv(4096).decode() 


def ALGORITHM(socket, KNOWN):
    POSSIBLE = []   # arreglo vacío con todas las respuestas posibles
    NO_W = '#$&!°'  # conjunto de caracteres que no están en w
    for c in W:     # recorremos todos los caracteres de w
        BASE_LENGTH = COMPRESSION_ORACLE(socket, KNOWN + NO_W + c)
        C_LENGTH = COMPRESSION_ORACLE(socket, KNOWN + c + NO_W)
        if C_LENGTH < BASE_LENGTH:
            POSSIBLE.append(c)

    # RESPONSES contendrá todas las posibles soluciones para SECRET,
    # justo después de KNOWN
    RESPONSES = []
    if POSSIBLE != []:
        for p in POSSIBLE:
            RESPONSES += ALGORITHM(socket, KNOWN + p)

    return RESPONSES


def COMPUTE_PADDING(socket, KNOWN):
    # computamos un padding para que el largo calce con el largo del bloque
    BASE_LENGTH = COMPRESSION_ORACLE(socket, KNOWN)
    NEW_LENGTH = BASE_LENGTH
    BASURA = ''
    while NEW_LENGTH == BASE_LENGTH:
        NEW_LENGTH = COMPRESSION_ORACLE(socket, BASURA + KNOWN)
        if NEW_LENGTH <= BASE_LENGTH:
            BASURA += random.choice(W)

    return BASURA[:-1]


def CRIME_ATTACK(socket, KNOWN):
    # computamos el padding
    PADDING = COMPUTE_PADDING(socket, KNOWN)
    print("[PADDING] \"{}\"".format(PADDING))

    KNOWN =  PADDING + KNOWN
    print("[KNOWN] \"{}\"".format(KNOWN))

    # computamos la respuesta
    RESPONSE = ALGORITHM(socket, KNOWN)
    SECRET = ''
    for r in RESPONSE:
        SECRET += r[-1]
        
    print("[CRIME RESPONSE] \"{}\"".format(SECRET))
    return SECRET


if __name__ == "__main__":
    W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = os.urandom(16)  
    iv = os.urandom(16)  
    IKNOW = 'Cookie: secret='
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    while True:
        try:
            print("-----------------------------------------------------")
            print("-------------------- CRIME ATTACK -------------------")

            CRIME_ATTACK(s, IKNOW)

            print("-----------------------------------------------------")
        except Exception as e:
            print(e)
            print("Closing Client...")
            input.close()
            s.close()
            break