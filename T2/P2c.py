from re import I
import socket
import random
import gzip
import os
from urllib import response
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding 

CONNECTION_ADDR = ('localhost', 5327)

# # mensaje secreto
# SECRET = "H0LAaaa3ST03SUNS3CRE70MUYS3CR3T0"

def COMPRESSION_ORACLE(MSJ):
    #print("COMPRESION_ORACLE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    data=""
    # enviamos el mensaje para su compresión
    s.sendall(MSJ.encode())
    data_total = ""
    data_total = s.recv(4096)
    #while True:
     #   try:
      #      data = s.recv(16)
       #     data_total += data.decode()
#
 #           if len(data)<16:
  #              print("no more")
   #             break

    #    except Exception as e:
     #       print(e)
            #print("Closing...")
      #      break
    s.close()
    return len(data_total)


def ALGORITHM(KNOWN):
    #print("ALGORITHM")
    PADDING = COMPUTE_PADDING(KNOWN + NO_W)
    POSSIBLE = []       # arreglo vacío con todas las respuestas posibles
    for c in W:         # recorremos todos los caracteres de w
        #print("Primero mayor que segundo gano {}".format(c))
        BASE_LENGTH = COMPRESSION_ORACLE(PADDING + KNOWN + NO_W + c)
        #print(BASE_LENGTH)
        C_LENGTH = COMPRESSION_ORACLE(PADDING + KNOWN + c + NO_W)
        #print(C_LENGTH)
        if C_LENGTH < BASE_LENGTH:
            POSSIBLE.append(c)

    print("[POSSIBLE] \"{}\"".format(POSSIBLE))
    # RESPONSES contendrá todas las posibles soluciones para SECRET,
    # justo después de KNOWN
    #print(POSSIBLE)
    #RESPONSES = []
    #if POSSIBLE!= []:
    #    for p in POSSIBLE:
    #        RESPONSES +=ALGORITHM(KNOWN+p)

    
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
    #KNOWN = BASURA + KNOWN
    return BASURA[:-1]


def CRIME_ATTACK(IKNOW):
    #SECRET = ''
    #while len(SECRET) < 32:
        #PADDING = COMPUTE_PADDING(IKNOW + SECRET)
       # print("[PADDING] \"{}\"".format(PADDING))

        #KNOWN =  PADDING + IKNOW + SECRET

        # computamos la respuesta
    RESPONSE = ALGORITHM(IKNOW)
    print("[RESPONSES] \"{}\"".format(RESPONSE))

    left=32
    
    while left >0:
        POSSIBLES=[]
        for p in RESPONSE:
            POSSIBLE = ALGORITHM(IKNOW + p)
            for j in  POSSIBLE:
                POSSIBLES.append(p+j)
        RESPONSE=  POSSIBLES
        left-=1
        print("RESPONSE {}".format(RESPONSE))
        
    #print("[SECRET] \"{}\"".format(SECRET))
    return RESPONSE


if __name__ == "__main__":
    W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    NO_W = '#$&![]/'    # conjunto de caracteres que no están en w
    key = os.urandom(16)  
    iv = os.urandom(16)  
    IKNOW = 'Cookie: secret='
    
    # while True:

    print("-----------------------------------------------------")
    print("-------------------- CRIME ATTACK -------------------")

    CRIME_ATTACK(IKNOW)

    print("-----------------------------------------------------")
