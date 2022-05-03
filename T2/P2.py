import socket

# We connect to a (host,port) tuple
import utils

CONNECTION_ADDR = ('localhost', 5327)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(CONNECTION_ADDR)
    while True:
        try:
            # Read a message from standard input
            response = input("send a message: ")
            # You need to use encode() method to send a string as bytes.
            #print("[Client] \"{}\"".format(response))
            s.send(response.encode())
            resp = s.recv(4096).decode()    
            print("[Server] \"{}\"".format(resp))
            # Wait for a response and disconnect.
        except Exception as e:
            print(e)
            print("Closing...")
            input.close()
            s.close()
            break
