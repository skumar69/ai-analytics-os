import { Card, CardContent, Typography, Box, Skeleton } from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";

function KpiCard({ title, value, icon, subtitle, trend, loading = false, color = "primary" }) {
  if (loading) {
    return (
      <Card sx={{ borderRadius: 3, height: "100%" }}>
        <CardContent>
          <Skeleton variant="text" width="60%" />
          <Skeleton variant="text" width="40%" height={52} />
          <Skeleton variant="text" width="70%" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      sx={{
        borderRadius: 3,
        height: "100%",
        borderTop: `3px solid`,
        borderTopColor: `${color}.main`,
        transition: "transform 0.15s",
        "&:hover": { transform: "translateY(-2px)" },
      }}
    >
      <CardContent>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <Typography variant="caption" color="text.secondary" fontWeight={600} textTransform="uppercase" letterSpacing={0.8}>
            {title}
          </Typography>
          <Box sx={{ color: `${color}.main`, opacity: 0.8 }}>
            {icon}
          </Box>
        </Box>

        <Typography variant="h4" fontWeight="bold" sx={{ mt: 1, mb: 0.3 }}>
          {value ?? "—"}
        </Typography>

        {(subtitle || trend != null) && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
            {trend != null && (
              trend >= 0
                ? <TrendingUpIcon sx={{ fontSize: 16, color: "success.main" }} />
                : <TrendingDownIcon sx={{ fontSize: 16, color: "error.main" }} />
            )}
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default KpiCard;