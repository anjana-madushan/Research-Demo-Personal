import multer from 'multer';
import { Router } from "express";
import axios from 'axios';
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
router.post('/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }

    // File uploaded successfully
    const filePath = req.file.path;
    console.log('File uploaded:', filePath);
    res.send('File uploaded successfully.');

    const pythonServerUrl = 'http://127.0.0.1:5000'; // Adjust the URL as per your setup
    const response = await axios.post(`${pythonServerUrl}/process_video`, {
      videoPath: filePath,
      outputDir: 'uploads/1',
      frameSkip: 10 // Frame skip value
    });

    console.log('Python server response:', response.data);
    res.send('Video processing completed');

  } catch (e) {
    console.log('Error ', e)
  }
});

export default router;