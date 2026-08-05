import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  CircularProgress,
  Box,
  Alert,
} from "@mui/material";

import API from "../services/api";

export default function HighRiskAssets() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API}/high-risk-assets`);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();

      if (Array.isArray(data)) {
        setAssets(data);
      } else {
        setAssets([]);
      }

    } catch (err) {
      console.error("High Risk Assets Error:", err);
      setError(err.message || "Unable to load assets.");
      setAssets([]);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch ((priority || "").toLowerCase()) {
      case "critical":
        return "error";
      case "high":
        return "warning";
      case "medium":
        return "info";
      default:
        return "success";
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          p: 5,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper
      elevation={4}
      sx={{
        p: 3,
        mt: 5,
        borderRadius: 3,
      }}
    >
      <Typography
        variant="h5"
        fontWeight="bold"
        gutterBottom
      >
        🚨 High Risk Assets
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {!error && assets.length === 0 && (
        <Alert severity="info">
          No high-risk assets found.
        </Alert>
      )}

      {!error && assets.length > 0 && (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><b>Equipment</b></TableCell>
              <TableCell><b>Plant</b></TableCell>
              <TableCell><b>Priority</b></TableCell>
              <TableCell><b>Health %</b></TableCell>
              <TableCell><b>Status</b></TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {assets.map((row, index) => (
              <TableRow key={index} hover>
                <TableCell>{row.equipment}</TableCell>

                <TableCell>{row.plant}</TableCell>

                <TableCell>
                  <Chip
                    size="small"
                    label={row.priority}
                    color={getPriorityColor(row.priority)}
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