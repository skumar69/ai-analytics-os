import {
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
  CartesianGrid,
} from "recharts";

import {
  Paper,
  Typography,
} from "@mui/material";

export default function PlantChart({ data = [] }) {
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
        Plant Distribution
      </Typography>

      {data.length === 0 ? (
        <Typography
          align="center"
          color="text.secondary"
          sx={{ py: 8 }}
        >
          No plant data available
        </Typography>
      ) : (
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="plant" />

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