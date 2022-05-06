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


#KNOWN = 'Cookie: secret='      # porción del texto adyascente al secreto
#SECRET = ''     # secreto que queremos encontrar
#X = ''                                  # bytearray o string
#GZIP_X = gzip.compress(X.encode())      # gzip de X
#key = os.urandom(16)  
#iv = os.urandom(16)   


def encrypt_aes_cbc(msj):           
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor() 
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    t_padded = padder.update(msj) + padder.finalize()
    ENCRYPT_X = encryptor.update(t_padded) + encryptor.finalize()   
    return ENCRYPT_X


def COMPRESSION_ORACLE(DATA):
    return len(encrypt_aes_cbc(gzip.compress(DATA.encode())))


def ALGORITHM(KNOWN):
    POSSIBLE = []   # arreglo vacío con todas las respuestas posibles
    # UNCOMPRESSED_LENGTH = COMPRESSION_ORACLE(KNOWN + y)
    NO_W = '#$&!°'       # conjunto de caracteres que no están en w
    for c in W:     # recorremos todos los caracteres de w
        BASE_LENGTH = COMPRESSION_ORACLE(KNOWN + NO_W + c)
        C_LENGTH = COMPRESSION_ORACLE(KNOWN + c + NO_W)
        if C_LENGTH < BASE_LENGTH:
            POSSIBLE.append(c)

    # RESPONSES contendrá todas las posibles soluciones para SECRET,
    # justo después de KNOWN
    RESPONSES = []
    if POSSIBLE != []:
        for p in POSSIBLE:
            RESPONSES += ALGORITHM(KNOWN + p)

    return RESPONSES


def COMPUTE_PADDING(KNOWN):
    # computamos un padding para que el largo calce con el largo del bloque
    BASE_LENGTH = COMPRESSION_ORACLE(KNOWN)
    NEW_LENGTH = BASE_LENGTH
    BASURA = ''
    while NEW_LENGTH == BASE_LENGTH:
        NEW_LENGTH = COMPRESSION_ORACLE(BASURA + KNOWN)
        if NEW_LENGTH <= BASE_LENGTH:
            BASURA += random.choice(W)

    #IKNOWN = BASURA + IKNOWN
    return BASURA[:-1]


def CRIME_ATTACK(MSJ):
    # computamos el padding
    PADDING = COMPUTE_PADDING(MSJ)
    print("[PADDING] \"{}\"".format(PADDING))

    MSJ =  PADDING + MSJ
    # computamos la respuesta
    RESPONSE = ALGORITHM(MSJ)
    print("[RESPONSES] \"{}\"".format(RESPONSE))
    
    SECRET = ''
    for r in RESPONSE:
        SECRET += r[-1]
        
    print("[CRIME RESPONSE] \"{}\"".format(SECRET))
    return SECRET


if __name__ == "__main__":
    W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = os.urandom(16)  
    iv = os.urandom(16)  
    IKNOW = 'Cookie: secret='      # porción del texto adyascente al secreto 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    while True:
        try:
            # Se lee un mensaje desde el sys
            response = input("send a message: ")

            # Se envia el mensaje en bytess
            s.send(response.encode())

            # Se recibe la respuesta y se imprime como mensaje del servidor
            print("[Client] \"{}\"".format(response))
            resp = s.recv(4096).decode()    
            print("[Server] \"{}\"".format(resp))

            print("-------------------- CRIME ATTACK -------------------")

            # ejecutamos el ataque CRIME definido en la clase P2b
            CRIME_ATTACK(resp+IKNOW)

            
            print("-----------------------------------------------------")
        except Exception as e:
            print(e)
            print("Closing Client...")
            input.close()
            s.close()
            break