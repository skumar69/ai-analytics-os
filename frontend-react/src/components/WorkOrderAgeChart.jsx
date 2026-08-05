import { Paper, Typography } from "@mui/material";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export default function WorkOrderAgeChart({
  buckets = [],
  avgDays,
  maxDays,
}) {
  return (
    <Paper elevation={3} sx={{ p: 3, borderRadius: 3 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Work Order Age Analysis
      </Typography>

      {avgDays != null && (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Average Age: <strong>{avgDays} Days</strong>
          {" | "}
          Maximum Age: <strong>{maxDays} Days</strong>
        </Typography>
      )}

      {buckets.length === 0 ? (
        <Typography color="text.secondary">
          No work order age data available.
        </Typography>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={buckets}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" />
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