import VideoUpload from "../components/Video/videoUpload";
import Banner from "../components/headers/header";
import NavBar from "../components/headers/nav_bar";

const Home = () => {
  return (
    <>
      <NavBar />
      <Banner />
      <br />
      <VideoUpload />
    </>
  )
}

export default Home