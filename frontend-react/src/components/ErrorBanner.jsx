import { Alert, Box, Collapse, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useState } from "react";

export default function ErrorBanner({ message, onRetry }) {
  const [open, setOpen] = useState(true);

  if (!message) return null;

  return (
    <Collapse in={open}>
      <Alert
        severity="error"
        sx={{ mb: 2, borderRadius: 2 }}
        action={
          <Box sx={{ display: "flex", gap: 0.5, alignItems: "center" }}>
            {onRetry && (
              <IconButton size="small" color="inherit" onClick={onRetry}>
                ↺
              </IconButton>
            )}
            <IconButton size="small" color="inherit" onClick={() => setOpen(false)}>
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>
        }
      >
        {message}
      </Alert>
    </Collapse>
  );
}
