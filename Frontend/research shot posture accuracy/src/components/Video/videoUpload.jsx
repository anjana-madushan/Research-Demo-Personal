import { useState, useRef } from "react";
import {
  Button,
  Typography,
  Box,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardMedia,
  CardContent,
  ButtonGroup
} from "@mui/material";
import axios from "axios";

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [fileName, setFileName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [batsmanType, setBatsmanType] = useState('');
  const [accuracy, setAccuracy] = useState(null);
  const [isVideoLoaded, setIsVideoLoaded] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(0.25);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleFileUploadChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setIsLoading(true);
      setIsVideoLoaded(false);

      if (videoRef.current) {
        const videoUrl = URL.createObjectURL(selectedFile);
        videoRef.current.src = videoUrl;
        videoRef.current.playbackRate = 0.25;
        videoRef.current.muted = true;
        videoRef.current.load();
      }
    }
  };

  const handleFileUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handlePlaybackSpeedChange = (event) => {
    const speed = event.target.value;
    setPlaybackSpeed(speed);
    if (videoRef.current) {
      videoRef.current.playbackRate = speed;
    }
  };

  const handleBatsmanTypeChange = (event) => {
    setBatsmanType(event.target.value);
  };

  const captureFrame = async () => {
    if (!videoRef.current || !isVideoLoaded) return;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const frameDataUrl = canvas.toDataURL('image/png');

    const blob = await fetch(frameDataUrl).then((res) => res.blob());

    const formData = new FormData();
    formData.append("image", blob, "frame.png");
    formData.append("type", batsmanType);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/upload/image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const batting_stroke = response.data['Stroke'];
      const accuracy_level = parseInt(response.data['accuracy'], 10);
      setMessage(batting_stroke);
      setAccuracy(accuracy_level);
    } catch (error) {
      console.log(error);
    }
  };

  const handleVideoLoadedMetadata = () => {
    setIsLoading(false);
    setIsVideoLoaded(true);
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" padding={4}>
      <Card sx={{ maxWidth: 600, boxShadow: 3, marginBottom: 3 }}>
        <CardMedia
          component="video"
          controls
          ref={videoRef}
          onLoadedMetadata={handleVideoLoadedMetadata}
          sx={{ height: 350 }}
          muted
          controlsList="nodownload noplaybackrate"
          disablePictureInPicture
        >
          {file && (
            <source
              src={URL.createObjectURL(file)}
              type={file.type}
            />
          )}
        </CardMedia>
        <CardContent>
          <input
            type="file"
            accept="video/mp4, video/quicktime"
            onChange={handleFileUploadChange}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          <Box sx={{ marginTop: 2, marginBottom: 2 }}>
            <Typography variant="overline" sx={{ marginBottom: 0.5 }}>Playback Speed</Typography>
            <ButtonGroup sx={{ gap: 5, display: 'flex', justifyContent: 'center' }} disabled={!isVideoLoaded}>
              <Button onClick={() => handlePlaybackSpeedChange({ target: { value: 0.25 } })}
                variant={playbackSpeed === 0.25 ? 'contained' : 'text'}>0.25x</Button>
              <Button onClick={() => handlePlaybackSpeedChange({ target: { value: 0.5 } })}
                variant={playbackSpeed === 0.50 ? 'contained' : 'text'}>0.50x</Button>
              <Button onClick={() => handlePlaybackSpeedChange({ target: { value: 0.75 } })}
                variant={playbackSpeed === 0.75 ? 'contained' : 'text'}>0.75x</Button>
              <Button onClick={() => handlePlaybackSpeedChange({ target: { value: 1.0 } })}
                variant={playbackSpeed === 1.0 ? 'contained' : 'text'}>1x</Button>
            </ButtonGroup>
          </Box>
          <Button
            variant="contained"
            fullWidth
            onClick={handleFileUploadClick}
            sx={{ marginBottom: 2, background: 'linear-gradient(90deg, #8e44ad, #c0392b)' }}
          >
            Upload Video
          </Button>

          {fileName && <Typography variant="body1">{fileName}</Typography>}
          {message && <Typography variant="h6" color="primary">{message}</Typography>}

          {accuracy !== null && (
            <Box position="relative" display="inline-flex" sx={{ marginY: 2 }}>
              <CircularProgress size={60} variant="determinate" value={accuracy} />
              <Box
                top={0}
                left={0}
                bottom={0}
                right={0}
                position="absolute"
                display="flex"
                alignItems="center"
                justifyContent="center"
              >
                <Typography variant="caption" component="div" color="textSecondary">
                  {`${accuracy}%`}
                </Typography>
              </Box>
            </Box>
          )}

          <Button
            variant="contained"
            fullWidth
            onClick={captureFrame}
            disabled={!isVideoLoaded}
            sx={{ marginBottom: 2 }}
          >
            Select Frame
          </Button>

          <FormControl fullWidth disabled={!isVideoLoaded}>
            <InputLabel>Batsman Type</InputLabel>
            <Select
              value={batsmanType}
              onChange={handleBatsmanTypeChange}
              label="Batsman Type"
            >
              <MenuItem value="right-hand">Right-Handed</MenuItem>
              <MenuItem value="left-hand">Left-Handed</MenuItem>
            </Select>
          </FormControl>
        </CardContent>
      </Card>
    </Box>
  );
};

export default VideoUpload;
