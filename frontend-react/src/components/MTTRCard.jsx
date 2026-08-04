import { Card, CardContent, Typography, Box } from "@mui/material";
import AccessTimeIcon from "@mui/icons-material/AccessTime";

export default function MTTRCard({ value, sampleSize, source }) {
  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
          <AccessTimeIcon color="primary" />
          <Typography variant="subtitle2" color="text.secondary">
            MTTR
          </Typography>
        </Box>
        <Typography variant="h4" fontWeight="bold" color="primary">
          {value != null ? `${value}d` : "—"}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Mean Time To Repair
        </Typography>
        {sampleSize > 0 && (
          <Typography variant="caption" display="block" color="text.secondary">
            Based on {sampleSize} orders
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
