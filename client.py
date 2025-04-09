import socket
import sys
import aes_cipher as aes
import random
sys.setrecursionlimit(100000)


def xgcd(a,b):
    if b ==0:
        return (a,1,b)
    else:
        d,x,y = xgcd(b,a%b)
        return (d,y,x-(a//b)*y)

def mod_mult(a,b,m):
    return(a*b)%m

def mod_square(a,m):
    return mod_mult(a,a,m)

def fast_pow_mod(a,b,m):
    if(b ==0):
        return 1
    elif(b%2 ==0):
        y = fast_pow_mod(a,b//2,m)
        z = mod_square(y,m)
        if (z==1 and y != 1 and y != m-1):
            return 0
        else:
            return z
    else:
        return mod_mult(a,fast_pow_mod(a,b-1,m),m)

def isPrime(m,count):
    for x in range(count):
        #print(x)
        a = random.randrange(1,m-1)
        if(fast_pow_mod(a,m,m) != a):
            return 0
    return 1

def findbigprimes(numbits):
    p = random.randrange(pow(2,numbits-1), pow(2,numbits)-1)
    while isPrime(p,10) ==0:
        #randomly generates a new number until p is prime
        p = random.randrange(pow(2,numbits-1), pow(2,numbits)-1)

    q = random.randrange(pow(2,numbits-1), pow(2,numbits)-1)
    while isPrime(q,10) ==0:
        #randomly generates a new number until q is prime
        q = random.randrange(pow(2,numbits-1), pow(2,numbits)-1)
    return p,q

def generateexponents(phi):
    e = random.randrange(pow(2,299),pow(2,300)-1)
    gcd,x,y = xgcd(phi,e)
    while gcd != 1:
        e = random.randrange(pow(2,299),pow(2,300)-1)
        gcd,x,y = xgcd(phi,e)
    return e,y


def main():

    if len(sys.argv) != 3:
        print("Correct usage: script, bit-length,password")
        exit()

    bit_length = int(sys.argv[1])
    #print(f"Chosen prime bit length: {bit_length}")

    password = str(sys.argv[2])
    #print(f"Chosen password: {password}")
    
    #setting up rsa to share private aes key
    p,q = findbigprimes(bit_length)
    n= p*q
    phi = (p-1)*(q-1)
    e,d = generateexponents(phi)
    d =d %phi

    characters = [ord(c) for c in password] #converting password into list of ascii values
    #print(characters)

    enc_chars = []

    for c in characters:
        new_c = fast_pow_mod(c,d,n)
        enc_chars.append(new_c)

    #print(enc_chars)
    enc_chars = str(enc_chars)


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host,port))

    data_encrypter = aes.DataEncrypter(aes.Pbkdf2Sha512Default)
    #data_decrypter = aes.DataDecrypter()


    while True:
        message = input("Enter your message: ")
        data_encrypter.Encrypt(message,password)
        enc_data = data_encrypter.GetEncryptedData()
        client_socket.sendall(enc_data)
        data = client_socket.recv(1024)
        response = data.decode('utf-8')
        print(f"Server response: {response}")

if __name__ == "__main__":
    main()
