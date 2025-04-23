import socket
import sys
import aes_cipher as aes
import rsa
sys.setrecursionlimit(100000)

def main():

    if len(sys.argv) != 3:
        print("Correct usage: script, bit-length,password")
        exit()

    bit_length = int(sys.argv[1])
    #print(f"Chosen prime bit length: {bit_length}")

    password = str(sys.argv[2])
    #print(f"Chosen password: {password}")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host,port))

    data_encrypter = aes.DataEncrypter(aes.Pbkdf2Sha512Default)
    #data_decrypter = aes.DataDecrypter()

    message = str(bit_length)
    data_encrypter.Encrypt(message,password)
    enc_data = data_encrypter.GetEncryptedData()
    client_socket.sendall(enc_data)
    data = client_socket.recv(1024)
    response = data.decode('utf-8')
    pubkeys = eval(response)
    print(f"Server response: {response}")
    ciphertext = rsa.rsa_encrypt(password,pubkeys)
    print(ciphertext)
    data_encrypter.Encrypt(str(ciphertext),password)
    enc_data = data_encrypter.GetEncryptedData()
    client_socket.sendall(enc_data)

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
