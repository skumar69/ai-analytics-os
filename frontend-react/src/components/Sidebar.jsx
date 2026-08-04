import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import BuildIcon from "@mui/icons-material/Build";
import AnalyticsIcon from "@mui/icons-material/Analytics";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SettingsIcon from "@mui/icons-material/Settings";

const drawerWidth = 220;

const menuItems = [
  { text: "Dashboard", icon: <DashboardIcon /> },
  { text: "SAP PM", icon: <BuildIcon /> },
  { text: "Analytics", icon: <AnalyticsIcon /> },
  { text: "AI Assistant", icon: <SmartToyIcon /> },
  { text: "Settings", icon: <SettingsIcon /> },
];

export default function Sidebar() {
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
          <ListItemButton key={item.text}>
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