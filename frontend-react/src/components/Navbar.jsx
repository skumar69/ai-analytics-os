import { AppBar, Toolbar, Typography, Box, Chip, Button, Tooltip } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import LogoutIcon from "@mui/icons-material/Logout";
import { useAuth } from "../context/AuthContext";

const ROLE_COLOR = {
  Admin: "error", Manager: "primary", Planner: "success",
  Executive: "secondary", Technician: "warning",
};

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <AppBar position="fixed" sx={{ bgcolor: "#111827", zIndex: 1300 }}>
      <Toolbar>
        <DashboardIcon sx={{ mr: 1.5 }} />
        <Typography variant="h6" fontWeight="bold" sx={{ flexGrow: 1 }}>
          VisionIQ
        </Typography>

        {user && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
            <Chip
              label={`${user.full_name} · ${user.role}`}
              color={ROLE_COLOR[user.role] ?? "default"}
              size="small"
              sx={{ color: "white", fontWeight: 600 }}
            />
            <Tooltip title="Sign out">
              <Button color="inherit" size="small" startIcon={<LogoutIcon />} onClick={logout}>
                Logout
              </Button>
            </Tooltip>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;