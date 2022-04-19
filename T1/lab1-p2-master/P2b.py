# P2b - Utilice el código base para crear un programa que envíe un texto al
# servicio A, reciba su respuesta, envíe esa respuesta al servicio B y reciba la
# respuesta de este servicio.

# Para esta parte solo basta con conectarse a ambos puertos de la IP
# Y enviar al servidor B el mensaje recibido por el servidor A después
# de enviar un mensaje a cifrar.
import socket
import utils

# Creamos las tuplas (IP, puerto) de ambos servidores
ServerA = ("172.17.69.107", 5312)
ServerB = ("172.17.69.107", 5313)

if __name__ == "__main__":
    sock_input_A, sock_output_A = utils.create_socket(ServerA)
    sock_input_B, sock_output_B = utils.create_socket(ServerB)

    while True:
        try:
            # Se guarda el mensaje M a enviar al servidor A
            response = input("send a message: ")
            print("[Client] \"{}\"".format(response))

            # Se envía el mensaje M al servidor A
            resp_A = utils.send_message(sock_input_A, sock_output_A, response)
            print("[ServerA] \"{}\"".format(resp_A))

            # Se evía el mensaje cifrado C enviado por A al servidor B
            resp_B = utils.send_message(sock_input_B, sock_output_B, resp_A)
            print("[ServerB] \"{}\"".format(resp_B))

        except Exception as e:
            print(e)
            print("Closing...")
            input.close()
            break
