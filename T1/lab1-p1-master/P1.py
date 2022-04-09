'''
a)  El problema de la implementación de RSA es que el algoritmo
    de generación de claves no ocupa dos primos aleatorios, sino 
    que obtiene uno en función del otro (utilizando la función
    next_prime). Esto lleva a que no tenemos aleatoriedad real
    sobre ambos primos, vulnerando la seguridad de la clave.

b)  Debido a que p y q son primos consecutivos, sabemos de primera 
    mano que p < q. Además, estos dos valores no se distancian 
    tanto unos de otros.
    Por otro lado, podemos desarrollar N:
        N = p*q
        N = p*(p+x)         (usando p + x = q)
        N = p^2 + p*x
        
    Y además sabemos que q^2 > pq = N. Luego:
        sqrt(N) = sqrt(p*q) < sqrt(q^2) = q 
        sqrt(N) = sqrt(p^2 + p*x)   (por el desarrollo anterior)
    
    Finalmente p = sqrt(p^2) < sqrt(p^2 + p*x) < sqrt(q^2) = q,
    o en otras palabras:
        p < sqrt(N) < q

    Así, tenemos que para encontrar p y q basta encontrar el 
    siguiente número primo de sqrt(N). 


c)  Utilizaremos b) para programar una solución que nos permita
    quebrar la implementación de RSA.
'''

import constants
import decimal
from utils import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

decimal.getcontext().prec = 4096

def break_rsa(N):
    """
    break_rsa breaks RSA encryption by finding the factors of N.
    :param N: RSA modulus, the product of two primes p and q
    :return: p, q
    """
    # We use the fact that N = p*q and that p and q are consecutives
    # We find the square root of N
    sqrt_N = int(decimal.Decimal(N).sqrt())

    # We find the next prime number after sqrt_N
    q = next_prime(sqrt_N)

    # We find p using q
    p = N // q

    return p, q

def decipher_Doc(cipheredDoc, p, q):
    '''
    decipher_Doc deciphers the cipheredDoc using the private key
    the private key is obtained using p, q and the funcition
    new_fixed_rsa_key, that generates the key
    :param cipheredDoc: ciphered document
    :param p: first prime
    :param q: second prime
    '''
    sk = new_fixed_rsa_key(p, q)
    decipheredDoc = sk.decrypt(cipheredDoc, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))
    with open(constants.DECIPHERED_PATH_P1, 'wb') as f:
        print("Saving deciphered version of text by calculating p and q...")
        f.write(decipheredDoc)

if __name__ == "__main__":
    pk = load_public_key_file(constants.PUBLIC_KEY_PATH)
    N = get_n(pk)
    print("---------------------------")
    print("N:", N, "\n")
    p, q = break_rsa(N)
    print("p:", p,"\n", "q:", q, "\n") 
    with open(constants.CIPHERED_PATH, 'rb') as f:
        C = f.read()
        decipher_Doc(C, p, q) 