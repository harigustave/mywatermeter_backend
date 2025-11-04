# model/infer.py
import sys
import json
from ultralytics import YOLO

# Load YOLOv11 model once
model_path = "model/best.pt"
model = YOLO(model_path)

def analyze_image(image_path):
    # Directly run the model
    results = model.predict(source=image_path, imgsz=640, conf=0.25)
    
    detected_number = str(results[0].boxes.cls)  # replace with actual output from your model
    return detected_number

if __name__ == "__main__":
    image_path = sys.argv[1]
    reading = analyze_image(image_path)
    print(json.dumps({"reading": reading}))
