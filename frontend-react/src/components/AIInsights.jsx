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
  Box,
} from "@mui/material";

import LightbulbIcon from "@mui/icons-material/Lightbulb";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import BuildCircleIcon from "@mui/icons-material/BuildCircle";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";

import API from "../services/api";

export default function AIInsights() {
  const [data, setData] = useState(null);

  useEffect(() => {
    loadInsights();
  }, []);

  const loadInsights = async () => {
    try {
      const response = await fetch(`${API}/ai-insights`);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const result = await response.json();

      console.log("AI Insights:", result);

      setData(result);
    } catch (error) {
      console.error("AIInsights Error:", error);

      setData({
        summary: {
          critical_incidents: 0,
          overdue_pm: 0,
          high_risk_assets: 0,
          asset_health: "N/A",
        },
        recommendations: [
          "Unable to load AI recommendations.",
          "Please verify backend connectivity.",
        ],
      });
    }
  };

  if (!data) {
    return (
      <Paper sx={{ p: 4 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <CircularProgress />
        </Box>
      </Paper>
    );
  }

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
            label={`Critical: ${data.summary?.critical_incidents ?? 0}`}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <Chip
            color="warning"
            icon={<BuildCircleIcon />}
            label={`Overdue PM: ${data.summary?.overdue_pm ?? 0}`}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <Chip
            color="secondary"
            label={`High Risk: ${data.summary?.high_risk_assets ?? 0}`}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <Chip
            color="success"
            icon={<MonitorHeartIcon />}
            label={`Health: ${data.summary?.asset_health ?? "N/A"}`}
          />
        </Grid>
      </Grid>

      <Divider sx={{ my: 3 }} />

      <Typography variant="h6" gutterBottom>
        AI Recommendations
      </Typography>

      <List>
        {(data.recommendations || []).map((item, index) => (
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