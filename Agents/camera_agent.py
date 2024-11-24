import socket
import json
import random
import time
import logging

# Configurar el sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clase para manejar la cámara y sus funciones básicas
class CameraAgent:
    def _init_(self, camera_id, server_ip="127.0.0.1", server_port=5005):
        self.camera_id = camera_id  # Identificador único para cada cámara
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.connected = False
        self.monitoring_active = True  # Estado de monitoreo

    def connect_to_server(self):
        # Conectar al servidor de comunicación
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            logging.info(f"Camera {self.camera_id} connected to server at {self.server_ip}:{self.server_port}")
        except Exception as e:
            logging.error(f"Failed to connect Camera {self.camera_id} to server: {e}")
            self.connected = False

    def send_message(self, message):
        # Enviar un mensaje en formato JSON al servidor
        if self.connected:
            try:
                self.client_socket.send(json.dumps(message).encode('utf-8'))
                logging.info(f"Sent message to server: {message}")
            except Exception as e:
                logging.error(f"Error sending message from Camera {self.camera_id}: {e}")

    def simulate_detection(self):
        # Simulación de detección de eventos con alta probabilidad (≥ 0.7)
        if self.monitoring_active:
            probability = round(random.uniform(0.7, 1.0), 2)  # Generar eventos con alta probabilidad
            coordinates = {"x": random.randint(0, 100), "y": random.randint(0, 100)}

            logging.info(f"Camera {self.camera_id} detected a possible event at {coordinates} with probability {probability}")

            # Enviar alerta al servidor
            self.send_message({
                "sender": f"camera_{self.camera_id}",
                "event_type": "movement_detected",
                "coordinates": coordinates,
                "probability": probability
            })

    def monitor_area(self):
        # Ciclo principal de monitoreo de la cámara
        if not self.connected:
            self.connect_to_server()

        while self.connected:
            # Simular monitoreo constante del área
            self.simulate_detection()
            time.sleep(3)  # Pausa para simular el intervalo de monitoreo

        # Cerrar conexión al terminar
        self.client_socket.close()

# Ejemplo de ejecución de la cámara
if __name__ == "_main_":
    camera = CameraAgent(camera_id=1)
    camera.monitor_area()



