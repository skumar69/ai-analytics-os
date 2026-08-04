import {
  Container,
  Grid,
  Typography,
  Paper,
  Divider,
} from "@mui/material";

import KpiCard from "../components/KpiCard";
import WorkOrderChart from "../charts/WorkOrderChart";
import FileUpload from "../components/FileUpload";

import EngineeringIcon from "@mui/icons-material/Engineering";
import NotificationsIcon from "@mui/icons-material/Notifications";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";

export default function Dashboard({ stats }) {
  return (
    <Container
      maxWidth="xl"
      sx={{
        ml: "240px",
        mt: "90px",
        mb: 5,
      }}
    >
      <Typography variant="h3" fontWeight="bold">
        VisionIQ Dashboard
      </Typography>

      <Typography color="text.secondary" sx={{ mb: 4 }}>
        AI Powered SAP PM Analytics Platform
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <KpiCard
            title="Work Orders"
            value={stats.work_orders}
            icon={<EngineeringIcon />}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <KpiCard
            title="Notifications"
            value={stats.notifications}
            icon={<NotificationsIcon />}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <KpiCard
            title="Asset Health"
            value={`${stats.asset_health}%`}
            icon={<MonitorHeartIcon />}
          />
        </Grid>
      </Grid>

      <Paper sx={{ mt: 5, p: 3, borderRadius: 3 }}>
        <Typography variant="h5">
          Monthly Work Order Trend
        </Typography>

        <Divider sx={{ my: 2 }} />

        <WorkOrderChart />
      </Paper>

      <FileUpload />
    </Container>
  );
}