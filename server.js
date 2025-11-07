import dotenv from "dotenv";
dotenv.config();

import express from "express";
import multer from "multer";
import fetch from "node-fetch";
import cors from "cors";
import fs from "fs";

const app = express();
app.use(cors());
const upload = multer({ dest: "uploads/" });

// Correct Hugging Face Inference API endpoint
const hfUrl = "https://router.huggingface.co/hf-inference/models/harigustave/watermeterapp";

// Read token from Render environment
const HF_TOKEN = process.env.HF_TOKEN;

app.post("/predict", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No image uploaded" });
    }

    const imageBytes = fs.readFileSync(req.file.path);

    // Send image to Hugging Face Inference API
    const response = await fetch(hfUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${HF_TOKEN}`,
        "Content-Type": "application/octet-stream",
      },
      body: imageBytes,
    });

    const result = await response.json();

    // Handle potential HF errors
    if (!response.ok) {
      return res.status(response.status).json({
        success: false,
        error: result.error || "Hugging Face request failed",
      });
    }

    // Extract prediction text dynamically
    let prediction = "Unknown";
    if (Array.isArray(result) && result.length > 0) {
      prediction = result[0].generated_text || result[0].text || JSON.stringify(result[0]);
    } else if (result.generated_text) {
      prediction = result.generated_text;
    } else if (result.text) {
      prediction = result.text;
    } else if (result.data) {
      prediction = result.data[0];
    }

    // Cleanup temp file
    fs.unlinkSync(req.file.path);

    // Send response back to MAUI app
    res.json({ success: true, prediction });
  } catch (error) {
    console.error("Prediction error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Health check
app.get("/", (req, res) => {
  res.send("Water Meter Backend Running on Render");
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
