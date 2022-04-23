# P2e - Cree una función que permita descifrar el 
# último carácter del texto cifrado.

# Para lo anterior, programaremos el algoritmo descrito en el 
# enunciado de la tarea.

from tarfile import BLOCKSIZE
import utils
from datetime import datetime
now = datetime.now()

SIZE_BLOCK = 16 # bytes

# Tupla para la conexión entre los servidores
SERVER_A= ("172.17.69.107", 5312)
SERVER_B = ("172.17.69.107", 5313)

# mensaje por defecto para la prueba
mensaje = "eso tilin"

Ins = []
Bns = []

f = open ('P2e.txt','w')
f.write("Current Time = {}\n".format(now))

def last_byte_decypher(resp,i):


    # Transformamos el cifrado hexagonal en bytes
    C_bytes = utils.hex_to_bytes(resp)

    # se separa c_bytes en bloques de 16
    C_block = utils.split_blocks(C_bytes, SIZE_BLOCK)
    C_block_respaldo = utils.split_blocks(C_bytes, SIZE_BLOCK)

    Cn_menos_1 = C_block[-2]    # Obtengo el penultimo bloque

    # Se guarda Cn-1 en una variable nueva
    Mn_menos_1=Cn_menos_1

    if i < SIZE_BLOCK:
        for j in range(len(Ins)):
            #Mn-1[J]=In-1[J]+(Blocksize-position)
            Mn_menos_1[-j-1] = Ins[j]^(SIZE_BLOCK-i+1)

    # Se obtienen los ultimos bytes de cada bloque
    #Cn_last_byte = Cn[SIZE_BLOCK-1]
    #Cn_menos_last_byte = Cn_menos_1[SIZE_BLOCK-1]

    
    # Mn-1[BlockSize-1]=[0x00]
    Mn_menos_1[i-1]=0

    # while Dn[blockSize-1]!=[0x00], aumentar Mn-1[BlockSize-1] en 1
    # y seguir su verificación
    count=1
    sock_input, sock_output = utils.create_socket(SERVER_B)
    while count < 256:
        print("{}-[{}/256]".format(i,count))

        # creamos una copia de c_block
        C_block_copy = C_block

        # cambiamos Cn-1 por Mn-1
        C_block_copy[-2] = Mn_menos_1

        # juntamos ambos bloques y se pasan a hexadecimal
        C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block_copy))

        # Se envia el nuevo mensaje codificado al servidor B
        resp2 = utils.send_message(sock_input, sock_output, C_Modificado)

        # Si el servidor B responde con un mensaje de error
        if "pkcs7:" in resp2: 
            # Avanzamos el count en 1
            Mn_menos_1[i-1] = count
            count+=1

            if count==255:
                print("Saldre poque el while ya no cumple la condicion")
                exit()

        # Si no hubo error
        elif (i>1):
            # recuperamos el respaldo para no perder la referencia
            Mn_menos_1_respaldo = Mn_menos_1

            # Cambiamos M_n-1[Size_BLOCK-2] a otro byte
            Mn_menos_1[i-2]=1

            # Reemplazamos Cn-1 por Mn-1
            C_block_copy[-2]=Mn_menos_1

            # Se juntan los bloques y se pasan a hexadecimal
            C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block_copy))

            # Se envía el mensaje codificado al servidor B
            resp3 = utils.send_message(sock_input, sock_output, C_Modificado)

            Mn_menos_1=Mn_menos_1_respaldo

            # si nuevamente no lanza error, entonces encontramos un padding verificado
            if not "pkcs7:" in resp3:
                print("VERIFIED PADDING")
                break

            # si ya terminó y no se encontró, tenemos un error
            if count==255:
                print("Saldre poque el while ya no cumple la condicion")
                exit()
        else:
            break

    # XOR entre Mn-1[SIZE_BLOCK-1] y [0x01]
    In_last_int = (count-1)^(SIZE_BLOCK-i+1)

    

    # Printeamos los resultados obtenidos del programa
    f.write("\n")
    f.write("---------------------------------------------\n")
    f.write("\n")
    f.write("Es el paciente {}\n".format(i))
    f.write("Mn-1: {}\n".format(Mn_menos_1[i-1] ))
    f.write("[0X0{}]\n".format(count-1))
    f.write("In: {}\n".format(In_last_int))

    C_n_menos_1_original = C_block_respaldo[-2]

    # XOR Cn-1[SIZE_BLOCK-1] y In[SIZE_BLOCK-1]
    Bn=C_n_menos_1_original [SIZE_BLOCK-1] ^ In_last_int

    

    # Bn en formato string
    f.write("Bn_int: {}\n".format(Bn))
    # Bn en formato hexadecimal
    f.write("Bn_hexadecimal: {}\n".format(str(Bn).encode('utf-8').hex()))

    Bns.append(Bn)
    Ins.append(In_last_int)

if __name__ == "__main__":

    sock_input, sock_output = utils.create_socket(SERVER_A)
    # Enviamos el mensaje y conseguimos su codificación
    try:
        resp = utils.send_message(sock_input, sock_output, mensaje)
    except Exception as e:
        print(e)
        input.close()

    for j in range(16,0,-1):
        last_byte_decypher(resp,j)

    
    Bns_string = ""
    for k in Bns:
        Bns_string=str(k).encode('utf-8').hex()+Bns_string

    f.write("Bns en hex: {}\n".format(Bns_string))
    f.close()
    print(Bns_string)