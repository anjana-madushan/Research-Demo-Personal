import {
  Typography,
  Box,
  CircularProgress
} from "@mui/material";

// eslint-disable-next-line react/prop-types
const Rectifications = ({ rectifications, accuracy, stroke }) => {

  console.log(rectifications)

  return (
    <Box
      sx={{
        padding: 2,
        border: '1px solid #ddd',
        borderRadius: 2,
        boxShadow: 2,
        maxWidth: 400
      }}
    >
      <Typography variant="h6" gutterBottom>
        Corrections Needed
      </Typography>
      <Typography variant="h6" color="primary">{stroke}</Typography>
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
      {rectifications.map((rectification, index) => (
        <Box key={index} sx={{ marginBottom: 2 }}>
          <Typography variant="body1">
            <strong>{rectification['angle name']}</strong>
          </Typography>
          <Typography variant="body2"><strong>{`${rectification['current angle value']}°`}</strong></Typography>
          <Typography variant="body2" color="error">
            <Typography variant="body2"><strong>{rectification['error type']}</strong></Typography>
          </Typography>
          <Typography variant="body2">
            <Typography variant="body2"><strong>{rectification['general response']}</strong></Typography>
          </Typography>
          <Typography variant="body2">
            <Typography variant="body2"><strong>{rectification['mathematical response']}</strong></Typography>
          </Typography>
        </Box>
      ))}
    </Box>
  );
};

export default Rectifications