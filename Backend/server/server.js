// Import dependencies
import bodyParser from "body-parser";
import cors from "cors";
import express from "express";

import env from './config.js';
import exampleRouter from "./controller/posture_accuracy.js";

// Using dependencies
export const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/api', exampleRouter);

// Declare port
const PORT = env.port || 8070;

app.get("/", (req, res) => {
  res.send("Hello from express");
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is up and running on Port: ${PORT}`);
});
