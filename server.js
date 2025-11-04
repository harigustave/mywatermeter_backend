import express from "express";
import multer from "multer";
import { spawn } from "child_process";
import fs from "fs";

const app = express();
const upload = multer({ dest: "uploads/" });

app.post("/analyze", upload.single("image"), (req, res) => {
  const { meterId, meterOwner, timestamp} = req.body;
  const imagePath = req.file.path;

  const py = spawn("python3", ["infer.py", imagePath]);

  let data = "";
  py.stdout.on("data", (chunk) => (data += chunk));
  py.stderr.on("data", (err) => console.error("Python error:", err.toString()));

  py.on("close", (code) => {
    fs.unlinkSync(imagePath); // remove temp file
    try {
      const parsed = JSON.parse(data);
      res.json({
        success: true,
        MeterNumber: meterId,
        MeterOwner: meterOwner,
        RecordDate: timestamp,
        meterReading: parsed.reading,
      });
    } catch (err) {
      res.status(500).json({ success: false, error: err.message });
    }
  });
});

app.listen(10000, () => console.log("Server running on port 10000"));
