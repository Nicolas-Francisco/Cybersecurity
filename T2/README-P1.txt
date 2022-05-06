__________________________________________________
        Tarea 2 - Seguridad Computacional
        Nicolás García, Javier Lavados               

HOW_TO_RUN

El programa P1.py es un servidor que simplemente recibe
un mensaje, lo parsea según un log específico, y luego
lo comprime con AES-CBC. Para ejecutarlo, basta con tener
un cliente que se conecte a la misma IP y puerto, y que
sea capaz de enviar un mensaje al servidor. 

En este caso, un cliente simple será el programa P2a.py,
y para ejecutarlo de forma local basta correr:

> python P1.py
> python P2a.py

Ambos comandos en distintas consolas y en los mismos
directorios.

La consola que ejecute P2a.py será el cliente, que 
enviará un mensaje enviado por el usuario en la consola
al servidor, mientras que la consola del servidor 
mostrará lo solicitado por la P1