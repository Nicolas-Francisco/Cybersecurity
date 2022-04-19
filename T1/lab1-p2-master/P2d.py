# P2d - Cree una función que permita descifrar el último carácter del texto cifrado.

import socket
import utils
import P2c
SIZE_BLOCK = 16 # bytes

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

C = bytearray.fromhex(resp)

def get_last_block(C):
    return C[-SIZE_BLOCK:]

Cn = get_last_block(C)
Cn1 = get_last_block(C[0:-SIZE_BLOCK])
Cn_block1 = C[-1:]
Cn1_block1 = Cn1[-1:]
