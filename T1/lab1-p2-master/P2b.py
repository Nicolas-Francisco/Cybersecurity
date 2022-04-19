import socket

# We connect to a (host,port) tuple
import utils

ServerA = ("172.17.69.107", 5312)
ServerB = ("172.17.69.107", 5313)

if __name__ == "__main__":
    sock_input_A, sock_output_A = utils.create_socket(ServerA)
    sock_input_B, sock_output_B = utils.create_socket(ServerB)

    while True:
        try:
            # Read a message from standard input
            response = input("send a message: ")

            # You need to use encode() method to send a string as bytes.
            print("[Client] \"{}\"".format(response))
            resp_A = utils.send_message(sock_input_A, sock_output_A, response)
            print("[ServerA] \"{}\"".format(resp_A))
            # Wait for a response and disconnect.

            resp_B = utils.send_message(sock_input_B, sock_output_B, resp_A)
            print("[ServerB] \"{}\"".format(resp_B))
            # Wait for a response and disconnect.


        except Exception as e:
            print(e)
            print("Closing...")
            input.close()
            break
