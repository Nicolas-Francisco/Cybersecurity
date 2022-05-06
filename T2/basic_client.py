import socket
import sys

if len(sys.argv) != 2:
    print('Use: ' + 'IP VPN SERVIDOR')
    sys.exit(1)

CONNECTION_ADDR = (sys.argv[1], 5327)
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
            resp = s.recv(4096).decode()    
            print("[Server] \"{}\"".format(resp))
        except Exception as e:
            print(e)
            print("Closing...")
            input.close()
            s.close()
            break
