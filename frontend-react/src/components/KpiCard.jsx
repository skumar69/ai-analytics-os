import { Card, CardContent, Typography } from "@mui/material";

function KpiCard({ title, value, icon }) {
  return (
    <Card
      sx={{
        bgcolor: "#1e293b",
        color: "white",
        borderRadius: 3,
      }}
    >
      <CardContent>
        {icon}

        <Typography variant="h5" sx={{ mt: 1 }}>
          {title}
        </Typography>

        <Typography
          variant="h2"
          sx={{
            color: "white",
            fontWeight: "bold",
          }}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default KpiCard;