import { useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import { useAuth } from "./context/AuthContext";

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

import WorkOrderChart from "./charts/WorkOrderChart";
import PriorityPieChart from "./charts/PriorityPieChart";
import StatusBarChart from "./charts/StatusBarChart";
import PlantChart from "./charts/PlantChart";

import {
  Container,
  Grid,
  Typography,
  Paper,
  Divider,
} from "@mui/material";

function App() {

  const { user } = useAuth();

  if (!user) return <LoginPage />;

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

        </Routes>

      </Container>

    </>

  );

}

export default App;