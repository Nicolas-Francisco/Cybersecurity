import socket

# We connect to a (host,port) tuple
import utils
import xlsxwriter


libro = xlsxwriter.Workbook('ParteA.xlsx')
hoja = libro.add_worksheet()

hoja.write(0,0,"Mensaje")
hoja.write(0,1,"Largo mensaje")
hoja.write(0,2,"Texto cifrado")
hoja.write(0,3,"Largo cifrado")

CONNECTION_ADDR = ("172.17.69.107", 5312)

if __name__ == "__main__":
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    i=1
    while True:
        try:
            print("["+str(i)+"/666]")
            if i<666:
                cifrado_max=""
                max_val=0
                for j in range(0,3):
                    mensaje = "J"*i
                    resp = utils.send_message(sock_input, sock_output, mensaje)
                    if len(resp)>max_val:
                        cifrado_max=resp
                        max_val=len(resp)

                hoja.write(i,0,mensaje)
                hoja.write(i,1,i)
                hoja.write(i,2,cifrado_max)
                hoja.write(i,3,max_val)
                i+=1
            else:
                libro.close()
                break

        except Exception as e:
            print(e)
            print("Closing...")
            input.close()
            break
