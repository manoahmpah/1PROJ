import socket
import threading

def create_server(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(1)
    print("Serveur en écoute sur le port", server_port)
    client_socket, client_address = server_socket.accept()
    print("Connexion acceptée de", client_address)
    return client_socket, client_address

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message.decode() == "exit":
                print("Le client a fermé la connexion.")
                break
            print("Message reçu du client:", message.decode())
        except:
            print("Erreur de réception.")
            break

def send_messages(client_socket):
    while True:
        try:
            response = input("\n Entrez une réponse à envoyer au client: ")
            client_socket.sendall(response.encode())
            if response == "exit":
                break
        except:
            print("Erreur d'envoi.")
            break

def main():
    client_socket, client_address = create_server(12345)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()
    print("Connexion fermée")

if __name__ == "__main__":
    main()
