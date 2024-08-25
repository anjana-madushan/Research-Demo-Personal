import { useState, useRef } from "react";
import { Button, Typography, Box, CircularProgress, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import { ShotClassification } from "../Outputs/shotClassification";
import axios from "axios";
import { styled } from "@mui/material";

const UploadButton = styled(Button)({
  marginRight: "8px",
});

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [fileName, setFileName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [batsmanType, setBatsmanType] = useState(''); // New state for batsman type
  const videoRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setFileName(selectedFile ? selectedFile.name : '');

    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  };

  const handleBatsmanTypeChange = (event) => {
    setBatsmanType(event.target.value);
  };

  const captureFrame = async () => {
    if (!videoRef.current) return;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const frameDataUrl = canvas.toDataURL('image/png');

    const blob = await fetch(frameDataUrl).then((res) => res.blob());

    const formData = new FormData();
    formData.append("image", blob, "frame.png");
    formData.append("batsmanType", batsmanType); // Append batsman type to the form data

    try {
      const response = await axios.post(
        "http://localhost:8070/api/upload/image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      const predictedLabel = response.data.data.predicted_labels['Performed shot is'];
      setMessage(predictedLabel);
      console.log(response.data);
      console.log(response)
    } catch (error) {
      console.log(error);
    }
  };

  const handleVideoLoadedMetadata = () => {
    if (videoRef.current) {
      videoRef.current.play();
      videoRef.current.playbackRate = 0.25;
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 2,
      }}
    >
      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        id="contained-button-file"
        style={{ display: "none" }}
      />
      {!file && (
        <label htmlFor="contained-button-file">
          <UploadButton variant="contained" component="span">
            Choose Video
          </UploadButton>
        </label>
      )}
      {message && <ShotClassification message={message} />}
      {fileName && <Typography>{fileName}</Typography>}
      <Box sx={{ position: 'relative', maxWidth: 700 }}>
        {isLoading ? (
          <Box
            sx={{
              position: 'absolute',
              top: -2,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              backgroundColor: 'rgba(255, 255, 255, 0.5)',
              zIndex: 9999,
            }}
          >
            <CircularProgress />
          </Box>
        ) : null}
        {file && (
          <video
            ref={videoRef}
            src={URL.createObjectURL(file)}
            controls={false}
            autoPlay
            muted
            width="100%"
            onLoadedMetadata={handleVideoLoadedMetadata}
            style={{ visibility: isLoading ? 'hidden' : 'visible' }} // Hide video while loading
          />
        )}
        {file && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              marginTop: 1,
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Button
              onClick={() => {
                if (!videoRef.current.paused) {
                  videoRef.current.pause();
                } else {
                  videoRef.current.play();
                }
              }}
              style={{ backgroundColor: "transparent", cursor: "pointer" }}
            >
              {videoRef.current && !videoRef.current.paused ? (
                <PauseIcon />
              ) : (
                <PlayArrowIcon />
              )}
            </Button>
            <Button
              variant="contained"
              onClick={captureFrame}
              sx={{ marginTop: 1 }}
            >
              Select Frame
            </Button>
            {/* Dropdown menu for selecting batsman type */}
            <FormControl variant="outlined" sx={{ marginTop: 2, minWidth: 120 }}>
              <InputLabel id="batsman-type-label">Batsman Type</InputLabel>
              <Select
                labelId="batsman-type-label"
                value={batsmanType}
                onChange={handleBatsmanTypeChange}
                label="Batsman Type"
              >
                <MenuItem value="Right-Handed">Right-Handed</MenuItem>
                <MenuItem value="Left-Handed">Left-Handed</MenuItem>
              </Select>
            </FormControl>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default VideoUpload;
