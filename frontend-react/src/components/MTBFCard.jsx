import { Card, CardContent, Typography, Box } from "@mui/material";
import LoopIcon from "@mui/icons-material/Loop";

export default function MTBFCard({ value, sampleSize, source }) {
  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
          <LoopIcon color="success" />
          <Typography variant="subtitle2" color="text.secondary">
            MTBF
          </Typography>
        </Box>
        <Typography variant="h4" fontWeight="bold" color="success.main">
          {value != null ? `${value}d` : "—"}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Mean Time Between Failures
        </Typography>
        {sampleSize > 0 && (
          <Typography variant="caption" display="block" color="text.secondary">
            Based on {sampleSize} intervals
          </Typography>
        )}
        {source === "demo" && (
          <Typography variant="caption" display="block" sx={{ color: "warning.main" }}>
            Demo data — upload SAP Excel to calculate
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
