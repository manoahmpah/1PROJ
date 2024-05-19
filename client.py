import socket
import threading


def connect_to_server(server_address, server_port):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((server_address, server_port))
	return client_socket


def handle_server_receive(client_socket):
	while True:
		try:
			response = client_socket.recv(1024)
			if response.decode() == "exit":
				print("Le serveur a fermé la connexion.")
				break
			print("\n Réponse du serveur:", response.decode())
		except:
			print("Erreur de réception.")
			break


def handle_server_send(client_socket):
	while True:
		try:
			message = input("\n Entrez un message à envoyer au serveur: ")
			client_socket.sendall(message.encode())
			if message == "exit":
				break
		except:
			print("Erreur d'envoi.")
			break


def main():
	client_socket = connect_to_server('127.0.0.1', 12345)

	receive_thread = threading.Thread(target=handle_server_receive, args=(client_socket,))
	send_thread = threading.Thread(target=handle_server_send, args=(client_socket,))

	receive_thread.start()
	send_thread.start()

	receive_thread.join()
	send_thread.join()

	client_socket.close()
	print("Connexion fermée")


if __name__ == "__main__":
	main()
