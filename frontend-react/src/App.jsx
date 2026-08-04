import { useEffect, useState, Component } from "react";
import { Routes, Route } from "react-router-dom";
import { Box, Typography, Button, Container, Grid, Paper, Divider } from "@mui/material";
import { useAuth } from "./context/AuthContext";

// Catches render errors so the app never goes completely blank
class ErrorBoundary extends Component {
  state = { hasError: false, error: null };
  static getDerivedStateFromError(error) { return { hasError: true, error }; }
  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 4, textAlign: "center", mt: 8 }}>
          <Typography variant="h5" color="error" gutterBottom>Something went wrong</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {this.state.error?.message}
          </Typography>
          <Button variant="contained" onClick={() => window.location.reload()}>Reload</Button>
        </Box>
      );
    }
    return this.props.children;
  }
}

import LoginPage from "./pages/LoginPage";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import DashboardHeader from "./components/DashboardHeader";
import KPISection from "./components/KPISection";
import FileUpload from "./components/FileUpload";
import AIInsights from "./components/AIInsights";
import HighRiskAssets from "./components/HighRiskAssets";
import NotificationTable from "./components/NotificationTable";
import ReliabilityDashboard from "./pages/ReliabilityDashboard";
import ExecutiveDashboard from "./pages/ExecutiveDashboard";
import AICopilot from "./pages/AICopilot";

import WorkOrderChart from "./charts/WorkOrderChart";
import PriorityPieChart from "./charts/PriorityPieChart";
import StatusBarChart from "./charts/StatusBarChart";
import PlantChart from "./charts/PlantChart";


// AuthGate renders LoginPage or App — hooks live in App so they're always called
function AuthGate() {
  const { user } = useAuth();
  if (!user) return <LoginPage />;
  return <ErrorBoundary><AppShell /></ErrorBoundary>;
}

function AppShell() {

  const [stats, setStats] = useState({
    work_orders: 0,
    notifications: 0,
    equipment: 0,
    plants: 0,
    asset_health: 0,
    ai_score: 96,
  });

  // ======================================================
  // Load Dashboard KPIs
  // ======================================================

  const fetchDashboard = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/stats"
      );

      if (!response.ok) {
        throw new Error("Unable to load dashboard");
      }

      const data = await response.json();

      console.log("Dashboard:", data);

      setStats((prev) => ({
        ...prev,
        ...data,
      }));

    } catch (err) {

      console.error(err);

    }

  };

  useEffect(() => {

    fetchDashboard();

  }, []);

  return (

    <>

      <Navbar />

      <Sidebar />

      <Container
        maxWidth="xl"
        sx={{
          ml: { xs: 0, md: "240px" },
          mt: "90px",
          mb: 8,
        }}
      >

        <Routes>

          {/* Main Dashboard */}
          <Route path="/" element={
            <>
              <DashboardHeader />
              <KPISection stats={stats} />

              <Paper elevation={4} sx={{ mt: 5, p: 3, borderRadius: 3 }}>
                <Typography variant="h5" fontWeight="bold">
                  📈 Monthly Work Order Trend
                </Typography>
                <Divider sx={{ my: 2 }} />
                <WorkOrderChart />
              </Paper>

              <Typography variant="h5" fontWeight="bold" sx={{ mt: 5, mb: 2 }}>
                📊 Incident Analytics
              </Typography>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}><PriorityPieChart /></Grid>
                <Grid item xs={12} md={6}><StatusBarChart /></Grid>
                <Grid item xs={12} md={6}><PlantChart /></Grid>
                <Grid item xs={12} md={6}><AIInsights /></Grid>
              </Grid>

              <HighRiskAssets />
              <NotificationTable />

              <Paper elevation={4} sx={{ mt: 5, p: 3, borderRadius: 3 }}>
                <Typography variant="h5" fontWeight="bold">
                  📂 Upload SAP Excel File
                </Typography>
                <Divider sx={{ my: 2 }} />
                <FileUpload refreshDashboard={fetchDashboard} />
              </Paper>
            </>
          } />

          {/* Reliability Analytics */}
          <Route path="/reliability" element={<ReliabilityDashboard />} />

          {/* Executive Dashboard */}
          <Route path="/executive" element={<ExecutiveDashboard />} />

          {/* AI Copilot */}
          <Route path="/ai" element={<AICopilot />} />

        </Routes>

      </Container>

    </>

  );

}

function App() {
  return <AuthGate />;
}

export default App;