import { Paper, Typography } from "@mui/material";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Cell, ReferenceLine,
} from "recharts";

const scoreColor = (score) =>
  score < 40 ? "#d32f2f" : score < 60 ? "#ed6c02" : score < 80 ? "#1976d2" : "#2e7d32";

export default function EquipmentHealthGauge({ data = [], onBarClick }) {
  const display = data.slice(0, 12);

  const handleClick = (entry) => {
    if (onBarClick && entry?.activePayload?.[0]?.payload?.equipment) {
      onBarClick(entry.activePayload[0].payload.equipment);
    }
  };

  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Equipment Health Scores
      </Typography>
      {display.length === 0 ? (
        <Typography color="text.secondary">No health data available.</Typography>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={display} onClick={handleClick} style={{ cursor: "pointer" }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="equipment" tick={{ fontSize: 11 }} />
            <YAxis domain={[0, 100]} />
            <Tooltip formatter={(v) => [`${v}%`, "Health Score"]} />
            <ReferenceLine y={60} stroke="#ed6c02" strokeDasharray="4 4" label={{ value: "60%", position: "right", fontSize: 11 }} />
            <Bar dataKey="health_score" radius={[6, 6, 0, 0]}>
              {display.map((entry, i) => (
                <Cell key={i} fill={scoreColor(entry.health_score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
