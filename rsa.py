import random

data = {
    "p": 44617,
    "q": 32969,
    "N": 1470977873,
    "phi_N": 1470900288,
    "e": 596208931,
    "d": 526837387,
    "PARTNER_N": 2141370397,
    "PARTNER_e": 133106707,
    "PARTNER_MESSAGE": [230459415, 273247991, 773614679, 996343186, 1043904371, 1010832043],
    "PARTNER_SIGNATURE": [1315603004, 307792732, 1258840492, 1574387229],
    "PARTNER_SIGNED_MESSAGE": "Amir Souri"
}

''' reset file '''
def reset_file(filename="myData.txt"):
    with open(filename, "w") as f:
        f.write("")

''' write data to file '''
def write_data(data, filename="myData.txt"):
    with open(filename, "a") as f:
        f.write(data+"\n")
        print(data)

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

''' calculate gcd '''
def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

''' calculate the modular inverse from e and phi '''
def mod_inverse(e, phi):
    # d -> ed = 1(mod phi)        ; 1 < d < phi
    d = 2
    while d < phi:
        # check if this is the required `d` value
        if ((d*e) % phi)==1:
            return d
        # else : increment and continue
        d += 1

''' generate p and q as per the given keysize '''
def generate_p_and_q(keysize):
    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [i for i in range(nMin+1, nMax, 2) if isprime(i)]

    p = random.choice(primes)
    primes.remove(p)
    q = random.choice(primes)

    write_data('p = '+str(p))
    data["p"] = p
    write_data('q = '+str(q))
    data["q"] = q

    return (p, q)

''' generate public and private keys '''
def generate_keys(p, q):
    # Calculate N = p * q
    N = p*q
    write_data('N = '+str(N))
    data["N"] = N

    # Calculate Phi(N)
    phi = (p-1) * (q-1) 
    write_data('phi_N = '+str(phi))
    data["phi_N"] = phi_N

    # Choose an integer 'e' such that 'e' and phi(n) are coprime
    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    # e -> gcd(e, phi) == 1      ; 1 < e < phi
    e = random.randrange(1, phi - 1)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi - 1)
        g = gcd(e, phi)
    write_data('e = '+str(e))
    data["e"] = e

    d = mod_inverse(e, phi)
    write_data('d = '+str(d))
    data["d"] = d

    public_key = (e, N)
    private_key = (d, N)

    return (public_key, private_key)

''' power mod '''
def power_mod(b, e, m):
    str_bin = bin(e).replace("0b", "")
    # print(str_bin)

    list_bin = list(map(int, str_bin))
    # print(list_bin)

    reverse_list_bin = list_bin[::-1]
    # print(reverse_list_bin)

    list_with_square_value = [b % m]
    for i in range(1, len(reverse_list_bin)):
        list_with_square_value.append(pow(list_with_square_value[i-1], 2, m))
    # print("list_with_square_value =", list_with_square_value)

    product = 1
    for i in range(len(reverse_list_bin)):
        if (reverse_list_bin[i] == 1):
            product = product * list_with_square_value[i]

    r = product % m

    return r

''' encrypt message '''
def encryption(m, e, n):
    print("\n# encryption")
    print("MY_MESSAGE =", m)
    
    MY_MESSAGE_chunks = [m[i:i+3] for i in range(0, len(m), 3)]
    print("MY_MESSAGE_chunks =", MY_MESSAGE_chunks)
    
    MY_MESSAGE_chunks_hex = [chunk.encode('utf-8').hex() for chunk in MY_MESSAGE_chunks]
    print("MY_MESSAGE_chunks_hex =", MY_MESSAGE_chunks_hex)
    
    MY_MESSAGE_chunks_int = [int(chunk, 16) for chunk in MY_MESSAGE_chunks_hex]
    print("MY_MESSAGE_chunks_int =", MY_MESSAGE_chunks_int)
    
    MY_CIPHERTEXT = [pow(chunk, e, n) for chunk in MY_MESSAGE_chunks_int]
    print("MY_CIPHERTEXT =", MY_CIPHERTEXT)

    return MY_CIPHERTEXT

''' decrypt message '''
def decryption(PARTNER_CIPHERTEXT, d, n):
    print("\n# decryption")
    print("PARTNER_CIPHERTEXT =", PARTNER_CIPHERTEXT)

    PARTNER_MESSAGE_chunks_int = [pow(chunk, d, n) for chunk in PARTNER_CIPHERTEXT]
    print("PARTNER_MESSAGE_chunks_int =", PARTNER_MESSAGE_chunks_int)
    
    PARTNER_MESSAGE_chunks_hex = [hex(chunk) for chunk in PARTNER_MESSAGE_chunks_int]
    print("PARTNER_MESSAGE_chunks_hex =", PARTNER_MESSAGE_chunks_hex)
    
    PARTNER_MESSAGE_chunks = [bytes.fromhex(chunk[2:]).decode('utf-8') for chunk in PARTNER_MESSAGE_chunks_hex]
    print("PARTNER_MESSAGE_chunks =", PARTNER_MESSAGE_chunks)
    
    PARTNER_MESSAGE = "".join(PARTNER_MESSAGE_chunks)
    print("PARTNER_MESSAGE =", PARTNER_MESSAGE)

    return PARTNER_MESSAGE

