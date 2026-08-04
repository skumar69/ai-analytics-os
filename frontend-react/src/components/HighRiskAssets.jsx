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
} from "@mui/material";

export default function HighRiskAssets() {

  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/high-risk-assets"
      );

      const data = await response.json();

      setAssets(data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

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

            <TableRow key={index}>

              <TableCell>{row.equipment}</TableCell>

              <TableCell>{row.plant}</TableCell>

              <TableCell>

                <Chip
                  label={row.priority}
                  color={
                    row.priority === "Critical"
                      ? "error"
                      : row.priority === "High"
                      ? "warning"
                      : "primary"
                  }
                />

              </TableCell>

              <TableCell>{row.health}%</TableCell>

              <TableCell>{row.status}</TableCell>

            </TableRow>

          ))}

        </TableBody>

      </Table>

    </Paper>

  );

}