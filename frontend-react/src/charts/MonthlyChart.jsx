import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

import {
  Paper,
  Typography,
  CircularProgress,
  Box,
} from "@mui/material";

export default function MonthlyChart() {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChart();
  }, []);

  const loadChart = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/workorder-trend"
      );

      if (!response.ok) {
        throw new Error("Unable to fetch Monthly Trend");
      }

      const result = await response.json();

      console.log("Monthly Trend:", result);

      setData(Array.isArray(result) ? result : []);

    } catch (err) {

      console.error(err);
      setData([]);

    } finally {

      setLoading(false);

    }

  };

  if (loading) {

    return (
      <Box
        sx={{
          height: 350,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <CircularProgress />
      </Box>
    );

  }

  if (data.length === 0) {

    return (
      <Paper
        sx={{
          height: 350,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Typography>No Monthly Trend Data Available</Typography>
      </Paper>
    );

  }

  return (

    <Paper
      elevation={0}
      sx={{ p: 2 }}
    >

      <Typography
        variant="h6"
        fontWeight="bold"
        gutterBottom
      >
        📈 Monthly Work Order Trend
      </Typography>

      <ResponsiveContainer
        width="100%"
        height={320}
      >

        <LineChart data={data}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="month" />

          <YAxis />

          <Tooltip />

          <Legend />

          <Line
            type="monotone"
            dataKey="orders"
            name="Work Orders"
            stroke="#1976d2"
            strokeWidth={3}
            dot={{ r: 5 }}
            activeDot={{ r: 8 }}
          />

        </LineChart>

      </ResponsiveContainer>

    </Paper>

  );

}