# P2d - Cree una función que permita descifrar el último carácter del texto cifrado.

from re import I
import socket
import utils
import P2c
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
Cn_menos_1 = C_block[-2]

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
    #Cambio Cn-1 por Mn-1
    C_block[-2]=Mn_menos_1
    #Junto los bloques y lo paso a hexagonal
    C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block))
    #Envio el mensaje codificado al servidor B
    resp2 = utils.send_message(sock_input, sock_output, C_Modificado)

    Mn_menos_1[-1:]=i
    i+=1

