import { useState, useRef } from "react";
import {
  Button,
  Typography,
  Box,
  FormLabel,
  FormControlLabel,
  RadioGroup,
  Radio,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardMedia,
  CardContent,
  ButtonGroup,
  Grid
} from "@mui/material";
import axios from "axios";
import Rectifications from "../ui/rectifications";

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [fileName, setFileName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [batsmanType, setBatsmanType] = useState(null);
  const [accuracy, setAccuracy] = useState(null);
  const [isVideoLoaded, setIsVideoLoaded] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(0.25);
  const [rectifications, setRectifications] = useState([]);
  const [hasClassification, setHasClassification] = useState(false);
  const [battingStroke, setBattingStroke] = useState(null);
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

  const handleBattingStrokeChange = (event) => {
    setBattingStroke(event.target.value);
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
    formData.append("classify", hasClassification);
    formData.append("stroke", battingStroke);

    console.log(battingStroke, hasClassification)

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
      console.log(response.data)
      const batting_stroke = response.data['Stroke'];
      const accuracy_level = parseInt(response.data['accuracy'], 10);
      const rectifications = response.data['rectifications'];
      setMessage(batting_stroke);
      setAccuracy(accuracy_level);
      setRectifications(rectifications)
    } catch (error) {
      console.log(error);
    }
  };

  const handleVideoLoadedMetadata = () => {
    setIsLoading(false);
    setIsVideoLoaded(true);
  };

  return (
    <Grid container justifyContent="center" alignItems="flex-start">
      < Grid item xs={12} md={8} >
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
              autoPlay
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
              <Button
                variant="contained"
                fullWidth
                onClick={handleFileUploadClick}
                sx={{ marginBottom: 1, background: 'linear-gradient(90deg, #8e44ad, #c0392b)' }}
              >
                Upload Video
              </Button>
              <Box sx={{ marginBottom: 1 }}>
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
              {fileName && <Typography variant="body1">{fileName}</Typography>}
              <FormControl disabled={!isVideoLoaded}>
                <FormLabel id="demo-row-radio-buttons-group-label">Classification Needed</FormLabel>
                <RadioGroup
                  row
                  aria-labelledby="demo-row-radio-buttons-group-label"
                  name="row-radio-buttons-group"
                  value={hasClassification ? "yes" : "no"}
                  onChange={(event) => setHasClassification(event.target.value === "yes")}
                >
                  <FormControlLabel value="yes" control={<Radio />} label="Yes" />
                  <FormControlLabel value="no" control={<Radio />} label="No" />
                </RadioGroup>
              </FormControl>
              <Grid container spacing={2} alignItems="center" sx={{ marginBottom: 1.0 }}>
                <Grid item xs={12} md={6}>
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
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth disabled={hasClassification || !isVideoLoaded}>
                    <InputLabel>Batting Stroke</InputLabel>
                    <Select
                      value={battingStroke}
                      onChange={handleBattingStrokeChange}
                      label="Batting Stroke"
                    >
                      <MenuItem value="forward defence">Forward Defence</MenuItem>
                      <MenuItem value="forward drive">Forward Drive</MenuItem>
                      <MenuItem value="backfoot defence">Backfoot Defence</MenuItem>
                      <MenuItem value="backfoot drive">Backfoot Drive</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
              <Button
                variant="contained"
                fullWidth
                onClick={captureFrame}
                disabled={!isVideoLoaded ||
                  batsmanType === null ||
                  (!hasClassification && battingStroke === null)}
                sx={{ marginBottom: 2 }}
              >
                Select Frame
              </Button>
            </CardContent>
          </Card>
        </Box>
      </Grid >
      {accuracy && <Grid item xs={12} md={4}>
        <Rectifications rectifications={rectifications} stroke={message} accuracy={accuracy} />
      </Grid>}
    </Grid >
  );
};

export default VideoUpload;
