import multer from 'multer';
import fs from 'fs';
import path from 'path';
import { Router } from "express";
const router = Router();

// Set up multer storage for uploaded files
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname)
    console.log(console.log(file.originalname))
  }
});

const upload = multer({ storage: storage });

// Define endpoint for file upload
router.post('/upload', upload.single('file'), (req, res) => {
  try {
    console.log('hello!');
    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }

    // File uploaded successfully
    const filePath = req.file.path;
    console.log('File uploaded:', filePath);
    res.send('File uploaded successfully.');
  } catch (e) {
    console.log('Error ', e)
  }
});

export default router;