import { useNavigate, useLocation } from "react-router-dom";
import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import EngineeringIcon from "@mui/icons-material/Engineering";
import AnalyticsIcon from "@mui/icons-material/Analytics";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SettingsIcon from "@mui/icons-material/Settings";
import LeaderboardIcon from "@mui/icons-material/Leaderboard";

const drawerWidth = 220;

const menuItems = [
  { text: "Dashboard",             icon: <DashboardIcon />,   path: "/" },
  { text: "Reliability Analytics", icon: <EngineeringIcon />, path: "/reliability" },
  { text: "Executive Dashboard",   icon: <LeaderboardIcon />, path: "/executive" },
  { text: "AI Assistant",          icon: <SmartToyIcon />,    path: "/ai" },
  { text: "Analytics",             icon: <AnalyticsIcon />,   path: "/analytics" },
  { text: "Settings",              icon: <SettingsIcon />,    path: "/settings" },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          background: "#111827",
          color: "white",
        },
      }}
    >
      <List sx={{ marginTop: "70px" }}>
        {menuItems.map((item) => (
          <ListItemButton
            key={item.text}
            selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}
            sx={{
              "&.Mui-selected": {
                background: "rgba(255,255,255,0.12)",
                borderLeft: "3px solid #1976d2",
              },
              "&:hover": { background: "rgba(255,255,255,0.08)" },
            }}
          >
            <ListItemIcon sx={{ color: "white" }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}