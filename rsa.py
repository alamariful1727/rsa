import random

def isprime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

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

if __name__ == "__main__":
    p, q = generate_p_and_q(16)
    # p, q = (52457, 39509)
    print(p, q)