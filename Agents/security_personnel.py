import socket
import json
import logging

# Configurar el sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clase para manejar al personal de seguridad y sus funciones básicas
class SecurityPersonnel:
    def _init_(self, server_ip="127.0.0.1", server_port=5005):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.connected = False
        self.control_drone = False  # Estado de control manual del dron

    def connect_to_server(self):
        # Conectar al servidor de comunicación
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            logging.info(f"Security Personnel connected to server at {self.server_ip}:{self.server_port}")
        except Exception as e:
            logging.error(f"Failed to connect Security Personnel to server: {e}")
            self.connected = False

    def send_message(self, message):
        # Enviar un mensaje en formato JSON al servidor
        if self.connected:
            try:
                self.client_socket.send(json.dumps(message).encode('utf-8'))
            except Exception as e:
                logging.error(f"Error sending message from Security Personnel: {e}")

    def receive_message(self):
        # Recibir mensajes del servidor
        if self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    return message
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
        return None

    def evaluate_alert(self, message):
        # Evaluar la alerta recibida y decidir si tomar control del dron
        probability = message.get("probability", 0)
        coordinates = message.get("coordinates", {})

        if probability >= 0.8:
            logging.info(f"High alert detected! Probability: {probability}. Taking control of the drone.")
            self.control_drone = True
            # Enviar comando para que el dron pase a control manual
            self.send_message({
                "sender": "security_personnel",
                "event_type": "manual_control",
                "coordinates": coordinates
            })
        else:
            logging.info(f"Alert evaluated as minor. Probability: {probability}. No action taken.")

    def run(self):
        # Ciclo principal del personal de seguridad
        if not self.connected:
            self.connect_to_server()

        while self.connected:
            # Verificar si hay mensajes del servidor (alertas)
            message = self.receive_message()
            if message:
                event_type = message.get("event_type")

                if event_type == "movement_detected":
                    logging.info("Security Personnel received alert. Evaluating...")
                    self.evaluate_alert(message)

        # Cerrar conexión al terminar
        self.client_socket.close()

# Ejemplo de ejecución del personal de seguridad
if __name__ == "_main_":
    security_personnel = SecurityPersonnel()
    security_personnel.run()