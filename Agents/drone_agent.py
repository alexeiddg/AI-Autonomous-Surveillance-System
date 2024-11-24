import socket
import json
import time
import logging

# Configurar el sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clase para manejar el dron y sus funciones básicas
class DroneAgent:
    def _init_(self, server_ip="127.0.0.1", server_port=5005):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.connected = False
        self.patrol_route = [(0, 0), (10, 10), (20, 0), (10, -10)]  # Ruta predefinida con puntos de control
        self.current_position = (0, 0)  # Posición inicial del dron
        self.patrol_index = 0  # Índice para seguir la ruta de patrullaje
        self.patrol_active = True
        self.landing_station = (0, 0)  # Estación de aterrizaje (posición inicial)

    def connect_to_server(self):
        # Conectar al servidor de comunicación
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5)  # Timeout de 5 segundos para evitar bloqueos
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            logging.info(f"Drone connected to server at {self.server_ip}:{self.server_port}")
        except Exception as e:
            logging.error(f"Failed to connect Drone to server: {e}")
            self.connected = False

    def send_message(self, message):
        # Enviar un mensaje en formato JSON al servidor
        if self.connected:
            try:
                self.client_socket.send(json.dumps(message).encode('utf-8'))
                logging.info(f"Sent message to server: {message}")
            except Exception as e:
                logging.error(f"Error sending message from Drone: {e}")

    def receive_message(self):
        # Recibir mensajes del servidor sin bloquear indefinidamente
        if self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    return message
            except socket.timeout:
                # Si el socket se bloquea por timeout, simplemente retornar None
                logging.info("No message received (timeout), continuing patrol.")
                return None
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
        return None

    def patrol(self):
        # Patrullaje básico: seguir una ruta de puntos de control
        if self.patrol_active:
            target = self.patrol_route[self.patrol_index]
            logging.info(f"Drone moving from {self.current_position} to {target}")
            self.current_position = target
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_route)

            # Enviar posición actual al servidor para registro (opcional)
            self.send_message({
                "sender": "drone",
                "event_type": "patrol_update",
                "current_position": self.current_position
            })
            logging.info(f"Drone has updated its position to {self.current_position} and sent the update.")

    def respond_to_alert(self, coordinates):
        # Responder a una alerta moviéndose a las coordenadas especificadas
        logging.info(f"Drone responding to alert at {coordinates}")
        self.current_position = coordinates

        # Enviar confirmación al servidor
        self.send_message({
            "sender": "drone",
            "event_type": "alert_responded",
            "current_position": self.current_position
        })
        logging.info(f"Drone has responded and moved to {coordinates}")

    def return_to_station(self):
        # Regresar a la estación de aterrizaje
        logging.info(f"Drone returning to landing station at {self.landing_station}")
        self.current_position = self.landing_station
        self.patrol_active = False

        # Enviar confirmación de aterrizaje al servidor
        self.send_message({
            "sender": "drone",
            "event_type": "landed",
            "current_position": self.current_position
        })
        logging.info(f"Drone has landed at {self.landing_station}")

    def run(self):
        # Ciclo principal del dron
        if not self.connected:
            self.connect_to_server()

        while self.connected:
            # Simular el patrullaje básico
            if self.patrol_active:
                self.patrol()
                time.sleep(2)  # Pausa para simular movimiento

            # Verificar si hay mensajes del servidor
            message = self.receive_message()
            if message:
                logging.info(f"Drone received message: {message}")
                event_type = message.get("response")
                coordinates = message.get("coordinates", {})

                if event_type == "Investigate":
                    self.respond_to_alert(coordinates)
                elif event_type == "Ignore":
                    logging.info("Drone received 'Ignore' command. Continuing patrol.")
                elif event_type == "Return":
                    self.return_to_station()
                    break
            else:
                logging.info("No message received from server, continuing patrol.")

        # Cerrar conexión al terminar
        self.client_socket.close()

# Ejemplo de ejecución del dron
if __name__ == "_main_":
    drone = DroneAgent()
    drone.run()
