/* eslint-disable react/prop-types */
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
const Rectifications = ({ rectifications, accuracy, stroke, correctAngles }) => {

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
      <Typography variant="h6" color="#388e3c" sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}>{stroke.toUpperCase()}</Typography>
      <Box display="flex" alignItems="center" justifyContent="center" sx={{ marginY: 2 }}>
        {/* Container for Circular Progress and Accuracy */}
        <Box display="flex" alignItems="center" justifyContent="center" sx={{ marginRight: 3 }}>
          <Typography variant="h6" color="primary" sx={{ marginRight: 2 }}>Accuracy Percentage</Typography>
          <Box position="relative" display="inline-flex">
            <CircularProgress size={80} variant="determinate" value={accuracy} />
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
              <Typography variant="h6" component="div" color="textSecondary" sx={{ fontWeight: 'bold' }}>
                {`${accuracy}%`}
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* List of Correct Angles */}
        {correctAngles && (
          <Box>
            <Typography variant="h6" color="#66bb6a">
              Correct Angles
            </Typography>
            <Box>
              {correctAngles.map((angle, index) => (
                <Typography key={index} variant="body2">
                  {`${angle}`}
                </Typography>
              ))}
            </Box>
          </Box>
        )}
      </Box>

      <TableContainer component={Paper} sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Angle Name</strong></TableCell>
              <TableCell><strong>Current Angle(°)</strong></TableCell>
              <TableCell><strong>Acceptable Angle Range(°)</strong></TableCell>
              {/* <TableCell><strong>Error</strong></TableCell> */}
              <TableCell><strong>Joints for Adjustment</strong></TableCell>
              <TableCell><strong>Recommended Action</strong></TableCell>
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
                  <TableCell>{`${rectification['current angle value']}`}</TableCell>
                  <TableCell>{rectification['acceptable range']}</TableCell>
                  {/* <TableCell>
                    <Typography variant="body2" color="error">
                      <strong>{rectification['error description']}</strong>
                    </Typography>
                  </TableCell> */}
                  <TableCell>{rectification['neighboring joints to change']}</TableCell>
                  <TableCell>{rectification['action']}</TableCell>
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