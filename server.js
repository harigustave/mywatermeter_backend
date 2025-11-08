import express from "express";
import multer from "multer";
import fs from "fs";
import cors from "cors";
import { Client } from "@gradio/client";

const app = express();
app.use(cors());
const upload = multer({ dest: "uploads/" });

// Gradio public Space name
const SPACE_NAME = "higustave/watermeterapp";

// ---------------------------------
// Predict Endpoint
// ---------------------------------
app.post("/predict", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No image uploaded" });

    const imageBytes = fs.readFileSync(req.file.path);
    console.log("Sending image to Gradio Space...");

    // Connect to your public Hugging Face Space
    const client = await Client.connect(SPACE_NAME);

    // Send prediction request
    const result = await client.predict("/predict", {
      image: imageBytes,
    });

    console.log("Gradio result:", result);

    // Clean up temp file
    fs.unlinkSync(req.file.path);

    // Safely extract prediction
    let prediction = "No prediction returned";
    if (result?.data && result.data.length > 0) {
      prediction = result.data[0];
    } else if (Array.isArray(result) && result.length > 0) {
      prediction = result[0];
    }

    res.json({ success: true, prediction });
  } catch (error) {
    console.error("Prediction error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// ---------------------------------
// Health Check
// ---------------------------------
app.get("/", (req, res) => {
  res.send("WaterMeter Backend Running Successfully with Public Gradio Space");
});

// ---------------------------------
// Start Server
// ---------------------------------
const PORT = process.env.PORT || 9000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
