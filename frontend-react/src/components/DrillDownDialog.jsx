import { useEffect, useState } from "react";
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, Typography, Box, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, CircularProgress, Chip,
} from "@mui/material";

const STATUS_COLOR = {
  open: "error", "in progress": "warning",
  completed: "success", closed: "success", teco: "success",
};

export default function DrillDownDialog({ equipment, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!equipment) return;
    setLoading(true);
    fetch(`http://127.0.0.1:8000/analytics/equipment/${encodeURIComponent(equipment)}`)
      .then((r) => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [equipment]);

  return (
    <Dialog open={!!equipment} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        Equipment Detail: <strong>{equipment}</strong>
      </DialogTitle>

      <DialogContent dividers>
        {loading ? (
          <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
            <CircularProgress />
          </Box>
        ) : !data || data.work_orders.length === 0 ? (
          <Typography color="text.secondary">
            No work order history available for this equipment.
          </Typography>
        ) : (
          <>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
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
                  {data.work_orders.map((row, i) => (
                    <TableRow key={i} hover>
                      <TableCell>{row.work_order || "—"}</TableCell>
                      <TableCell>
                        <Chip
                          label={row.status || "—"}
                          color={STATUS_COLOR[row.status?.toLowerCase()] ?? "default"}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{row.priority || "—"}</TableCell>
                      <TableCell>{row.created_on || "—"}</TableCell>
                      <TableCell>{row.completed_on || "—"}</TableCell>
                      <TableCell sx={{ maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
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
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}
