import { createTheme } from "@mui/material/styles";

const BRAND = {
  primary:   "#1976d2",
  secondary: "#7c3aed",
  success:   "#2e7d32",
  warning:   "#ed6c02",
  error:     "#d32f2f",
  navy:      "#0f172a",
  surface:   "#1e293b",
  border:    "#334155",
};

const theme = createTheme({
  palette: {
    mode: "dark",
    primary:   { main: BRAND.primary },
    secondary: { main: BRAND.secondary },
    success:   { main: BRAND.success },
    warning:   { main: BRAND.warning },
    error:     { main: BRAND.error },
    background: {
      default: BRAND.navy,
      paper:   "#1a2744",
    },
    text: {
      primary:   "#f1f5f9",
      secondary: "#94a3b8",
    },
    divider: BRAND.border,
  },
  typography: {
    fontFamily: '"Inter", "Segoe UI", Arial, sans-serif',
    h5: { fontWeight: 700 },
    h6: { fontWeight: 600 },
    subtitle2: { fontWeight: 600 },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          border: `1px solid ${BRAND.border}`,
          transition: "box-shadow 0.2s",
          "&:hover": { boxShadow: "0 4px 20px rgba(0,0,0,0.35)" },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          border: `1px solid ${BRAND.border}`,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { textTransform: "none", fontWeight: 600 },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600 },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: { fontWeight: 700, color: "#94a3b8" },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: BRAND.navy,
          borderRight: `1px solid ${BRAND.border}`,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: BRAND.navy,
          borderBottom: `1px solid ${BRAND.border}`,
          boxShadow: "none",
        },
      },
    },
  },
});

export default theme;
