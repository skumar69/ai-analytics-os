import { useState } from "react";
import {
  Box, Card, CardContent, TextField, Button,
  Typography, Alert, CircularProgress, InputAdornment, IconButton,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import { useAuth } from "../context/AuthContext";

const DEMO_USERS = [
  { label: "Admin",      user: "admin",      pass: "admin123" },
  { label: "Manager",    user: "manager",    pass: "manager123" },
  { label: "Planner",    user: "planner",    pass: "planner123" },
  { label: "Executive",  user: "executive",  pass: "exec123" },
  { label: "Technician", user: "technician", pass: "tech123" },
];

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (u, p) => { setUsername(u); setPassword(p); };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)",
      }}
    >
      <Card elevation={12} sx={{ width: 420, borderRadius: 4 }}>
        <CardContent sx={{ p: 4 }}>
          {/* Logo / Title */}
          <Box sx={{ textAlign: "center", mb: 3 }}>
            <Typography variant="h4" fontWeight="bold" color="primary">
              VisionIQ
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Enterprise Asset Intelligence Platform
            </Typography>
          </Box>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <form onSubmit={handleLogin}>
            <TextField
              fullWidth label="Username" value={username} autoFocus
              onChange={(e) => setUsername(e.target.value)}
              sx={{ mb: 2 }} size="small"
            />
            <TextField
              fullWidth label="Password" value={password}
              type={showPass ? "text" : "password"}
              onChange={(e) => setPassword(e.target.value)}
              size="small" sx={{ mb: 3 }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton size="small" onClick={() => setShowPass((v) => !v)}>
                      {showPass ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <Button
              fullWidth variant="contained" type="submit" size="large"
              disabled={loading || !username || !password}
              sx={{ borderRadius: 2, py: 1.2 }}
            >
              {loading ? <CircularProgress size={22} color="inherit" /> : "Sign In"}
            </Button>
          </form>

          {/* Demo quick-fill buttons */}
          <Box sx={{ mt: 3 }}>
            <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
              Demo accounts:
            </Typography>
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.8 }}>
              {DEMO_USERS.map(({ label, user, pass }) => (
                <Button
                  key={label} size="small" variant="outlined"
                  onClick={() => fillDemo(user, pass)}
                  sx={{ fontSize: 11, px: 1.2, py: 0.4 }}
                >
                  {label}
                </Button>
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
