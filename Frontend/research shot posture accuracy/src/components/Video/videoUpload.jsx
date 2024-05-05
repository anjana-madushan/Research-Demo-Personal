import { useState, useRef } from "react";
import { Button, Typography, Box } from "@mui/material";
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import ShotClassification from "../Outputs/shot_classification";
import axios from "axios";
import { styled } from "@mui/material";

const UploadButton = styled(Button)({
  marginRight: "8px",
});

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [fileName, setFileName] = useState('');
  const videoRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setFileName(selectedFile ? selectedFile.name : '');
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
      console.log(response.data)
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
      <Typography variant="h3" fontWeight="bold">
        Batting Technique Checker
      </Typography>
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
      {fileName && <Typography>{fileName}</Typography>}
      <Box sx={{ position: 'relative', maxWidth: 700 }}>
        {file && (
          <video
            ref={videoRef}
            src={URL.createObjectURL(file)}
            controls={false}
            autoPlay
            muted
            width="100%"
            onLoadedMetadata={handleVideoLoadedMetadata}
          />
        )}
        {file && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              marginTop: 1,
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
              sx={{ marginLeft: 1 }}
            >
              Select Frame
            </Button>
          </Box>
        )}
        {message && <ShotClassification message={message} />}
      </Box>
    </Box>
  );
};

export default VideoUpload;
