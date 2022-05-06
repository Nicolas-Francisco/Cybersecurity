from re import I
import socket
import random
import time
import os


CONNECTION_ADDR = ('localhost', 5327)

def COMPRESSION_ORACLE(MSJ):
    #print("COMPRESION_ORACLE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    # enviamos el mensaje para su compresión
    s.sendall(MSJ.encode())
    # recibimos lo entregado por el servidor
    data = s.recv(4096)
    s.close()
    return len(data)


def ALGORITHM(KNOWN):
    PADDING = COMPUTE_PADDING(KNOWN + NO_W)
    POSSIBLE = []       # arreglo vacío con todas las respuestas posibles
    
    for c in W:         # recorremos todos los caracteres de w
        BASE_MSJ = PADDING + KNOWN + NO_W + c
        BASE_LENGTH = COMPRESSION_ORACLE(BASE_MSJ)
        print("Texto BASE en request enviada = {}".format(BASE_MSJ))
        print("Largo de texto BASE en request = {}".format(BASE_LENGTH))
        
        C_MSJ = PADDING + KNOWN + c + NO_W
        C_LENGTH = COMPRESSION_ORACLE(C_MSJ)
        print("Texto C en request enviada = {}".format(C_MSJ))
        print("Largo de texto C en request = {}".format(C_LENGTH))

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
    RESPONSE = ALGORITHM(IKNOW)

    left=32
    
    while left >0:
        POSSIBLES=[]
        for p in RESPONSE:
            POSSIBLE = ALGORITHM(IKNOW + p)
            for j in  POSSIBLE:
                POSSIBLES.append(p+j)
        RESPONSE=  POSSIBLES
        print("[lista de posibles valores de secret] = {}".format(RESPONSE))
        left-=1
    print("SU SECRETO BIEN SECRETO ES {}".format("".join(RESPONSE)))
    return RESPONSE


if __name__ == "__main__":
    W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    NO_W = '#$&![]/'    # conjunto de caracteres que no están en w
    key = os.urandom(16)  
    iv = os.urandom(16)  
    IKNOW = 'Cookie: secret='
    actual_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("Fecha del log: {}".format(actual_time))


    print("-----------------------------------------------------")
    print("-------------------- CRIME ATTACK -------------------")

    CRIME_ATTACK(IKNOW)

    print("-----------------------------------------------------")
