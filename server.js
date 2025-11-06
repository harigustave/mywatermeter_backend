import express from "express";
import multer from "multer";
import { spawn } from "child_process";
import fs from "fs";

import { execSync } from "node:child_process"; //ES module import

// Log Python packages
console.log(execSync("python -m pip list").toString());

const app = express();
const upload = multer({ dest: "uploads/" });

// Use absolute Python path
// const PYTHON_PATH = "C:\\Users\\gharintwari\\AppData\\Local\\Programs\\Python\\Python312\\python.exe";

// app.post("/analyze", (req, res) => {
//   const py = spawn(PYTHON_PATH, ["testcodes.py"]);
// Accept image uploads
app.post("/analyze", upload.single("image"), (req, res) => {

  const PYTHON_PATH = "python";

  const imagePath = req.file.path;

  const py = spawn(PYTHON_PATH, ["testcodes.py", imagePath]);
  let data = "";
  py.stdout.on("data", (chunk) => (data += chunk));
  py.stderr.on("data", (err) => console.error("Python error:", err.toString()));

  py.on("close", (code) => {
    try {
      const parsed = JSON.parse(data);
      res.json({
        success: true,
        meterReading: parsed.reading
      });
    } catch (err) {
      res.status(500).json({ success: false, error: err.message });
    }
  });
});

app.listen(10000, () => console.log("Server running on port 10000"));