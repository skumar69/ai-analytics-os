import { Card, CardContent, Typography, Box, LinearProgress } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

export default function PMComplianceCard({ compliancePct, completed, total, source }) {
  const pct = compliancePct ?? 0;
  const color = pct >= 80 ? "success" : pct >= 60 ? "warning" : "error";

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
          <CheckCircleIcon color={color} />
          <Typography variant="subtitle2" color="text.secondary">
            PM Compliance
          </Typography>
        </Box>
        <Typography variant="h4" fontWeight="bold" color={`${color}.main`}>
          {pct}%
        </Typography>
        <LinearProgress
          variant="determinate"
          value={pct}
          color={color}
          sx={{ mt: 1, mb: 1, borderRadius: 2, height: 8 }}
        />
        {total > 0 && (
          <Typography variant="caption" color="text.secondary">
            {completed} / {total} orders completed
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
