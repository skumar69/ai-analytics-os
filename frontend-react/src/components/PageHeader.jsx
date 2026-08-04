import { Box, Typography, Breadcrumbs, Link } from "@mui/material";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";

export default function PageHeader({ title, subtitle, breadcrumbs = [], actions }) {
  return (
    <Box
      sx={{
        display: "flex", alignItems: "flex-start",
        justifyContent: "space-between", mb: 3,
      }}
    >
      <Box>
        {breadcrumbs.length > 0 && (
          <Breadcrumbs
            separator={<NavigateNextIcon fontSize="small" />}
            sx={{ mb: 0.5 }}
          >
            {breadcrumbs.map((crumb, i) =>
              i < breadcrumbs.length - 1 ? (
                <Link key={crumb} underline="hover" color="text.secondary" sx={{ fontSize: 13 }}>
                  {crumb}
                </Link>
              ) : (
                <Typography key={crumb} sx={{ fontSize: 13, color: "text.primary" }}>
                  {crumb}
                </Typography>
              )
            )}
          </Breadcrumbs>
        )}
        <Typography variant="h5" fontWeight="bold">{title}</Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.3 }}>
            {subtitle}
          </Typography>
        )}
      </Box>
      {actions && <Box sx={{ display: "flex", gap: 1, mt: 0.5 }}>{actions}</Box>}
    </Box>
  );
}
