import { Box, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import SearchOffIcon from "@mui/icons-material/SearchOff";
import BarChartIcon from "@mui/icons-material/BarChart";

const icons = {
  upload: CloudUploadIcon,
  nodata: SearchOffIcon,
  chart:  BarChartIcon,
};

export default function EmptyState({
  icon = "nodata",
  title = "No data available",
  message = "Upload a SAP PM Excel file to see analytics.",
  action,
}) {
  const Icon = icons[icon] ?? SearchOffIcon;

  return (
    <Box
      sx={{
        display: "flex", flexDirection: "column", alignItems: "center",
        justifyContent: "center", py: 6, px: 2, textAlign: "center",
      }}
    >
      <Icon sx={{ fontSize: 56, color: "text.secondary", mb: 2, opacity: 0.5 }} />
      <Typography variant="h6" color="text.secondary" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 360 }}>
        {message}
      </Typography>
      {action && <Box sx={{ mt: 2 }}>{action}</Box>}
    </Box>
  );
}
