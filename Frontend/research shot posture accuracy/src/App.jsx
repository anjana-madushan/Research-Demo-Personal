import { BrowserRouter, Routes, Route } from 'react-router-dom';
import VideoUpload from './components/Video/videoUpload';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<VideoUpload />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
