
import cv2
import numpy as np
from flask import Flask, request, jsonify
import torch

app = Flask(__name__)

# Cargar modelo YOLO
model_path = "yolov5/runs/train/exp2/weights/best.pt"  # Ruta al modelo
print("Loading YOLO model...")
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)
print("YOLO model loaded successfully.")

# Función para verificar si el bbox contiene color rosa
def filter_pink(image, bbox):
    x1, y1, x2, y2 = [int(coord) for coord in bbox]
    cropped_image = image[y1:y2, x1:x2]

    # Convertir a espacio de color HSV
    hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)

    # Rango HSV para color rosa
    lower_pink = np.array([130, 40, 40])
    upper_pink = np.array([180, 255, 255])

    # Máscara para el color rosa
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    pink_pixels = cv2.countNonZero(mask)

    # Umbral mínimo para considerar el oso como rosa
    return pink_pixels > 50

@app.route("/stream/<camera_id>", methods=["POST"])
def detect(camera_id):
    try:
        # Decodificar la imagen recibida
        image_data = np.frombuffer(request.data, np.uint8)
        img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image data"}), 400

        # Guardar frames (opcional para depuración)
        cv2.imwrite(f"all_frames_{camera_id}.jpg", img)

        # Procesar con YOLO
        results = model(img)
        detections = results.xyxy[0].cpu().numpy()

        rosa_detectado = False
        oso_detectado = False
        output = []

        for *bbox, conf, cls in detections:
            es_rosa = filter_pink(img, bbox)
            if es_rosa:
                rosa_detectado = True
            if model.names[int(cls)] == "bear" and conf > 0.5:
                oso_detectado = True
                output.append({
                    "bbox": [float(coord) for coord in bbox],
                    "class": model.names[int(cls)],
                    "confidence": float(conf)
                })

        # Generar alertas
        if oso_detectado and rosa_detectado:
            print(f"🚨 ALERT: Bear detected on {camera_id}.")
        elif rosa_detectado:
            print(f"🔍 Something suspicious was detected on {camera_id}.")

        return jsonify({"camera_id": camera_id, "detections": output})
    except Exception as e:
        print(f"Error on {camera_id}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Server ready. Starting Flask...")
    app.run(host="0.0.0.0", port=8000)
