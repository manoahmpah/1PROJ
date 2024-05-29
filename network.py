import socket
import threading

class Network:
    def __init__(self, server_port):
        self.server_port = server_port
        self.server_socket = self.create_server()
        self.running = True

    def create_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.server_port))
        server_socket.listen(5)  # Allow up to 5 pending connections
        print("Server listening on port", self.server_port)
        return server_socket

    def handle_client(self, client_socket, client_address):
        print("Accepted connection from", client_address)
        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=self.send_messages, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

        client_socket.close()
        print("Connection with", client_address, "closed")

    def receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if not message or message.decode() == "exit":
                    print("Client closed the connection.")
                    break
                print("\n[RECEIVED]", message.decode())
                print("[SEND]", end="")
            except Exception as e:
                print("Receive error:", e)
                break

    def send_messages(self, client_socket):
        while True:
            try:
                response = input("\nEnter a response to send to the client: ")
                client_socket.sendall(response.encode())
                if response == "exit":
                    break
            except Exception as e:
                print("Send error:", e)
                break

    def run(self):
        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_handler.start()
        except KeyboardInterrupt:
            print("Server is shutting down.")
            self.running = False
        finally:
            self.server_socket.close()
            print("Server socket closed.")


if __name__ == "__main__":
    network = Network(12345)
    network.run()
