import { Paper, Typography, CardMedia } from '@mui/material';

export default function Banner() {
  return (
    <Paper
      sx={{
        backgroundColor: '#00000', // Background color of the banner
        padding: '10px', // Padding around the content
        textAlign: 'center', // Center align the content
      }}
    >
      <CardMedia
        component="img"
        height="450"
        image="src/assets/images/banner.jpg"
        alt="Banner Image"
        sx={{
          marginBottom: '20px', // Margin bottom to create space between image and text
        }}
      />
      <Typography variant="h3" fontWeight="bold">
        Batting Technique Checker
      </Typography>
      <Typography variant="body1" paragraph>
      </Typography>
    </Paper>


  );
}