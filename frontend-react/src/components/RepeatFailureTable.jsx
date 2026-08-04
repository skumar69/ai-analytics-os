import { Paper, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Chip } from "@mui/material";

const risk_color = { Critical: "error", High: "warning", Medium: "info" };

export default function RepeatFailureTable({ data = [] }) {
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Repeat Failure Analysis
      </Typography>
      {data.length === 0 ? (
        <Typography color="text.secondary">No chronic failures detected.</Typography>
      ) : (
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Equipment</TableCell>
                <TableCell align="right">Failures</TableCell>
                <TableCell align="right">Repeat Rate</TableCell>
                <TableCell align="center">Risk</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow key={row.equipment} hover>
                  <TableCell>{row.equipment}</TableCell>
                  <TableCell align="right">{row.failures}</TableCell>
                  <TableCell align="right">{row.repeat_rate_pct}%</TableCell>
                  <TableCell align="center">
                    <Chip label={row.risk} size="small"
                      color={risk_color[row.risk] ?? "default"} />
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
