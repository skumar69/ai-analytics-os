import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Grid,
  Chip,
  CircularProgress,
} from "@mui/material";

import LightbulbIcon from "@mui/icons-material/Lightbulb";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import BuildCircleIcon from "@mui/icons-material/BuildCircle";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";

export default function AIInsights() {

  const [data, setData] = useState(null);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/ai-insights")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch(console.error);

  }, []);

  if (!data)
    return (
      <Paper sx={{ p: 4, textAlign: "center" }}>
        <CircularProgress />
      </Paper>
    );

  return (

    <Paper
      elevation={4}
      sx={{
        p: 3,
        borderRadius: 3,
      }}
    >

      <Typography variant="h5" fontWeight="bold">
        🤖 AI Insights
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Grid container spacing={2}>

        <Grid item xs={12} md={3}>
          <Chip
            color="error"
            icon={<WarningAmberIcon />}
            label={`Critical: ${data.summary.critical_incidents}`}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <Chip
            color="warning"
            icon={<BuildCircleIcon />}
            label={`Overdue PM: ${data.summary.overdue_pm}`}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <Chip
            color="secondary"
            label={`High Risk: ${data.summary.high_risk_assets}`}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <Chip
            color="success"
            icon={<MonitorHeartIcon />}
            label={`Health: ${data.summary.asset_health}`}
          />
        </Grid>

      </Grid>

      <Divider sx={{ my: 3 }} />

      <Typography
        variant="h6"
        gutterBottom
      >
        AI Recommendations
      </Typography>

      <List>

        {data.recommendations.map((item, index) => (

          <ListItem key={index}>

            <ListItemIcon>
              <LightbulbIcon color="warning" />
            </ListItemIcon>

            <ListItemText primary={item} />

          </ListItem>

        ))}

      </List>

    </Paper>

  );

}