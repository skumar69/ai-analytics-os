import { useEffect, useState } from "react";
import {
  Box, Grid, TextField, MenuItem, Button, Tooltip,
} from "@mui/material";
import FilterListIcon from "@mui/icons-material/FilterList";
import ClearIcon from "@mui/icons-material/Clear";

const EMPTY = { plant: "", priority: "", status: "", planner_group: "", date_from: "", date_to: "" };

export default function FilterBar({ onFilter, onClear }) {
  const [options, setOptions] = useState({ plants: [], priorities: [], statuses: [], planner_groups: [] });
  const [filters, setFilters] = useState(EMPTY);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/filter-options")
      .then((r) => r.json())
      .then((d) => setOptions(d))
      .catch(() => {});
  }, []);

  const set = (key) => (e) => setFilters((f) => ({ ...f, [key]: e.target.value }));

  const apply = () => {
    const active = Object.fromEntries(Object.entries(filters).filter(([, v]) => v !== ""));
    onFilter(active);
  };

  const clear = () => {
    setFilters(EMPTY);
    onClear();
  };

  return (
    <Box
      sx={{
        p: 2, mb: 3, borderRadius: 2,
        background: "rgba(25, 118, 210, 0.06)",
        border: "1px solid rgba(25, 118, 210, 0.2)",
      }}
    >
      <Grid container spacing={2} alignItems="center">
        {[
          { key: "plant",         label: "Plant",          opts: options.plants ?? [] },
          { key: "priority",      label: "Priority",       opts: options.priorities ?? [] },
          { key: "status",        label: "Status",         opts: options.statuses ?? [] },
          { key: "planner_group", label: "Planner Group",  opts: options.planner_groups ?? [] },
        ].map(({ key, label, opts }) => (
          <Grid item xs={6} sm={3} md={2} key={key}>
            <TextField
              select size="small" fullWidth
              label={label} value={filters[key]}
              onChange={set(key)}
            >
              <MenuItem value="">All</MenuItem>
              {opts.filter(Boolean).map((o) => (
                <MenuItem key={o} value={o}>{o}</MenuItem>
              ))}
            </TextField>
          </Grid>
        ))}

        <Grid item xs={6} sm={3} md={2}>
          <TextField
            size="small" fullWidth type="date" label="From"
            InputLabelProps={{ shrink: true }}
            value={filters.date_from} onChange={set("date_from")}
          />
        </Grid>

        <Grid item xs={6} sm={3} md={2}>
          <TextField
            size="small" fullWidth type="date" label="To"
            InputLabelProps={{ shrink: true }}
            value={filters.date_to} onChange={set("date_to")}
          />
        </Grid>

        <Grid item xs={12} sm="auto">
          <Box sx={{ display: "flex", gap: 1 }}>
            <Button variant="contained" size="small" startIcon={<FilterListIcon />} onClick={apply}>
              Apply
            </Button>
            <Tooltip title="Clear all filters">
              <Button variant="outlined" size="small" startIcon={<ClearIcon />} onClick={clear}>
                Clear
              </Button>
            </Tooltip>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}
