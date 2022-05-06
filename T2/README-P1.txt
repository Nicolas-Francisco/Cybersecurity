___________________________________________________________
             Tarea 2 - Seguridad Computacional
              Nicolás García, Javier Lavados               

HOW_TO_RUN

El programa Server.py es un servidor que simplemente recibe
un mensaje, lo parsea según un log específico, y luego lo 
comprime con AES-CBC. Para ejecutarlo, basta con tener un 
cliente que se conecte a la misma IP y puerto, y que sea 
capaz de enviar un mensaje al servidor. 

En este caso, un cliente simple será el programa 
basic_client.py, y para ejecutarlo de forma local basta 
ejecutar los siguientes comandos:

> python Server.py <IP>
> python basic_client.py <IP>

Ambos comandos en distintas consolas y en los mismos 
directorios, donde <IP> es un parámetro dado por el usuario,
y que en particular puede ser <IP>='localhost' para su 
funcionamiento local.

La consola que ejecute basicClient.py será el cliente, que 
enviará un mensaje enviado por el usuario en la consola al 
servidor, mientras que la consola del servidor mostrará lo 
solicitado por la P1.