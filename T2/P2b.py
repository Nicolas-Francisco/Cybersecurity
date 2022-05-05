# Implementación del ataque CRIME, la que ocurre al utilizar cifrado 
# y compresión al mismo tiempo y que permite exfiltrar información 
# sin conocer la llave de cifrado

import random
import gzip
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding 

W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
KNOWN = ''      # porción del texto adyascente al secreto
SECRET = ''     # secreto que queremos encontrar

X = ''                                  # bytearray o string
GZIP_X = gzip.compress(X.encode())      # gzip de X
UNKOWN_START = ''
UNKOWN_END = ''
key = os.urandom(16)  
iv = os.urandom(16)   

def encrypt_aes_cbc(msj):           
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor() 
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    t_padded = padder.update(msj) + padder.finalize()
    ENCRYPT_X = encryptor.update(t_padded) + encryptor.finalize()   
    return ENCRYPT_X


def COMPRESSION_ORACLE(DATA):
    X = UNKOWN_START + DATA + UNKOWN_END
    return len(encrypt_aes_cbc(gzip.compress(X.encode())))


def ALGORITHM(DATA):
    POSSIBLE = []   # arreglo vacío con todas las respuestas posibles
    y = '#$&!°'          # y es el conjunto de 5 a 10 carácteres fuera de w
    UNCOMPRESSED_LENGTH = COMPRESSION_ORACLE(KNOWN + y)
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

    KNOWN = BASURA + KNOWN
    return BASURA[:-1]


def CRIME_ATTACK():
    # computamos el padding
    PADDING = COMPUTE_PADDING(KNOWN)
    # computamos la respuesta
    RESPONSE = ALGORITHM(KNOWN + PADDING)
    # computamos el secreto
    SECRET = ''
    for r in RESPONSE:
        SECRET += r[-1]
    return SECRET