import { useEffect, useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Chip,
  Alert,
} from "@mui/material";

import API from "../services/api";

const STATUS_COLOR = {
  open: "error",
  "in progress": "warning",
  completed: "success",
  closed: "success",
  teco: "success",
};

export default function DrillDownDialog({ equipment, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!equipment) return;

    loadEquipmentDetails();
  }, [equipment]);

  const loadEquipmentDetails = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API}/analytics/equipment/${encodeURIComponent(equipment)}`
      );

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const result = await response.json();

      setData(result);
    } catch (err) {
      console.error("Equipment Detail Error:", err);
      setError(err.message || "Unable to load equipment details.");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog
      open={Boolean(equipment)}
      onClose={onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        Equipment Detail: <strong>{equipment}</strong>
      </DialogTitle>

      <DialogContent dividers>
        {loading ? (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              p: 4,
            }}
          >
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : !data || !Array.isArray(data.work_orders) || data.work_orders.length === 0 ? (
          <Typography color="text.secondary">
            No work order history available for this equipment.
          </Typography>
        ) : (
          <>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ mb: 2 }}
            >
              {data.total} work order{data.total !== 1 ? "s" : ""} found
            </Typography>

            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Work Order</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Priority</TableCell>
                    <TableCell>Created</TableCell>
                    <TableCell>Completed</TableCell>
                    <TableCell>Description</TableCell>
                  </TableRow>
                </TableHead>

                <TableBody>
                  {data.work_orders.map((row, index) => (
                    <TableRow key={index} hover>
                      <TableCell>{row.work_order || "—"}</TableCell>

                      <TableCell>
                        <Chip
                          size="small"
                          label={row.status || "—"}
                          color={
                            STATUS_COLOR[
                              row.status?.toLowerCase()
                            ] || "default"
                          }
                        />
                      </TableCell>

                      <TableCell>{row.priority || "—"}</TableCell>

                      <TableCell>{row.created_on || "—"}</TableCell>

                      <TableCell>{row.completed_on || "—"}</TableCell>

                      <TableCell
                        sx={{
                          maxWidth: 220,
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          whiteSpace: "nowrap",
                        }}
                      >
                        {row.description || "—"}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </>
        )}
      </DialogContent>

      <DialogActions>
        <Button
          variant="contained"
          onClick={onClose}
        >
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}