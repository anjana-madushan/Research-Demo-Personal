import multer from 'multer';
import { Router } from "express";
import axios from 'axios';
import FormData from 'form-data';
import fs from 'fs';
const router = Router();

// Set up multer storage for uploaded images
const imageStorage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/frames/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const imageUpload = multer({ storage: imageStorage }).single('image');

//image upload router
router.post('/upload/image', (req, res) => {
  imageUpload(req, res, async (err) => {
    try {
      if (err instanceof multer.MulterError) {
        return res.status(400).send('Error uploading image.');
      } else if (err) {
        return res.status(500).send('Error uploading image.');
      }

      // Read the uploaded image file
      const imageBuffer = fs.readFileSync(req.file.path);

      // Created a FormData object
      const formData = new FormData();
      formData.append('image', imageBuffer, { filename: req.file.originalname });

      // POST request to Flask endpoint
      const pythonServerUrl = 'http://127.0.0.1:5000';
      const response = await axios.post(`${pythonServerUrl}/process_image`, formData, {
        headers: {
          ...formData.getHeaders(), // Include form data headers
        },
      });

      console.log('Python server response:', response.data);
      return res.status(200).json({ message: 'Image processing and angle detection completed', data: response.data });
    } catch (error) {
      console.log('Error uploading image:', error);
      return res.status(500).send('Error uploading image.');
    }
  });
});

export default router;

// Set up multer storage for uploaded files
// const storage = multer.diskStorage({
//   destination: function (req, file, cb) {
//     cb(null, 'uploads/')
//   },
//   filename: function (req, file, cb) {
//     cb(null, file.originalname)
//     console.log(console.log(file.originalname))
//   }
// });

// const upload = multer({ storage: storage });

// Define endpoint for file upload
// router.post('/upload', upload.single('file'), async (req, res) => {
//   try {
//     if (!req.file) {
//       return res.status(400).send('No file uploaded.');
//     }

//     // File uploaded successfully
//     const filePath = req.file.path;
//     console.log('File uploaded:', filePath);
//     res.send('File uploaded successfully.');

//     const pythonServerUrl = 'http://127.0.0.1:5000'; // Adjust the URL as per your setup
//     const response = await axios.post(`${pythonServerUrl}/process_video`, {
//       videoPath: filePath,
//       outputDir: 'uploads/1',
//       frameSkip: 10 // Frame skip value
//     });

//     console.log('Python server response:', response.data);
//     res.send('Video processing completed');

//   } catch (e) {
//     console.log('Error ', e)
//   }
// });