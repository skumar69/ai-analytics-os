import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Box,
  Alert,
} from "@mui/material";

import API from "../services/api";

export default function NotificationTable() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API}/notifications`);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();

      console.log("Notifications:", data);

      if (Array.isArray(data)) {
        setRows(data);
      } else {
        setRows([]);
      }

    } catch (err) {
      console.error("Notification Error:", err);
      setError(err.message || "Unable to load notifications.");
      setRows([]);
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

  const getStatusColor = (status) => {
    switch ((status || "").toLowerCase()) {
      case "open":
        return "error";
      case "in progress":
        return "warning";
      case "completed":
      case "closed":
        return "success";
      default:
        return "default";
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          py: 6,
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
        mt: 5,
        p: 3,
        borderRadius: 3,
      }}
    >
      <Typography
        variant="h5"
        fontWeight="bold"
        gutterBottom
      >
        🔔 Recent Notifications
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {!error && rows.length === 0 && (
        <Alert severity="info">
          No notifications available.
        </Alert>
      )}

      {!error && rows.length > 0 && (
        <TableContainer sx={{ maxHeight: 420 }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell><b>Notification</b></TableCell>
                <TableCell><b>Equipment</b></TableCell>
                <TableCell><b>Priority</b></TableCell>
                <TableCell><b>Status</b></TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {rows.map((row, index) => (
                <TableRow key={index} hover>
                  <TableCell>{row.notification}</TableCell>

                  <TableCell>{row.equipment}</TableCell>

                  <TableCell>
                    <Chip
                      size="small"
                      label={row.priority}
                      color={getPriorityColor(row.priority)}
                    />
                  </TableCell>

                  <TableCell>
                    <Chip
                      size="small"
                      label={row.status}
                      color={getStatusColor(row.status)}
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