# Tarea 1 - Informe
### Javier Lavados Jilbert, Nicolás García Ríos

## P2
### a)
Para estudiar la variación del largo del mensaje cifrado de salida,  crearemos un excel donde se guardará el mensaje enviado (que será creciente) y el mensaje cifrado para estudiar su largo y como este varía. (ver P2a.py).

Al ir aumentando el tamaño del mensaje M, el largo del mensaje cifrado C va aumentando de a bloques. Esto puede observarse en el excel generado  con el programa anterior, ya que después de cirto largo, el largo del mensaje C aumenta hasta llegar a un tope de 352 carácteres.

Por otro lado, al modificar un solo carácter del mensaje cifrado enviado al servidor B este lanza algún error de inconsistencia del mensaje (ya sea que el ultimo byte no calza con el padding, que existe un carácter  inválido, o que existe un byte que no corresponde a codificación hexadecimal). 

Mientras que si se modifica gran parte del mensaje cifrado enviando un  mensaje C completamente distinto a los registrados por el programa, el servidor sigue lanzando algún error de inconsistencia (como un input JSON inesperado), pero este tarda un poco más en informarlo.
### b)
Para esta parte solo basta con conectarse a ambos puertos de la IP y enviar al servidor B el mensaje recibido por el servidor A después de enviar un mensaje a cifrar. (ver P2b.py)
### c)
Para esto, crearemos un programa parecido al anterior, pero que este detecte los cambios del tamaño del mensaje C para poder calcular de forma automática el tamaño del bloque. (ver P2c.py)
### d)
Para esta parte solamente se implementó el algoritmo descrito en el enunciado de la tarea. (ver P2d.py)
### e)
Se extiende la parte anterior, iterando de 1 a BLOCKSIZE la función programada para desencriptar el último bloque.  (ver P2e.py)
### f)
Se extiende lo anterior para iterar sobre los k bloques del mensaje. En este caso, es necesario decifrar el último bloque del mensaje cifrado, e ir sacando cada bloque del mismo para cifrar iterativamente. Al final se obtiene la lista de In's y Todos los Bn's listos para poder obtener la llave del cifrado. (ver P2f.py). Debido a problemas de tiempo no fue posible probar esta solución.

## How to Run
Se creó un archivo python por cada funcionalidad de la Tarea, por lo que es posible testear cada sección de la pregunta 2 por separado usando ```python P2<section>.py```. En el caso de querer ejecutar toda la P2, basta con ejecutar el comando ```python P2f.py```.