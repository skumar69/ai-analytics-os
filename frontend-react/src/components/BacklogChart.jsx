import { Paper, Typography } from "@mui/material";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Cell,
} from "recharts";

const backlogColor = (count) =>
  count > 50 ? "#d32f2f" : count > 25 ? "#ed6c02" : "#2e7d32";

export default function BacklogChart({ data = [] }) {
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Backlog by Plant
      </Typography>
      {data.length === 0 ? (
        <Typography color="text.secondary">No backlog data available.</Typography>
      ) : (
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" />
            <YAxis type="category" dataKey="plant" width={60} />
            <Tooltip />
            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
              {data.map((entry, i) => (
                <Cell key={i} fill={backlogColor(entry.count)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
