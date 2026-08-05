import { useEffect, useState, useCallback } from "react";
import {
  Box, Grid, Typography, CircularProgress, Button,
  Tooltip, Paper, Chip,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import FiberManualRecordIcon from "@mui/icons-material/FiberManualRecord";
import API from "../services/api";
import AssetHealthCard from "../components/AssetHealthCard";
import BacklogChart from "../components/BacklogChart";
import MTTRTrendChart from "../components/MTTRTrendChart";
import PlannerPerformanceTable from "../components/PlannerPerformanceTable";
import RepeatFailureTable from "../components/RepeatFailureTable";
import FilterBar from "../components/FilterBar";

//const API = "http://127.0.0.1:8000";

function buildQuery(filters) {
  const qs = new URLSearchParams(filters).toString();
  return qs ? `?${qs}` : "";
}

function FleetHealthBadge({ avg, red, amber, green }) {
  const color = avg >= 70 ? "success" : avg >= 50 ? "warning" : "error";
  return (
    <Paper elevation={3} sx={{ p: 2.5, borderRadius: 3, textAlign: "center" }}>
      <Typography variant="subtitle2" color="text.secondary">Fleet Health Score</Typography>
      <Typography variant="h3" fontWeight="bold" color={`${color}.main`}>
        {avg ?? "—"}
      </Typography>
      <Box sx={{ display: "flex", justifyContent: "center", gap: 2, mt: 1 }}>
        {[["Red", red, "#d32f2f"], ["Amber", amber, "#ed6c02"], ["Green", green, "#2e7d32"]].map(([label, count, hex]) => (
          <Box key={label} sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
            <FiberManualRecordIcon sx={{ color: hex, fontSize: 14 }} />
            <Typography variant="caption">{label}: <strong>{count}</strong></Typography>
          </Box>
        ))}
      </Box>
    </Paper>
  );
}

function SLACard({ sla }) {
  if (!sla) return null;
  const pct = sla.overdue_count + sla.on_time_count > 0
    ? Math.round((sla.overdue_count / (sla.overdue_count + sla.on_time_count)) * 100)
    : 0;
  const color = pct > 30 ? "error" : pct > 15 ? "warning" : "success";
  return (
    <Paper elevation={3} sx={{ p: 2.5, borderRadius: 3 }}>
      <Typography variant="subtitle2" color="text.secondary">Work Orders &gt; {sla.sla_days}d SLA</Typography>
      <Typography variant="h4" fontWeight="bold" color={`${color}.main`}>{sla.overdue_count}</Typography>
      <Typography variant="caption" color="text.secondary">
        {pct}% overdue · {sla.on_time_count} on time
      </Typography>
    </Paper>
  );
}

export default function ExecutiveDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});

  const load = useCallback((activeFilters = {}) => {
    setLoading(true);
    fetch(`${API}/sap/intelligence-summary${buildQuery(activeFilters)}`)
      .then((r) => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleFilter = (f) => { setFilters(f); load(f); };
  const handleClear  = ()  => { setFilters({}); load({}); };

  if (loading && !data) {
    return <Box sx={{ display: "flex", justifyContent: "center", mt: 10 }}><CircularProgress /></Box>;
  }

  const health      = data?.asset_health ?? [];
  const pmByPlant   = data?.pm_by_plant ?? [];
  const mttrTrend   = data?.mttr_trend ?? [];
  const planners    = data?.planner_performance ?? [];
  const repeatFails = data?.repeat_failures ?? [];
  const sla         = data?.work_order_sla;

  // Show worst 12 assets by health score
  const worstAssets = [...health].slice(0, 12);

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 1 }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">Executive Dashboard</Typography>
          <Typography variant="body2" color="text.secondary">
            Enterprise Asset Intelligence — Plant Leadership View
          </Typography>
        </Box>
        <Tooltip title="Refresh">
          <Button variant="outlined" size="small" startIcon={<RefreshIcon />} onClick={() => load(filters)}>
            Refresh
          </Button>
        </Tooltip>
      </Box>

      <FilterBar onFilter={handleFilter} onClear={handleClear} />

      {/* Fleet summary row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={4}>
          <FleetHealthBadge
            avg={data?.fleet_health_avg}
            red={data?.red_count}
            amber={data?.amber_count}
            green={data?.green_count}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <SLACard sla={sla} />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper elevation={3} sx={{ p: 2.5, borderRadius: 3 }}>
            <Typography variant="subtitle2" color="text.secondary">PM Compliance (worst plant)</Typography>
            {pmByPlant.length > 0 ? (
              <>
                <Typography variant="h4" fontWeight="bold" color="warning.main">
                  {pmByPlant[0].compliance_pct}%
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Plant {pmByPlant[0].plant} · {pmByPlant[0].completed}/{pmByPlant[0].total} orders
                </Typography>
              </>
            ) : (
              <Typography color="text.secondary">No data</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Asset Health Grid */}
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 1.5 }}>
        Equipment Health Scores
        <Chip
          label={`${data?.red_count ?? 0} Critical`}
          color="error" size="small" sx={{ ml: 1 }}
        />
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {worstAssets.map((asset) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={asset.equipment}>
            <AssetHealthCard
              equipment={asset.equipment}
              healthScore={asset.health_score}
              riskLevel={asset.risk_level}
              details={asset.details}
            />
          </Grid>
        ))}
        {worstAssets.length === 0 && (
          <Grid item xs={12}>
            <Typography color="text.secondary">Upload SAP data to see equipment health.</Typography>
          </Grid>
        )}
      </Grid>

      {/* MTTR Trend + Backlog by Plant */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <MTTRTrendChart data={mttrTrend} target={3} />
        </Grid>
        <Grid item xs={12} md={6}>
          <BacklogChart data={pmByPlant.map((r) => ({ plant: r.plant, count: r.total - r.completed }))} />
        </Grid>
      </Grid>

      {/* Planner Performance + Repeat Failures */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <PlannerPerformanceTable data={planners} />
        </Grid>
        <Grid item xs={12} md={6}>
          <RepeatFailureTable data={repeatFails} />
        </Grid>
      </Grid>
    </Box>
  );
}
