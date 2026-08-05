import { useEffect, useState } from "react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

import {
  Paper,
  Typography,
  CircularProgress,
  Box,
} from "@mui/material";

import API from "../services/api";

const COLORS = [
  "#d32f2f",
  "#f57c00",
  "#1976d2",
  "#43a047",
];

export default function PriorityPieChart() {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChart();
  }, []);

  const loadChart = async () => {

    try {

      const response = await fetch(`${API}/priority-chart`);

      if (!response.ok) {
        throw new Error("Unable to load Priority Chart");
      }

      const result = await response.json();

      console.log("Priority Chart:", result);

      setData(Array.isArray(result) ? result : []);

    } catch (err) {

      console.error("Priority Chart Error:", err);

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

  if (data.length === 0) {

    return (
      <Paper
        elevation={4}
        sx={{
          p: 3,
          borderRadius: 3,
          height: 320,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Typography>No Priority Data Available</Typography>
      </Paper>
    );

  }

  return (

    <Paper
      elevation={4}
      sx={{
        p: 3,
        borderRadius: 3,
        height: 420,
      }}
    >

      <Typography
        variant="h6"
        fontWeight="bold"
        gutterBottom
      >
        🥧 Priority Distribution
      </Typography>

      <ResponsiveContainer
        width="100%"
        height={320}
      >

        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={110}
            label
          >

            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
              />
            ))}

          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>

      </ResponsiveContainer>

    </Paper>

  );

}