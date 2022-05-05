import socket
import P2b

CONNECTION_ADDR = ('localhost', 5327)

if __name__ == "__main__":
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
            P2b.CRIME_ATTACK()

            
            print("-----------------------------------------------------")
        except Exception as e:
            print(e)
            print("Closing Client...")
            input.close()
            s.close()
            break
