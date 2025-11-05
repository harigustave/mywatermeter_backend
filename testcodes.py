# testcodes.py
import json
import sys
import io
import os

# Suppress YOLO's extra logs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
os.environ["YOLO_VERBOSE"] = "False"

import model  # import your existing model.py

# Get the image path from the command line argument
image_path = sys.argv[1] if len(sys.argv) > 1 else "meterimage.jpeg"

# Run your model function
try:
    result = model.testModel(image_path)
    # If your testModel() already prints "Meter Value: 12345",
    # you can modify it to *return* the value instead of print
    if result is not None:
        print(json.dumps({"reading": result}))
    else:
        print(json.dumps({"reading": None}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
