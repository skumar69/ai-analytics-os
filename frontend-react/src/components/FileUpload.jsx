import { useState } from "react";
import DataPreview from "./DataPreview";

import {
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  Divider,
  Chip,
  Stack,
  CircularProgress,
} from "@mui/material";

import UploadFileIcon from "@mui/icons-material/UploadFile";
import RestartAltIcon from "@mui/icons-material/RestartAlt";

export default function FileUpload({ refreshDashboard }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [preview, setPreview] = useState([]);
  const [loading, setLoading] = useState(false);

  const MAX_SIZE = 20 * 1024 * 1024; // 20 MB

  // ===========================================
  // File Selection
  // ===========================================

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["xlsx", "xls"].includes(extension)) {
      alert("Please select a valid Excel file (.xlsx or .xls)");
      return;
    }

    if (file.size > MAX_SIZE) {
      alert("File size should be less than 20 MB.");
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setPreview([]);
  };

  // ===========================================
  // Reset
  // ===========================================

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setPreview([]);
  };

  // ===========================================
  // Upload Excel
  // ===========================================

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please choose an Excel file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);

      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log("Upload Result:", data);

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setResult(data);
      setPreview(data.preview || []);

      // ===========================================
      // Refresh Dashboard Automatically
      // ===========================================

      if (refreshDashboard) {
        await refreshDashboard();
      }

    } catch (error) {
      console.error(error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Paper
        elevation={5}
        sx={{
          p: 4,
          mt: 5,
          borderRadius: 3,
        }}
      >
        <Typography
          variant="h5"
          fontWeight="bold"
          gutterBottom
        >
          📂 Upload SAP PM Excel File
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ mb: 2 }}
        >
          Supported Formats: .xlsx / .xls
        </Typography>

        <Divider sx={{ mb: 3 }} />

        <Stack spacing={2}>

          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
          />

          {selectedFile && (
            <Chip
              color="primary"
              icon={<UploadFileIcon />}
              label={`${selectedFile.name} (${(
                selectedFile.size /
                1024 /
                1024
              ).toFixed(2)} MB)`}
            />
          )}

          <Box display="flex" gap={2}>

            <Button
              variant="contained"
              size="large"
              disabled={loading}
              onClick={handleUpload}
            >
              {loading ? (
                <>
                  <CircularProgress
                    size={20}
                    sx={{
                      mr: 1,
                      color: "white",
                    }}
                  />
                  Uploading...
                </>
              ) : (
                "Upload Excel"
              )}
            </Button>

            <Button
              variant="outlined"
              color="secondary"
              startIcon={<RestartAltIcon />}
              onClick={handleReset}
              disabled={loading}
            >
              Reset
            </Button>

          </Box>

        </Stack>

        {result && (
          <Alert
            severity="success"
            sx={{ mt: 4 }}
          >
            <Typography>
              <strong>Filename:</strong>{" "}
              {result.filename || selectedFile?.name}
            </Typography>

            <Typography>
              <strong>Total Rows:</strong> {result.rows}
            </Typography>

            <Typography>
              <strong>Total Columns:</strong>{" "}
              {result.columns.length}
            </Typography>

            <Typography sx={{ mt: 1 }}>
              <strong>Column Names:</strong>
            </Typography>

            <Typography variant="body2">
              {result.columns.join(", ")}
            </Typography>

            <Typography
              variant="caption"
              display="block"
              sx={{ mt: 2 }}
            >
              Uploaded Successfully at{" "}
              {new Date().toLocaleString()}
            </Typography>
          </Alert>
        )}

      </Paper>

      <DataPreview data={preview} />

    </>
  );
}