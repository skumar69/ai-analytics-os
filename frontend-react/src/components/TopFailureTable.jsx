import {
  Paper, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Chip,
} from "@mui/material";

const riskColor = { Critical: "error", High: "warning", Medium: "info", Low: "success" };

export default function TopFailureTable({ data = [], onRowClick }) {
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, p: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Top Failed Equipment
      </Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>Equipment</TableCell>
              <TableCell align="right">Failures</TableCell>
              {data[0]?.health_score != null && <TableCell align="right">Health</TableCell>}
              {data[0]?.risk != null && <TableCell align="center">Risk</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, i) => (
              <TableRow
                key={row.equipment}
                hover
                onClick={() => onRowClick && onRowClick(row.equipment)}
                sx={{ cursor: onRowClick ? "pointer" : "default" }}
              >
                <TableCell>{i + 1}</TableCell>
                <TableCell>{row.equipment}</TableCell>
                <TableCell align="right">{row.failures ?? row.failure_count}</TableCell>
                {row.health_score != null && (
                  <TableCell align="right">{row.health_score}%</TableCell>
                )}
                {row.risk != null && (
                  <TableCell align="center">
                    <Chip
                      label={row.risk}
                      color={riskColor[row.risk] ?? "default"}
                      size="small"
                    />
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
