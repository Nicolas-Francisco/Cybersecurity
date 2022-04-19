# P2c - Usando el código anterior, determine una estrategia 
# para calcular el tamaño del bloque usado en el texto cifrado 
# a través de una función que lo calcule de forma automática. 
# Explique justificadamente por qué ocurre esto.

# Respuesta:
# Para esto, crearemos un programa parecido al anterior, pero que este
# detecte los cambios del tamaño del mensaje C para poder calcular de
# forma automática el tamaño del bloque.
import socket
from tarfile import BLOCKSIZE
import utils

# Creamos las tuplas (IP, puerto) de ambos servidores
ServerA = ("172.17.69.107", 5312)
ServerB = ("172.17.69.107", 5313)
BLOCK_SIZE = 0

if __name__ == "__main__":
    sock_input_A, sock_output_A = utils.create_socket(ServerA)
    sock_input_B, sock_output_B = utils.create_socket(ServerB)
    it = 1
    last_c = ""
    while True:
        try:
            # Creamos un mensaje base que irá aumentando hasta detectar el 
            # salto del tamaño de C
            M = "1" * it
            print("[Client] \"{}\"".format(M))

            # Se envía el mensaje M al servidor A
            resp_A = utils.send_message(sock_input_A, sock_output_A, M)

            # Se evía el mensaje cifrado C enviado por A al servidor B
            resp_B = utils.send_message(sock_input_B, sock_output_B, resp_A)
            
            dif = len(resp_A) - len(last_c)
            # Mientras el largo del último C sea menor, continuamos iterando
            if dif > 0 and it > 1:
                # Debido a que estamos trabajando con un string hexadecimal,
                # dos carácteres conjuntos forman un byte
                BLOCK_SIZE = dif//2 #bytes
                print("BLOCK_SIZE: \"{}\"".format(BLOCK_SIZE))
                break
            else:
                last_c = resp_A
                it += 1

        except Exception as e:
            print(e)
            print("Closing...")
            break