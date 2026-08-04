import { DataGrid } from "@mui/x-data-grid";

import {
  Paper,
  Typography,
} from "@mui/material";

export default function DataPreview({ data }) {

  if (!data || data.length === 0) return null;

  const columns = Object.keys(data[0]).map((key) => ({
    field: key,
    headerName: key,
    flex: 1,
    minWidth: 170,
  }));

  const rows = data.map((row, index) => ({
    id: index + 1,
    ...row,
  }));

  return (
    <Paper
      elevation={4}
      sx={{
        mt: 4,
        p: 3,
        borderRadius: 3,
      }}
    >
      <Typography
        variant="h5"
        gutterBottom
      >
        📋 SAP Data Preview
      </Typography>

      <div style={{ height: 500, width: "100%" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSizeOptions={[5,10,20,50,100]}
          initialState={{
            pagination:{
              paginationModel:{
                pageSize:10,
              },
            },
          }}
        />
      </div>

    </Paper>
  );
}