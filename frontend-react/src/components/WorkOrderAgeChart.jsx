import { Paper, Typography } from "@mui/material";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip,
} from "recharts";

export default function WorkOrderAgeChart({ buckets = [], avgDays, maxDays }) {
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Open Work Order Age
      </Typography>
      {avgDays != null && (
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Avg: <strong>{avgDays}d</strong> &nbsp;|&nbsp; Max: <strong>{maxDays}d</strong>
        </Typography>
      )}
      {buckets.length === 0 ? (
        <Typography color="text.secondary">No age data available.</Typography>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={buckets}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" tick={{ fontSize: 12 }} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#1976d2" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
