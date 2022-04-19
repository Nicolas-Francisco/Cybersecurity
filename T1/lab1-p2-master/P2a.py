# P2a - Comente qué ocurre en cada servicio con distintos tipos de entradas.
# En el caso del servicio A. ¿Qué pasa con el largo de la salida al variar el largo
# de la entrada? En el caso del servicio B, ¿Qué pasa si varía caracteres del valor
# recibido de A al enviarlos a B? ¿Qué pasa si envía algo completamente
# distinto?

# para estudiar la variación del largo del mensaje cifrado de salida, 
# crearemos un excel donde se guardará el mensaje enviado (que será creciente)
# y el mensaje cifrado para estudiar su largo y como este varía.

import socket
import utils
import xlsxwriter

# Inicializamos un libro excel
libro = xlsxwriter.Workbook('ParteA.xlsx')
hoja = libro.add_worksheet()

# Cabecera del libro excel.
hoja.write(0,0,"Mensaje")
hoja.write(0,1,"Largo mensaje")
hoja.write(0,2,"Texto cifrado")
hoja.write(0,3,"Largo cifrado")

# We connect to a (host,port) tuple
CONNECTION_ADDR = ("172.17.69.107", 5312)

# Utilizamos la conexión de socket como se vió en redes
if __name__ == "__main__":
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    i=1
    while True:
        try:
            print("["+str(i)+"/666]")
            # Mientras el largo de M sea menor a 666, seguiremos enviando mensajes
            if i<666:
                cifrado_max=""
                max_val=0

                # Intentamos cada mensaje 3 veces para quedarnos con el valor más alto
                # Es posible que por la latencia de la conexión a internet, el largo
                # del mensaje cifrado C sea menor al que debería ser.
                for j in range(0,3):
                    mensaje = "J"*i
                    resp = utils.send_message(sock_input, sock_output, mensaje)
                    if len(resp) > max_val:
                        cifrado_max = resp
                        max_val = len(resp)

                # escribimos en el excel
                hoja.write(i,0,mensaje)
                hoja.write(i,1,i)
                hoja.write(i,2,cifrado_max)
                hoja.write(i,3,max_val)
                i+=1
            else:
                # cerramos la conexión
                libro.close()
                break

        except Exception as e:
            print(e)
            print("Closing...")
            input.close()
            break


# RESPUESTA:
# Al ir aumentando el tamaño del mensaje M, el largo del mensaje cifrado C
# va aumentando de a bloques. Esto puede observarse en el excel generado 
# con el programa anterior, ya que después de cirto largo, el largo del
# mensaje C aumenta hasta llegar a un tope de 352 carácteres.

# Por otro lado, al modificar un solo carácter del mensaje cifrado enviado
# al servidor B este lanza algún error de inconsistencia del mensaje (ya
# sea que el ultimo byte no calza con el padding, que existe un carácter 
# inválido, o que existe un byte que no corresponde a codificación hexadecimal).
# Mientras que si se modifica gran parte del mensaje cifrado, el servidor
# sigue lanzando algún error de inconsistencia (como un input JSON inesperado),
# pero este tarda un poco más en informarlo.