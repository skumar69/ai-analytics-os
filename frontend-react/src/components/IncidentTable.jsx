import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Divider,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  CircularProgress,
} from "@mui/material";

export default function IncidentTable() {

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/high-risk-assets")
      .then((res) => res.json())
      .then((data) => {
        setRows(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));

  }, []);

  const getColor = (priority) => {
    switch (priority) {
      case "Critical":
        return "error";
      case "High":
        return "warning";
      case "Medium":
        return "info";
      default:
        return "success";
    }
  };

  return (

    <Paper
      elevation={4}
      sx={{
        p: 3,
        borderRadius: 3,
      }}
    >

      <Typography variant="h5" fontWeight="bold">
        🚨 High Risk Assets
      </Typography>

      <Divider sx={{ my: 2 }} />

      {loading ? (
        <CircularProgress />
      ) : (

        <Table>

          <TableHead>

            <TableRow>

              <TableCell><b>Equipment</b></TableCell>

              <TableCell><b>Plant</b></TableCell>

              <TableCell><b>Priority</b></TableCell>

              <TableCell><b>Health</b></TableCell>

              <TableCell><b>Status</b></TableCell>

            </TableRow>

          </TableHead>

          <TableBody>

            {rows.map((row, index) => (

              <TableRow key={index} hover>

                <TableCell>{row.equipment}</TableCell>

                <TableCell>{row.plant}</TableCell>

                <TableCell>

                  <Chip
                    label={row.priority}
                    color={getColor(row.priority)}
                  />

                </TableCell>

                <TableCell>{row.health}%</TableCell>

                <TableCell>{row.status}</TableCell>

              </TableRow>

            ))}

          </TableBody>

        </Table>

      )}

    </Paper>

  );

}