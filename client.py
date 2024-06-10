import socket
import threading

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = self.connect_to_server()
        self.running = True

    def connect_to_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_address, self.server_port))
        print("Connected to server at", self.server_address, "on port", self.server_port)
        return client_socket

    def handle_server_receive(self):
        while self.running:
            try:
                response = self.client_socket.recv(1024)
                if not response or response.decode() == "exit":
                    print("Le serveur a fermé la connexion.")
                    self.running = False
                    break
                print("\nRéponse du serveur:", response.decode())
            except Exception as e:
                print("Erreur de réception:", e)
                self.running = False
                break

    def handle_server_send(self):
        while self.running:
            try:
                message = input("\nEntrez un message à envoyer au serveur: ")
                self.client_socket.sendall(message.encode())
                if message == "exit":
                    self.running = False
                    break
            except Exception as e:
                print("Erreur d'envoi:", e)
                self.running = False
                break

    def run(self):
        receive_thread = threading.Thread(target=self.handle_server_receive)
        send_thread = threading.Thread(target=self.handle_server_send)

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

        self.client_socket.close()
        print("Connexion fermée")

if __name__ == "__main__":
    client = Client('127.0.0.1', 12345)
    client.run()
