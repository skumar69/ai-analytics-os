import { Card, CardContent, Typography, Box, LinearProgress } from "@mui/material";

const risk_color = { Red: "error", Amber: "warning", Green: "success" };
const risk_hex   = { Red: "#d32f2f", Amber: "#ed6c02", Green: "#2e7d32" };

export default function AssetHealthCard({ equipment, healthScore, riskLevel, details = {} }) {
  const color = risk_color[riskLevel] ?? "info";

  return (
    <Card
      elevation={3}
      sx={{
        borderRadius: 3,
        borderLeft: `4px solid ${risk_hex[riskLevel] ?? "#1976d2"}`,
        height: "100%",
      }}
    >
      <CardContent>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <Typography variant="subtitle2" fontWeight="bold" noWrap sx={{ maxWidth: "70%" }}>
            {equipment}
          </Typography>
          <Typography
            variant="caption"
            fontWeight="bold"
            sx={{ color: risk_hex[riskLevel], whiteSpace: "nowrap" }}
          >
            {riskLevel}
          </Typography>
        </Box>

        <Typography variant="h4" fontWeight="bold" color={`${color}.main`} sx={{ mt: 0.5 }}>
          {healthScore}
        </Typography>
        <LinearProgress
          variant="determinate"
          value={healthScore}
          color={color}
          sx={{ mt: 0.5, mb: 1, borderRadius: 2, height: 6 }}
        />

        <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
          {details.failure_count != null && (
            <Typography variant="caption" color="text.secondary">
              Failures: <strong>{details.failure_count}</strong>
            </Typography>
          )}
          {details.open_orders != null && (
            <Typography variant="caption" color="text.secondary">
              Open: <strong>{details.open_orders}</strong>
            </Typography>
          )}
          {details.pm_compliance != null && (
            <Typography variant="caption" color="text.secondary">
              PM: <strong>{details.pm_compliance}%</strong>
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}
