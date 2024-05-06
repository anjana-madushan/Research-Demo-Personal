import { Typography } from "@mui/material"

// eslint-disable-next-line react/prop-types
export const ShotClassification = ({ message }) => {
  return (
    <Typography variant="h5" fontWeight="bold">You have performed a {message}</Typography>
  )
}
