# P2d - Cree una función que permita descifrar el 
# último carácter del texto cifrado.

# Para lo anterior, programaremos el algoritmo descrito en el 
# enunciado de la tarea.

from ctypes.wintypes import SIZE
import utils
SIZE_BLOCK = 16 # bytes

# Tupla para la conexión entre los servidores
SERVER_A= ("172.17.69.107", 5312)
SERVER_B = ("172.17.69.107", 5313)

# mensaje por defecto para la prueba
mensaje = "si puedes leer esto, eres un hacker"

def last_byte_decypher(mensaje, position, Ins):
    sock_input, sock_output = utils.create_socket(SERVER_A)

    # Enviamos el mensaje y conseguimos su codificación
    try:
        resp = utils.send_message(sock_input, sock_output, mensaje)
    except Exception as e:
        print(e)
        input.close()

    # Transformamos el cifrado hexagonal en bytes
    C_bytes = utils.hex_to_bytes(resp)

    # se separa c_bytes en bloques de 16
    C_block = utils.split_blocks(C_bytes, SIZE_BLOCK)
    Cn = C_block[-1]            # Obtengo el ultimo bloque
    Cn_menos_1 = C_block[-2]    # Obtengo el penultimo bloque

    # Se obtienen los ultimos bytes de cada bloque
    #Cn_last_byte = Cn[SIZE_BLOCK-1]
    #Cn_menos_last_byte = Cn_menos_1[SIZE_BLOCK-1]

    # Se guarda Cn-1 en una variable nueva
    Mn_menos_1=Cn_menos_1

    if position != SIZE_BLOCK:
        for j in range(position,SIZE_BLOCK):
            #Mn-1[J]=In-1[J]+(Blocksize-position)
            Mn_menos_1[j]=Ins[0]^(SIZE_BLOCK-position+1)

    # Mn-1[BlockSize-1]=[0x00]
    Mn_menos_1[position-1]=0

    # while Dn[blockSize-1]!=[0x00], aumentar Mn-1[BlockSize-1] en 1
    # y seguir su verificación
    i=1
    sock_input, sock_output = utils.create_socket(SERVER_B)
    while i < 256:
        #print("[{},256]".format(i))

        # creamos una copia de c_block
        C_block_copy =C_block

        # cambiamos Cn-1 por Mn-1
        C_block_copy[-2] = Mn_menos_1

        # juntamos ambos bloques y se pasan a hexadecimal
        C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block_copy))

        # Se envia el nuevo mensaje codificado al servidor B
        resp2 = utils.send_message(sock_input, sock_output, C_Modificado)

        # Si el servidor B responde con un mensaje de error
        if "pkcs7:" in resp2: 
            # Avanzamos el i en 1
            Mn_menos_1[position-1] = i
            i+=1


        # Si no hubo error
        else:
            # recuperamos el respaldo para no perder la referencia
            Mn_menos_1_respaldo = Mn_menos_1

            # Cambiamos M_n-1[Size_BLOCK-2] a otro byte
            Mn_menos_1[position-2]=1

            # Reemplazamos Cn-1 por Mn-1
            C_block_copy[-2]=Mn_menos_1

            # Se juntan los bloques y se pasan a hexadecimal
            C_Modificado=utils.bytes_to_hex(utils.join_blocks(C_block_copy))

            # Se envía el mensaje codificado al servidor B
            resp3 = utils.send_message(sock_input, sock_output, C_Modificado)

            # si nuevamente no lanza error, entonces encontramos un padding verificado
            if not "pkcs7:" in resp3:
                print("VERIFIED PADDING")
                break

    print("------------------------------")
    # XOR entre Mn-1[SIZE_BLOCK-1] y [0x01]
    In_last_int = (i-1)^(SIZE_BLOCK-position+1)

    # Printeamos los resultados obtenidos del programa
    print("Mn-1: {}".format(Mn_menos_1_respaldo[position-1] ))
    print("[0X0{}]".format(i-1))
    print("In: {}".format(In_last_int))

    # XOR Cn-1[SIZE_BLOCK-1] y In[SIZE_BLOCK-1]
    Bn_last_caracter=Cn_menos_1[position-1] ^ In_last_int

    # Bn en formato string
    print("Bn_int: {}".format(Bn_last_caracter))
    # Bn en formato hexadecimal
    print("Bn_hexadecimal: {}".format(str(Bn_last_caracter).encode('utf-8').hex()))
    Ins.append(In_last_int)
    return Ins

if __name__ == "__main__":
    arrayIns=[]
    arrayIns=last_byte_decypher(mensaje,16,arrayIns)
    arrayIns=last_byte_decypher(mensaje,15,arrayIns)