# P2d - Cree una función que permita descifrar el último carácter del texto cifrado.

from re import I
import socket
from traceback import print_tb
from unittest import TestCase
import utils
import P2c
import sys
SIZE_BLOCK = 16 # bytes

SERVER_A= ("172.17.69.107", 5312)
SERVER_B = ("172.17.69.107", 5313)

mensaje = "Cherry, cerra el orto"


sock_input, sock_output = utils.create_socket(SERVER_A)
try:
    resp = utils.send_message(sock_input, sock_output, mensaje)
except Exception as e:
    print(e)
    input.close()


print("Modo hacker")
#Transformo el cifrado hexagonal en bytes
C_bytes = utils.hex_to_bytes(resp)

#separo c_bytes en bloques de 16
C_block = utils.split_blocks(C_bytes, SIZE_BLOCK)
Cn = C_block[-1] #Obtengo el ultimo bloque
Cn_menos_1 = C_block[-2]#obtengo el penultimo bloque

#Obtengo el ultimo bytes
Cn_last_byte = Cn[SIZE_BLOCK-1]
Cn_menos_last_byte = Cn_menos_1[SIZE_BLOCK-1]
# guardo en una variable  Cn-1
Mn_menos_1=Cn_menos_1
# Mn-1[BlockSize-1]=[0x00]
Mn_menos_1[SIZE_BLOCK-1]=0
#mientras Dn[blockSize-1]!=[0x00],aumentar Mn-1[BlockSize-1] en 1

i=1
sock_input, sock_output = utils.create_socket(SERVER_B)
while i<=256:
    print("[{},256]".format(i))
    #Creo una copia de c_block
    C_block_copy =C_block
    #Cambio Cn-1 por Mn-1
    C_block_copy[-2]=Mn_menos_1
    #Junto los bloques y lo paso a hexagonal
    C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block_copy))
    #Envio el mensaje codificado al servidor B
    resp2 = utils.send_message(sock_input, sock_output, C_Modificado)

    if "pkcs7:" in resp2:
        Mn_menos_1[SIZE_BLOCK-1]=i
        i+=1
    elif i==256:
        print("Saldre poque el while ya no cumple la condicion")
    else:
        Mn_menos_1_respaldo=Mn_menos_1
        #cambio M_n-1[Size_BLOCK-2] a cualquier wea
        Mn_menos_1[SIZE_BLOCK-2]=1
        #Cambio Cn-1 por Mn-1
        C_block_copy[-2]=Mn_menos_1
        #Junto los bloques y lo paso a hexagonal
        C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block_copy))
        #Envio el mensaje codificado al servidor B
        resp3 = utils.send_message(sock_input, sock_output, C_Modificado)

        if not "pkcs7:" in resp3:
            print("sali del while por padding verificado")
            break
        #else:
            #print("era posible padding pero fallo la segunda")

# XOR entre Mn-1[SIZE_BLOCK-1] y [0x01]
In_last_int = (i-1)^1

print("Mn-1: {}".format(Mn_menos_1_respaldo[SIZE_BLOCK-1] ))
print("[0X0{}]".format(i-1))
print("In: {}".format(In_last_int))

# XOR Cn-1[SIZE_BLOCK-1] y In[SIZE_BLOCK-1]
Bn_last_caracter=Cn_menos_1[SIZE_BLOCK-1] ^ In_last_int

#Bn en formato string
print("Bn_int: {}".format(Bn_last_caracter))
#Bn en formato hexadecimal
print("Bn_hexadecimal: {}".format(str(Bn_last_caracter).encode('utf-8').hex()))
