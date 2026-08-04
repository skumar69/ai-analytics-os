import Grid from "@mui/material/Grid";
import EngineeringIcon from "@mui/icons-material/Engineering";
import NotificationsIcon from "@mui/icons-material/Notifications";
import PrecisionManufacturingIcon from "@mui/icons-material/PrecisionManufacturing";
import FactoryIcon from "@mui/icons-material/Factory";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";
import PsychologyIcon from "@mui/icons-material/Psychology";

import KpiCard from "./KpiCard";

export default function KPISection({ stats, loading = false }) {
  return (
    <Grid container spacing={3}>
      <Grid item xs={6} sm={4} md={2}>
        <KpiCard title="Work Orders" value={stats?.work_orders} loading={loading}
          icon={<EngineeringIcon />} subtitle="Total open & closed" color="primary" />
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <KpiCard title="Notifications" value={stats?.notifications} loading={loading}
          icon={<NotificationsIcon />} subtitle="Active notifications" color="warning" />
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <KpiCard title="Equipment" value={stats?.equipment} loading={loading}
          icon={<PrecisionManufacturingIcon />} subtitle="Unique assets" color="secondary" />
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <KpiCard title="Plants" value={stats?.plants} loading={loading}
          icon={<FactoryIcon />} subtitle="Active plants" color="info" />
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <KpiCard title="Asset Health" value={stats?.asset_health != null ? `${stats.asset_health}%` : null}
          loading={loading} icon={<MonitorHeartIcon />} subtitle="Fleet average" color="success" />
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <KpiCard title="AI Score" value={stats?.ai_score != null ? `${stats.ai_score}%` : null}
          loading={loading} icon={<PsychologyIcon />} subtitle="Confidence level" color="primary" />
      </Grid>
    </Grid>
  );
}