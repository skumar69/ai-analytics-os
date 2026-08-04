import Grid from "@mui/material/Grid";
import EngineeringIcon from "@mui/icons-material/Engineering";
import NotificationsIcon from "@mui/icons-material/Notifications";
import PrecisionManufacturingIcon from "@mui/icons-material/PrecisionManufacturing";
import FactoryIcon from "@mui/icons-material/Factory";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";
import PsychologyIcon from "@mui/icons-material/Psychology";

import KpiCard from "./KpiCard";

export default function KPISection({ stats }) {
  return (
    <Grid container spacing={3}>

      <Grid item xs={12} sm={6} md={2}>
        <KpiCard
          title="Work Orders"
          value={stats.work_orders}
          icon={<EngineeringIcon fontSize="large" />}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={2}>
        <KpiCard
          title="Notifications"
          value={stats.notifications}
          icon={<NotificationsIcon fontSize="large" />}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={2}>
        <KpiCard
          title="Equipment"
          value={stats.equipment}
          icon={<PrecisionManufacturingIcon fontSize="large" />}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={2}>
        <KpiCard
          title="Plants"
          value={stats.plants}
          icon={<FactoryIcon fontSize="large" />}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={2}>
        <KpiCard
          title="Asset Health"
          value={`${stats.asset_health}%`}
          icon={<MonitorHeartIcon fontSize="large" />}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={2}>
        <KpiCard
          title="AI Score"
          value="96%"
          icon={<PsychologyIcon fontSize="large" />}
        />
      </Grid>

    </Grid>
  );
}