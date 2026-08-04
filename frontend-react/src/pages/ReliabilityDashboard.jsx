import { useEffect, useState, useCallback } from "react";
import { Box, Grid, Typography, CircularProgress, Button, Tooltip } from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import RefreshIcon from "@mui/icons-material/Refresh";

import FilterBar from "../components/FilterBar";
import DrillDownDialog from "../components/DrillDownDialog";
import MTTRCard from "../components/MTTRCard";
import MTBFCard from "../components/MTBFCard";
import PMComplianceCard from "../components/PMComplianceCard";
import BreakdownCard from "../components/BreakdownCard";
import EquipmentHealthGauge from "../components/EquipmentHealthGauge";
import TopFailureTable from "../components/TopFailureTable";
import BacklogChart from "../components/BacklogChart";
import WorkOrderAgeChart from "../components/WorkOrderAgeChart";

const API = "http://127.0.0.1:8000";

function buildQuery(filters) {
  const params = new URLSearchParams(filters);
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export default function ReliabilityDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});
  const [drillEquipment, setDrillEquipment] = useState(null);

  const load = useCallback((activeFilters = {}) => {
    setLoading(true);
    fetch(`${API}/analytics/dashboard${buildQuery(activeFilters)}`)
      .then((r) => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleFilter = (f) => { setFilters(f); load(f); };
  const handleClear  = ()  => { setFilters({}); load({}); };

  const handleExport = () => {
    const url = `${API}/analytics/export${buildQuery(filters)}`;
    window.open(url, "_blank");
  };

  if (loading && !data) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 10 }}>
        <CircularProgress />
      </Box>
    );
  }

  const mttr       = data?.mttr ?? {};
  const mtbf       = data?.mtbf ?? {};
  const compliance = data?.pm_compliance ?? {};
  const breakdown  = data?.breakdown_percentage ?? {};
  const backlog    = data?.backlog ?? {};
  const age        = data?.work_order_age ?? {};
  const health     = data?.health_scores ?? [];
  const failures   = data?.top_failures ?? [];

  // Merge health scores into failure rows
  const enrichedFailures = failures.map((f) => {
    const h = health.find((r) => r.equipment === f.equipment);
    return { ...f, health_score: h?.health_score, risk: h?.risk };
  });

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 1 }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">Reliability Analytics</Typography>
          <Typography variant="body2" color="text.secondary">
            SAP PM / EAM metrics — upload an Excel file to see live data
          </Typography>
        </Box>
        <Box sx={{ display: "flex", gap: 1 }}>
          <Tooltip title="Refresh data">
            <Button variant="outlined" size="small" startIcon={<RefreshIcon />} onClick={() => load(filters)}>
              Refresh
            </Button>
          </Tooltip>
          <Button variant="contained" size="small" startIcon={<DownloadIcon />} onClick={handleExport}>
            Export Excel
          </Button>
        </Box>
      </Box>

      {/* Filters */}
      <FilterBar onFilter={handleFilter} onClear={handleClear} />

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MTTRCard value={mttr.mttr_days} sampleSize={mttr.sample_size} source={mttr.source} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MTBFCard value={mtbf.mtbf_days} sampleSize={mtbf.sample_size} source={mtbf.source} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <PMComplianceCard
            compliancePct={compliance.compliance_pct}
            completed={compliance.completed}
            total={compliance.total}
            source={compliance.source}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <BreakdownCard
            breakdownPct={breakdown.breakdown_pct}
            breakdownCount={breakdown.breakdown_count}
            total={breakdown.total}
            source={breakdown.source}
          />
        </Grid>
      </Grid>

      {/* Equipment Health */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12}>
          <EquipmentHealthGauge data={health} onBarClick={(eq) => setDrillEquipment(eq)} />
        </Grid>
      </Grid>

      {/* Top Failures + Backlog */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <TopFailureTable
            data={enrichedFailures.slice(0, 10)}
            onRowClick={(eq) => setDrillEquipment(eq)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <BacklogChart data={backlog.by_plant ?? []} />
        </Grid>
      </Grid>

      {/* Work Order Age */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <WorkOrderAgeChart
            buckets={age.buckets ?? []}
            avgDays={age.avg_age_days}
            maxDays={age.max_age_days}
          />
        </Grid>
      </Grid>

      {/* Drill-down Dialog */}
      <DrillDownDialog
        equipment={drillEquipment}
        onClose={() => setDrillEquipment(null)}
      />
    </Box>
  );
}
