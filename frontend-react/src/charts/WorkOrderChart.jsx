import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  LineChart,
  Line,
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

export default function WorkOrderChart() {

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

      console.log("Status :", response.status);

      const result = await response.json();

      console.log("API Response :", result);

      if (Array.isArray(result)) {
        setData(result);
      } else {
        console.error("Invalid response format");
        setData([]);
      }

    } catch (error) {

      console.error(error);
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

  return (

    <Paper
      elevation={0}
      sx={{ p: 2 }}
    >

      {data.length === 0 ? (

        <Typography align="center">
          No chart data available
        </Typography>

      ) : (

        <ResponsiveContainer
          width="100%"
          height={350}
        >

          <LineChart data={data}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="month" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="orders"
              stroke="#1976d2"
              strokeWidth={3}
              dot={{ r: 5 }}
            />

          </LineChart>

        </ResponsiveContainer>

      )}

    </Paper>

  );

}