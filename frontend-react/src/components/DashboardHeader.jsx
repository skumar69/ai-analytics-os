import {
  Paper,
  Typography,
  Box,
  Chip,
} from "@mui/material";

import PsychologyIcon from "@mui/icons-material/Psychology";
import CloudDoneIcon from "@mui/icons-material/CloudDone";

export default function DashboardHeader() {

  return (

    <Paper
      elevation={4}
      sx={{
        p:4,
        borderRadius:3,
        mb:4,
      }}
    >

      <Typography
        variant="h3"
        fontWeight="bold"
      >
        👋 Welcome Sanjeev
      </Typography>

      <Typography
        color="text.secondary"
        mt={1}
      >
        VisionIQ Enterprise • SAP PM Analytics • FastAPI • React • AI
      </Typography>

      <Box
        mt={3}
        display="flex"
        gap={2}
      >

        <Chip
          icon={<CloudDoneIcon />}
          label="Backend Connected"
          color="success"
        />

        <Chip
          icon={<PsychologyIcon />}
          label="AI Engine Active"
          color="primary"
        />

      </Box>

    </Paper>

  );

}