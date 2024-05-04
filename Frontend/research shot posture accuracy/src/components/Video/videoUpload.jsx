import { useState, useRef, useEffect } from "react";
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
  const [durationExceeded, setDurationExceeded] = useState(false);
  // const [frames, setFrames] = useState([]);
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play();
      videoRef.current.playbackRate = 0.5;
    }
  }, [videoRef]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
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
        setDurationExceeded(true);
      } else {
        setDurationExceeded(false);
      }

      // Release the object URL
      URL.revokeObjectURL(fileURL);

      // Extract frames from the video
      // extractFrames(videoElement);
    };
  };

  const handleOptionChange = (event) => {
    setBatsmanType(event.target.value);
  };

  // const extractFrames = (video) => {
  //   const frameRate = 30; // Adjust as needed
  //   const numFrames = Math.floor(video.duration * frameRate);

  //   const canvas = document.createElement('canvas');
  //   const context = canvas.getContext('2d');

  //   const extractedFrames = [];
  //   for (let i = 0; i < numFrames; i++) {
  //     video.currentTime = i / frameRate;
  //     video.pause(); // Pause the video to ensure accurate frame extraction
  //     canvas.width = video.videoWidth;
  //     canvas.height = video.videoHeight;
  //     context.drawImage(video, 0, 0, canvas.width, canvas.height);
  //     const frameDataUrl = canvas.toDataURL('image/png');
  //     extractedFrames.push(frameDataUrl);
  //   }
  //   setFrames(extractedFrames);
  // };

  const captureFrame = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const frameDataUrl = canvas.toDataURL('image/png');
    // Send the frameDataUrl to the backend
    console.log("Frame captured:", frameDataUrl);
    const blob = await fetch(frameDataUrl).then((res) => res.blob());

    // Create a FormData object
    const formData = new FormData();
    formData.append("image", blob, "frame.png");
    console.log(formData);
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
      setMessage(response.data);
    } catch (error) {
      console.log(error)
      setMessage("Error uploading file.");
    }
  };

  // const handleSelectFrame = (frameIndex) => {
  //   const selectedFrame = frames[frameIndex];
  //   // Send the selectedFrame to the backend
  //   console.log("Selected frame:", selectedFrame);
  //   // Here you can make an axios request to send the selectedFrame to the backend
  // };

  // const handleSubmit = async () => {
  //   if (!file) {
  //     setMessage("Please select a file.");
  //     return;
  //   }

  //   if (batsmanType === '') {
  //     setMessage('Please select the batsman type');
  //     return;
  //   }

  //   if (durationExceeded) {
  //     setMessage('Duration of the video is higher');
  //     return;
  //   }

  //   const formData = new FormData();
  //   formData.append("file", file);

  //   try {
  //     const response = await axios.post(
  //       "http://localhost:8070/api/upload/",
  //       formData,
  //       {
  //         headers: {
  //           "Content-Type": "multipart/form-data",
  //         },
  //       }
  //     );
  //     setMessage(response.data);
  //   } catch (error) {
  //     setMessage("Error uploading file.");
  //   }
  // };

  return (
    <>
      <Box
        sx={{
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
        {videoDuration && <Typography>Video Duration: {videoDuration} seconds</Typography>}
        {durationExceeded && <Typography>Duration of the video exceeds 10 seconds.</Typography>}
        {/* <UploadButton variant="contained" onClick={handleSubmit}>
          Upload
        </UploadButton> */}
        {message && <Typography>{message}</Typography>}
        {/* Display video element */}
        {file && <video ref={videoRef} src={URL.createObjectURL(file)} controls autoPlay width="400" height="300" />}
        {/* Button to capture frame */}
        <Button variant="contained" onClick={captureFrame}>Capture Frame</Button>
        {/* Display extracted frames */}
        {/* {frames.length > 0 && (
          <div>
            {frames.map((frame, index) => (
              <div key={index}>
                <img src={frame} alt={`Frame ${index}`} />
                <Button variant="contained" onClick={() => handleSelectFrame(index)}>Select Frame</Button>
              </div>
            ))}
          </div>
        )} */}
      </Box>
    </>
  );
};

export default VideoUpload;
