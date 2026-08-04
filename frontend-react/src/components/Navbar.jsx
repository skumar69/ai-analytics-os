import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";

function Navbar() {
  return (
    <AppBar position="static" sx={{ bgcolor: "#111827" }}>
      <Toolbar>
        <DashboardIcon sx={{ mr: 2 }} />

        <Typography variant="h5" sx={{ flexGrow: 1 }}>
          AI Analytics OS
        </Typography>

        <Button color="inherit">Dashboard</Button>
        <Button color="inherit">SAP PM</Button>
        <Button color="inherit">Analytics</Button>
        <Button color="inherit">AI</Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;