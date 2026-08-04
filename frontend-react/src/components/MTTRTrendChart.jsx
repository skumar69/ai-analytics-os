import { Paper, Typography } from "@mui/material";
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ReferenceLine,
} from "recharts";

export default function MTTRTrendChart({ data = [], target = 3 }) {
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        MTTR Trend
      </Typography>
      {data.length === 0 ? (
        <Typography color="text.secondary">No trend data available.</Typography>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="period" tick={{ fontSize: 11 }} />
            <YAxis unit="d" />
            <Tooltip formatter={(v) => [`${v} days`, "MTTR"]} />
            <ReferenceLine
              y={target}
              stroke="#2e7d32"
              strokeDasharray="4 4"
              label={{ value: `Target ${target}d`, position: "right", fontSize: 11 }}
            />
            <Line
              type="monotone" dataKey="mttr_days" stroke="#1976d2"
              strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
