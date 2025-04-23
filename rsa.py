import random
import math

def is_prime(n, k=10):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bit_length):
     while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1
        if is_prime(candidate):
            return candidate

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        raise Exception("Modular inverse does not exist for these values.")
    return x % m


def generate_rsa_keys(prime_bit_length):
    p = generate_prime(prime_bit_length)
    q = generate_prime(prime_bit_length)
    # make sure q and p are different
    while q == p:
        q = generate_prime(prime_bit_length)

    n = p * q  # mod for both keys

    phi = (p - 1) * (q - 1)  # euler's thingy

    e = 65537  # internet said this was a good number

    d = mod_inverse(e, phi)  # private exponent

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def rsa_encrypt(message, public_key):
    # generate keys
    e, n = public_key

    # convert message from string to int.
    message_bytes = message.encode('utf-8')
    message_int = int.from_bytes(message_bytes, byteorder='big')

    # encrypt
    encrypted_string = pow(message_int, e, n)
    return encrypted_string


def rsa_decrypt(encrypted_string, private_key):
    d, n = private_key

    # decrypt
    decrypted_int = pow(encrypted_string, d, n)

    # convert decrypted integer back to bytes
    byte_length = (decrypted_int.bit_length() + 7) // 8
    decrypted_bytes = decrypted_int.to_bytes(byte_length, byteorder='big')
    return decrypted_bytes.decode('utf-8', errors='ignore')


if __name__ == "__main__":
    message = input("Enter message to encrypt: ")
    prime_bit_length = int(input("Enter prime bit length (try 16 or 32 or you will be here until sun explodes): "))

    try:
        encrypted_str, pub_key, priv_key = rsa_encrypt(message, prime_bit_length)
        print("\nEncrypted message:", encrypted_str)
        print("Public key (e, n):", pub_key)
        print("Private key (d, n):", priv_key)

        decrypted_message = rsa_decrypt(encrypted_str, priv_key)
        print("Decrypted message:", decrypted_message)
    except ValueError as e:
        print("Error:", e)