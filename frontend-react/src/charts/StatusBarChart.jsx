import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  Paper,
  Typography,
  CircularProgress,
  Box,
} from "@mui/material";

import API from "../services/api";

export default function StatusBarChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChart();
  }, []);

  const loadChart = async () => {
    try {
      const response = await fetch(`${API}/status-chart`);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const result = await response.json();

      console.log("Status Chart:", result);

      if (Array.isArray(result)) {
        setData(result);
      } else {
        console.error("Invalid response format:", result);
        setData([]);
      }
    } catch (err) {
      console.error("StatusBarChart Error:", err);
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          height: 320,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper
      elevation={3}
      sx={{
        p: 2,
        borderRadius: 3,
      }}
    >
      <Typography
        variant="h6"
        fontWeight="bold"
        gutterBottom
      >
        Status Distribution
      </Typography>

      {data.length === 0 ? (
        <Typography align="center">
          No chart data available
        </Typography>
      ) : (
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="status" />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey="count"
              fill="#1976d2"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}