import express from "express";
import multer from "multer";
import cors from "cors";
import fetch from "node-fetch";
import fs from "fs";

const app = express();
const PORT = process.env.PORT || 10000;

// Enable CORS for all routes
app.use(cors());

// Create a storage engine for multer (stores uploads temporarily)
const upload = multer({ dest: "uploads/" });

// -----------------------------
// 🔹 1. Root route
// -----------------------------
app.get("/", (req, res) => {
  res.send("✅ WaterMeter Backend is running successfully on Render!");
});

// -----------------------------
// 🔹 2. Upload & Send to Hugging Face
// -----------------------------
app.post("/predict", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No image uploaded" });
    }

    const imagePath = req.file.path;
    const imageData = fs.readFileSync(imagePath);

    // Replace this URL with your Hugging Face Space API endpoint
    const hfEndpoint = "https://harigustave-watermeterapp.hf.space/api/predict/";

    // Send image to Hugging Face API
    const response = await fetch(hfEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        data: [`data:image/jpeg;base64,${imageData.toString("base64")}`],
      }),
    });

    const result = await response.json();

    // Delete uploaded file to save space
    fs.unlinkSync(imagePath);

    // Send Hugging Face model response back to frontend
    res.json({
      success: true,
      prediction: result.data ? result.data[0] : "No result returned",
    });
  } catch (error) {
    console.error("Prediction error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// -----------------------------
// 🔹 3. Start server
// -----------------------------
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