''' sign message '''
def sign(m, d, n):
    print("\n# sign")
    print("MY_MESSAGE_TO_BE_SIGNED =", m)
    
    MY_MESSAGE_TO_BE_SIGNED_chunks = [m[i:i+3] for i in range(0, len(m), 3)]
    print("MY_MESSAGE_TO_BE_SIGNED_chunks =", MY_MESSAGE_TO_BE_SIGNED_chunks)
    
    MY_MESSAGE_TO_BE_SIGNED_chunks_hex = [chunk.encode('utf-8').hex() for chunk in MY_MESSAGE_TO_BE_SIGNED_chunks]
    print("MY_MESSAGE_TO_BE_SIGNED_chunks_hex =", MY_MESSAGE_TO_BE_SIGNED_chunks_hex)
    
    MY_MESSAGE_TO_BE_SIGNED_chunks_int = [int(chunk, 16) for chunk in MY_MESSAGE_TO_BE_SIGNED_chunks_hex]
    print("MY_MESSAGE_TO_BE_SIGNED_chunks_int =", MY_MESSAGE_TO_BE_SIGNED_chunks_int)
    
    MY_SIGNATURE = [pow(chunk, d, n) for chunk in MY_MESSAGE_TO_BE_SIGNED_chunks_int]
    print("MY_SIGNATURE =", MY_SIGNATURE)

    return MY_SIGNATURE

''' verify message '''
def verify(PARTNER_SIGNATURE, PARTNER_SIGNED_MESSAGE, d, n):
    print("\n# verify the signature")
    print("PARTNER_SIGNED_MESSAGE =", PARTNER_SIGNED_MESSAGE)

    print("PARTNER_SIGNATURE =", PARTNER_SIGNATURE)
    PARTNER_SIGNATURE_chunks_int = [pow(chunk, d, n) for chunk in PARTNER_SIGNATURE]
    print("PARTNER_SIGNATURE_chunks_int =", PARTNER_SIGNATURE_chunks_int)
    
    PARTNER_SIGNATURE_chunks_hex = [hex(chunk) for chunk in PARTNER_SIGNATURE_chunks_int]
    print("PARTNER_SIGNATURE_chunks_hex =", PARTNER_SIGNATURE_chunks_hex)
    
    PARTNER_SIGNATURE_chunks = [bytes.fromhex(chunk[2:]).decode('utf-8') for chunk in PARTNER_SIGNATURE_chunks_hex]
    print("PARTNER_SIGNATURE_chunks =", PARTNER_SIGNATURE_chunks)
    
    PARTNER_VERIFIED_MESSAGE = "".join(PARTNER_SIGNATURE_chunks)
    print("PARTNER_VERIFIED_MESSAGE =", PARTNER_VERIFIED_MESSAGE)

    return PARTNER_VERIFIED_MESSAGE == PARTNER_SIGNED_MESSAGE

if __name__ == "__main__":
    # utility: reset text file
    # reset_file()

    if(data.get('p') and data.get('q') and data.get('N') and data.get('phi_N') and data.get('e') and data.get('d')):
        print("\n# my data")
        print("p =",data.get('p'))
        print("q =",data.get('q'))
        print("N =",data.get('N'))
        print("phi_N =",data.get('phi_N'))
        print("e =",data.get('e'))
        print("d =",data.get('d'))
        print("Public Key: (e, N) =",(data.get('e'), data.get('N')))
        print("Private Key: (d, N) =",(data.get('d'), data.get('N')))
    else:
        p, q = generate_p_and_q(16)

        public, private = generate_keys(p, q)
        print("Public Key: (e, N) =", public)
        print("Private Key: (d, N) =", private)

    MY_CIPHERTEXT = encryption("Bonjour, Amir",data.get('PARTNER_e'), data.get('PARTNER_N'))
    PARTNER_MESSAGE_AFTER_DECRYPT = decryption(data.get('PARTNER_MESSAGE'), data.get('d'), data.get('N'))

    MY_SIGNATURE = sign("Faiza Tahsin", data.get('d'), data.get('N'))
    IS_VALID_SIGNATURE = verify(data.get('PARTNER_SIGNATURE'), data.get('PARTNER_SIGNED_MESSAGE'), data.get('PARTNER_e'), data.get('PARTNER_N'))
    print("IS_VALID_SIGNATURE", IS_VALID_SIGNATURE)
