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

___________________________________________________________
a) ¿En qué afecta esto al protocolo?
R: Afecta al tamaño del mensaje. Debido a que ahora estamos 
   comprimiendo después de cifrar el mensaje, el protocolo 
   no registrará los cambios en la compresión del mensaje
   genérico enviado, pues este ahora comprime un cifrado de
   largo cte y que solo varía en bloques.


b) ¿En qué afecta esto al ataque?
R: Afecta a que ahora el cliente no puede detectar las 
   variaciones de los tamaños de la compresión del mensaje 
   conocido, impidiendo detectar los carácteres que componen
   el secreto y dejando inválido el ataque CRIME.


c) Proponga un cambio más eficiente al propuesto
R: El ataque puede ser optimizado al aplicar dicotomía. Si 
   se tiene un secreto en base 32 (existen 32 posible 
   valores por cada carácter) el cliente puede hacer requests 
   que contengan 16 copias del KNOWN 'Cookie: secret=X' para 
   16 variantes del  carácter X. Si alguna calza con el valor 
   real de SECRET, el largo comprimido será menor (como las 
   condiciones del ataque).

   Una vez se sepa que mitad de los 32 posibles valores de 
   X contiene, podemos hacer el mismo proceso sobre el cuarto 
   obtenido en el primer intento (esto es, probar con 8 
   posibles de los 16 encontrados en el primer intento). Ahora 
   tenemos búsqueda binaria, donde obtenemos el carácter válido 
   para una determinada posición en log_2(32) intentos.

   Esta optimización se pudo rescatar a partir de los anexos 
   de la tarea.
___________________________________________________________