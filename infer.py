import sys
import json
from ultralytics import YOLO

# Load YOLOv11 model once
model_path = "best.pt"  # adjust path if needed
model = YOLO(model_path)

def analyze_image(image_path):
    # Run inference
    results = model(image_path)

    # Extract detected class IDs
    class_ids = results[0].boxes.cls.tolist()
    names = results[0].names

    # Map class IDs to label names (e.g., "0".."9")
    digits = [names[int(cls_id)] for cls_id in class_ids]

    # Join all digits to form the recognized number
    reading = "".join(digits)

    # Return as JSON
    return {"reading": reading}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    image_path = sys.argv[1]
    output = analyze_image(image_path)
    print(json.dumps(output))
