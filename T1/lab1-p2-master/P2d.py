# P2d - Cree una función que permita descifrar el último carácter del texto cifrado.

import socket
import utils
import P2c

CONNECTION_ADDR = ("172.17.69.107", 5312)

if __name__ == "__main__":
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    try:
        # Read a message from standard input
        response = input("send a message: ")
        # You need to use encode() method to send a string as bytes.
        print("[Client] \"{}\"".format(response))
        resp = utils.send_message(sock_input, sock_output, response)
        print("[Server] \"{}\"".format(resp))
        # Wait for a response and disconnect.
    except Exception as e:
        print(e)
        print("Closing...")
        input.close()

print("modo hacker")

SIZE_BLOCK=16 #bites
# 8ef08288f8420315f91a870556d8b1086e098634e3e799ac5cd8119e105afb5d5cce400ea39c11561ecc4c2
C= bytearray.fromhex(resp) #[1,2,3,4,5,6,7,8]
len_c = len(C)
C_n = C[len_c-1]
