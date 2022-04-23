# Tarea 1 - Informe
### Javier Lavados Jilbert, Nicolás García Ríos
## P1
### a)
El problema de la implementación de RSA es que el algoritmo de generación de claves no ocupa dos primos aleatorios, sino que obtiene uno en función del otro (utilizando la función ```next_prime```. Esto lleva a que no tenemos aleatoriedad real sobre ambos primos, vulnerando la seguridad de la clave.

### b)
Debido a que $$p$$ y $$q$$ son primos consecutivos, sabemos de primera mano que $$p < q$$. Además, estos dos valores no se distancian tanto unos de otros. Por otro lado, podemos desarrollar $$N$$:

$$N = p*q $$


$$N = p*(p+x) $$


$$N = p^2 + p*x $$

(usando $$p + x = q$$ en la seguna igualdad)

Y además sabemos que $$q^{2} > pq = N$$. Luego:

$$sqrt(N) =  sqrt(p*q) < sqrt(q^2) = q$$

$$sqrt(N) =  sqrt(p^2 + p*x) < sqrt(q^2)$$

Finalmente $$p = sqrt(p^2) < sqrt(p^2 + p*x) < sqrt(q^2) = q$$, o en otras palabras, $$p < sqrt(N) < q$$

Así, tenemos que para encontrar $$p$$ y $$q$$ basta encontrar el  siguiente número primo de $$sqrt(N)$$. 
    
### c)  
Utilizaremos b) para programar una solución que nos permita quebrar la implementación de RSA. (ver P1.py)

## How to Run
Para ejecutar la P1 basta con ejecutar ```python P1.py```, pero también es necesario tener en la misma carpeta el archivo utils.py, y que el ayudante tenga la llave pública.