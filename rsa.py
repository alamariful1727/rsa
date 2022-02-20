from math import sqrt
import random

def isprime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
    return True

def generate_p_and_q(keysize):
    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [2]

    # print("nMin", nMin)
    # print("nMax", nMax)

    for i in range(3, nMax, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)

    # print("primes",primes)
    # print("len(primes)",len(primes))

    filteredPrimes = [prime for prime in primes if prime > nMin]
    # print("len(filteredPrimes)",len(filteredPrimes))

    p = random.choice(filteredPrimes)
    filteredPrimes.remove(p)
    q = random.choice(filteredPrimes)

    return (p, q)

if __name__ == "__main__":
    p, q = generate_p_and_q(16)    