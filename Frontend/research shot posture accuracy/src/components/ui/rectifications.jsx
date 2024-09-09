import {
  Typography,
  Box,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper
} from "@mui/material";

// eslint-disable-next-line react/prop-types
const Rectifications = ({ rectifications, accuracy, stroke }) => {

  return (
    <Box
      sx={{
        padding: 2,
        border: '1px solid #ddd',
        borderRadius: 2,
        boxShadow: 2,
        width: '100%',
        boxSizing: 'border-box'
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
      <TableContainer component={Paper} sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Angle Name</strong></TableCell>
              <TableCell><strong>Current Value</strong></TableCell>
              <TableCell><strong>Acceptable Range</strong></TableCell>
              <TableCell><strong>Error</strong></TableCell>
              <TableCell><strong>Rectification</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rectifications.map((rectification, index) => {
              const backgroundColor = rectification['error type'] === 'large error'
                ? '#f44336'
                : '#ffa726';
              return (
                <TableRow key={index}>
                  <TableCell sx={{ backgroundColor }}>{rectification['angle name']}</TableCell>
                  <TableCell>{`${rectification['current angle value']}°`}</TableCell>
                  <TableCell>{rectification['acceptable range']}</TableCell>
                  <TableCell>
                    <Typography variant="body2" color="error">
                      <strong>{rectification['error description']}</strong>
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      <strong>{rectification['neighboring joints to change']}</strong>
                    </Typography>
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Rectifications;