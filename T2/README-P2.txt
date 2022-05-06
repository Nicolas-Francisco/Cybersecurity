___________________________________________________________
             Tarea 2 - Seguridad Computacional
              Nicolás García, Javier Lavados               

HOW_TO_RUN

El programa Client.py es el cliente que efectua el ataque 
CRIME descrito en la P2. Este ataca al servidor a partir de 
los mensajes que recibe del mismo, utilizando los largos y 
un segmento conocido de los mensajes enviados por el servidor. 

Para ejecutarlo, es necesario conectarse al servidor 
programado en la P1. Así, se deben ejecutar los comandos:

> python Server.py <IP>
> python Client.py <IP>

Ambos comandos en distintas consolas y en los mismos 
directorios, donde <IP> es un parámetro dado por el usuario,
y que en particular puede ser <IP>='localhost' para su 
funcionamiento local.

La consola que ejecute Client.py será el cliente, que 
imprimirá los logs solicitados en la pregunta y que al final
del ataque imprimirá el secreto utilizado por el servidor.