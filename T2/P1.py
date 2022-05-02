import socket
import sys
import utils
import time

CONNECTION_ADDR = ('localhost', 5327)

formatMessage = "GET {} HTTP/1.1\nCookie: secret={}\nHost: cc5325.dcc\n\n"
SECRET = "H0LAaaa3ST03SUNS3CRE70MUYS3CR3T0"


if __name__ == "__main__":
    sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_output = sock_input.makefile(errors="ignore")

    sock_input.bind(CONNECTION_ADDR)
    sock_input.listen(5)

    while True:
        conn, addr = sock_input.accept()

        actual_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("Fecha del log: {}".format(actual_time))
       
        while True:
            try:
                data = conn.recv(1024)
                

            except Exception as e:
                print(e)
                print("Closing...")
                input.close()
                break

            print("Texto en request recibida: {}".format(data.decode()))
            print("IP en request recibida: {}".format())
            

            conn.send("Mensaje recibido :D".encode())
        conn.close()
        print('Desconecta3')