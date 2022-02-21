import random

''' check prime number '''
def isprime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

''' generate p and q as per the given keysize '''
def generate_p_and_q(keysize):
    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [i for i in range(nMin+1, nMax, 2) if isprime(i)]

    # print("primes",primes)
    # print("len(primes)",len(primes))

    p = random.choice(primes)
    primes.remove(p)
    q = random.choice(primes)

    return (p, q)

''' calculate gcd '''
def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

''' calculate the modular inverse from e and phi '''
def mod_inverse(e, phi):
    # d -> ed = 1(mod z)        ; 1 < d < z
    d = 2
    while d < phi:
        # check if this is the required `d` value
        if ((d*e) % phi)==1:
            return d
        # else : increment and continue
        d += 1

''' generate public and private keys '''
def generate_keys(p, q):
    # Calculate N = p * q
    N = p*q
    print("N ", N)

    # Calculate Phi(N)
    phi = (p-1) * (q-1) 
    print("phi ", phi)

    # Choose an integer 'e' such that 'e' and phi(n) are coprime
    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    # e -> gcd(e,z)==1      ; 1 < e < z
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    print("e ", e)

    d = mod_inverse(e, phi)
    print("d ", d)

    public_key = (e, N)
    private_key = (d, N)

    return (public_key, private_key)

if __name__ == "__main__":
    # p, q = generate_p_and_q(16)
    p, q = (52457, 39509)
    print("p: ", p)
    print("q: ", q)

    public, private = generate_keys(p, q)
    print("Public Key: ", public)
    print("Private Key: ", private)