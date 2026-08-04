import { Paper, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, LinearProgress, Chip } from "@mui/material";

const tier_color = (pct) => pct >= 80 ? "success" : pct >= 60 ? "warning" : "error";

export default function PlannerPerformanceTable({ data = [] }) {
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Planner Group Performance
      </Typography>
      {data.length === 0 ? (
        <Typography color="text.secondary">No data available.</Typography>
      ) : (
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Planner Group</TableCell>
                <TableCell align="right">Total</TableCell>
                <TableCell align="right">Completed</TableCell>
                <TableCell align="right">Backlog</TableCell>
                <TableCell>Compliance</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow key={row.planner_group} hover>
                  <TableCell fontWeight="bold">{row.planner_group}</TableCell>
                  <TableCell align="right">{row.total}</TableCell>
                  <TableCell align="right">{row.completed}</TableCell>
                  <TableCell align="right">
                    <Chip label={row.backlog} size="small"
                      color={row.backlog > 10 ? "error" : row.backlog > 5 ? "warning" : "success"} />
                  </TableCell>
                  <TableCell sx={{ minWidth: 140 }}>
                    <Typography variant="caption">{row.compliance_pct}%</Typography>
                    <LinearProgress
                      variant="determinate" value={row.compliance_pct}
                      color={tier_color(row.compliance_pct)}
                      sx={{ mt: 0.5, borderRadius: 2, height: 6 }}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Paper>
  );
}
