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
  Box,
} from "@mui/material";

import API from "../services/api";

export default function IncidentTable() {

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {

    try {

      const response = await fetch(`${API}/high-risk-assets`);

      if (!response.ok) {
        throw new Error("Unable to load High Risk Assets");
      }

      const data = await response.json();

      console.log("High Risk Assets:", data);

      setRows(Array.isArray(data) ? data : []);

    } catch (err) {

      console.error("IncidentTable Error:", err);

      setRows([]);

    } finally {

      setLoading(false);

    }

  };

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

  if (loading) {

    return (
      <Paper
        elevation={4}
        sx={{
          p: 4,
          borderRadius: 3,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <CircularProgress />
      </Paper>
    );

  }

  if (rows.length === 0) {

    return (
      <Paper
        elevation={4}
        sx={{
          p: 4,
          borderRadius: 3,
        }}
      >
        <Typography align="center">
          No High Risk Assets Available
        </Typography>
      </Paper>
    );

  }

  return (

    <Paper
      elevation={4}
      sx={{
        p: 3,
        borderRadius: 3,
      }}
    >

      <Typography
        variant="h5"
        fontWeight="bold"
      >
        🚨 High Risk Assets
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Box sx={{ overflowX: "auto" }}>

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

              <TableRow
                key={index}
                hover
              >

                <TableCell>{row.equipment}</TableCell>

                <TableCell>{row.plant}</TableCell>

                <TableCell>

                  <Chip
                    label={row.priority}
                    color={getColor(row.priority)}
                    size="small"
                  />

                </TableCell>

                <TableCell>{row.health}%</TableCell>

                <TableCell>{row.status}</TableCell>

              </TableRow>

            ))}

          </TableBody>

        </Table>

      </Box>

    </Paper>

  );

}