import socket
import threading
import aes_cipher as aes
import rsa


def handle_client(client_socket):

    messagecount =0
    data_decrypter = aes.DataDecrypter()

    if messagecount ==0:
        bitlength = client_socket.recv(1024)
        data_decrypter.Decrypt(bitlength, "test")
        length = data_decrypter.GetDecryptedData()
        #message = data.decode('utf-8')
        #print(f"Received message: {data}")
        length = length.decode('utf-8')

        pubkey, privkey = rsa.generate_rsa_keys(int(length))
        response = "Public Keys " + str(pubkey)
        client_socket.sendall(response.encode('utf-8'))
        messagecount += 1

    while True:
        #giving key for now
        data = client_socket.recv(1024)
        if not data:
            break
        data_decrypter.Decrypt(data, "test")
        message = data_decrypter.GetDecryptedData()
        #message = data.decode('utf-8')
        print(f"Received message: {data}")
        message = message.decode('utf-8')
        response = "Server Received your message " + message
        client_socket.sendall(response.encode('utf-8'))
        messagecount +=1
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = '127.0.0.1'
    port =12345
    server_socket.bind((host,port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client,args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()