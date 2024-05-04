import { useState } from "react";
import { Button, Typography, Radio, FormControlLabel, Box } from "@mui/material";
import axios from "axios";
import { styled } from "@mui/material";

const UploadButton = styled(Button)({
  marginRight: "8px",
});

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [batsmanType, setBatsmanType] = useState('');
  const [fileName, setFileName] = useState('');
  const [videoDuration, setVideoDuration] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    console.log(selectedFile);
    setFileName(selectedFile ? selectedFile.name : '');
    // Create a URL for the selected file
    const fileURL = URL.createObjectURL(selectedFile);

    // Create a new video element
    const videoElement = document.createElement('video');

    // Set the src of the video element to the file URL
    videoElement.src = fileURL;

    // When metadata has been loaded
    videoElement.onloadedmetadata = () => {
      // Set the video duration in seconds
      const durationInSeconds = Math.round(videoElement.duration);
      setVideoDuration(durationInSeconds);

      // Check if duration exceeds 10 seconds
      if (durationInSeconds > 10) {
        setMessage('Duration of the video is higher than 10 seconds.');
      } else {
        setMessage('');
      }

      // Release the object URL
      URL.revokeObjectURL(fileURL);
    };
  };

  const handleOptionChange = (event) => {
    setBatsmanType(event.target.value);
  };

  const handleSubmit = async () => {
    if (!file) {
      setMessage("Please select a file.");
      return;
    }

    if (batsmanType === '') {
      setMessage('Please select the batsman type');
      return;
    }

    // Check if duration exceeds 10 seconds
    if (videoDuration && videoDuration > 10) {
      setMessage('Duration of the video is higher than 10 seconds.');
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8070/api/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setMessage(response.data);
    } catch (error) {
      setMessage("Error uploading file.");
    }
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          mt: 20,
          height: "100vh",
          overflowY: "hidden", // Remove vertical scroll bar
        }}
      >
        <Typography variant="h2">Upload Video</Typography>
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          id="contained-button-file"
          style={{ display: "none" }}
        />
        <label htmlFor="contained-button-file">
          <UploadButton variant="contained" component="span">
            Choose File
          </UploadButton>
        </label>
        {fileName && <Typography>{fileName}</Typography>}
        <Box>
          <FormControlLabel
            value="left_handed"
            control={<Radio />}
            label="Left Handed"
            checked={batsmanType === "left_handed"}
            onChange={handleOptionChange}
          />
          <FormControlLabel
            value="right_handed"
            control={<Radio />}
            label="Right Handed"
            checked={batsmanType === "right_handed"}
            onChange={handleOptionChange}
          />
        </Box>
        <UploadButton variant="contained" onClick={handleSubmit}>
          Upload
        </UploadButton>
        {message && <Typography>{message}</Typography>}
      </Box>
    </>
  );
};

export default VideoUpload;
