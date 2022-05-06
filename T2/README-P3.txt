___________________________________________________________
             Tarea 2 - Seguridad Computacional
              Nicolás García, Javier Lavados               

HOW_TO_RUN

Para poder conectarse a traves de la conexión VPN del CEC, 
basta ingresar la IP brindada por la VPN en el parámetro 
<IP> con los siguientes comandos:

> python Server.py <IP>
> python Client.py <IP>

Ambos comandos en distintas consolas y en los mismos 
directorios. Así, se podrá efectuar el ataque con un 
servidor funcional en una IP del CEC.

Para el caso de efectuar el ataque en un servidor con el 
proceso inverso (cifrar-comprimir en vez de comprimir-cifrar),
es necesario ejecutar los siguientes comandos:

> python Inverted_Server.py <IP>
> python Client.py <IP>

___________________________________________________________
a) ¿En qué afecta esto al protocolo?

b) ¿En qué afecta esto al ataque?

c) Proponga un cambio más eficiente al propuesto