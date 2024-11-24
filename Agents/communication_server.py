import socket
import json
import threading
import logging

# Configurar el sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clase que manejará la comunicación mediante sockets
class CommunicationServer:
    def _init_(self, host="127.0.0.1", port=5005):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}
        self.running = False

    def start_server(self):
        # Iniciar el servidor de comunicación
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.running = True
        logging.info(f"Communication Server running on {self.host}:{self.port}...")

        # Iniciar el hilo para aceptar conexiones entrantes
        threading.Thread(target=self.accept_clients).start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, client_address = self.server.accept()
                logging.info(f"New connection from {client_address}")
                # Crear un hilo por cada cliente conectado
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except Exception as e:
                logging.error(f"Error accepting client: {e}")

    def handle_client(self, client_socket):
        while self.running:
            try:
                # Recibir mensajes de los clientes
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    sender = message.get("sender")
                    logging.info(f"Received message from {sender}: {message}")

                    # Procesar el mensaje y enviar respuesta si es necesario
                    response = self.process_message(message)
                    if response:
                        logging.info(f"Sending response to {sender}: {response}")
                        client_socket.send(json.dumps(response).encode('utf-8'))
                        logging.info(f"Response sent to {sender}: {response}")
            except (ConnectionResetError, json.JSONDecodeError) as e:
                logging.error(f"Error handling client message: {e}")
                break

        client_socket.close()
        logging.info("Client disconnected.")

    def process_message(self, message):
        # Procesar el mensaje recibido (lógica básica para demo)
        event_type = message.get("event_type")

        if event_type == "movement_detected":
            # Ejemplo de manejo de evento de detección de movimiento
            coordinates = message.get("coordinates", {})
            probability = message.get("probability", 0)
            logging.info(f"Processing event: Movement detected at {coordinates} with probability {probability}")

            # Responder con una acción simple (se puede expandir)
            if probability >= 0.7:
                logging.info(f"Event at {coordinates} has a high probability ({probability}). Responding with 'Investigate'.")
                return {"response": "Investigate", "coordinates": coordinates}
            else:
                logging.info(f"Event at {coordinates} has a low probability ({probability}). Responding with 'Ignore'.")
                return {"response": "Ignore"}

        return None

    def stop_server(self):
        self.running = False
        self.server.close()
        logging.info("Communication Server stopped.")

# Ejemplo de inicio del servidor
if __name__ == "_main_":
    comm_server = CommunicationServer()
    comm_server.start_server()


