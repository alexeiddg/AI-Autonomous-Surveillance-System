from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
import torch
import io

app = Flask(__name__)

# Load pre-trained YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Small model (fast)

# Dictionary to store frames and alerts per camera
camera_frames = {}
alerts = {}

@app.route('/stream/<camera_id>', methods=['POST'])
def stream(camera_id):
    """
    Receives frames from cameras, processes them with YOLO, and generates alerts.
    """
    global camera_frames, alerts
    try:
        # Read the frame bytes from the request
        image_bytes = request.data
        if not image_bytes:
            return "No image received", 400

        # Convert bytes to an image (NumPy array)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        frame = np.array(image)

        # Resize to 640x640 pixels if needed
        frame = cv2.resize(frame, (640, 640))

        # Detect objects using YOLO
        results = model(frame)

        # Log all detections
        print("Complete detections:")
        print(results.pandas().xyxy[0])  # Display all detections

        # Filter relevant detections
        detections = results.pandas().xyxy[0]  # DataFrame with detections
        anomalies = []

        for _, row in detections.iterrows():
            # Detect "person", "dog", and now "bear" as anomalies
            if row['name'] in ['person', 'dog', 'bear'] and row['confidence'] > 0.2:
                anomalies.append({
                    "class": row['name'],
                    "confidence": row['confidence'],
                    "bbox": [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
                })

        # Update data per camera
        camera_frames[camera_id] = frame
        alerts[camera_id] = anomalies if anomalies else None

        return jsonify({"anomalies": anomalies}), 200
    except Exception as e:
        return f"Error processing the image: {e}", 500


@app.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Returns active alerts for all cameras.
    """
    global alerts
    return jsonify(alerts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
