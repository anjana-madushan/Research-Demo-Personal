import { useState } from 'react';
import axios from 'axios';

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      setMessage('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log(formData);
      const response = await axios.post('http://localhost:8070/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setMessage(response.data);
    } catch (error) {
      setMessage('Error uploading file.');
    }
  };

  return (
    <div>
      <h2>Upload Video</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default VideoUpload;
