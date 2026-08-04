import { Card, CardContent, Typography, Box } from "@mui/material";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";

export default function BreakdownCard({ breakdownPct, breakdownCount, total, source }) {
  const pct = breakdownPct ?? 0;
  const color = pct > 30 ? "error" : pct > 15 ? "warning" : "success";

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
          <WarningAmberIcon color={color} />
          <Typography variant="subtitle2" color="text.secondary">
            Breakdown %
          </Typography>
        </Box>
        <Typography variant="h4" fontWeight="bold" color={`${color}.main`}>
          {pct}%
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Corrective vs Total Orders
        </Typography>
        {total > 0 && (
          <Typography variant="caption" display="block" color="text.secondary">
            {breakdownCount} breakdowns out of {total}
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
