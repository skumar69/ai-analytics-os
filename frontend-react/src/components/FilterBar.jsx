import { useEffect, useState } from "react";

import {
  Box,
  Grid,
  TextField,
  MenuItem,
  Button,
  Tooltip,
} from "@mui/material";

import FilterListIcon from "@mui/icons-material/FilterList";
import ClearIcon from "@mui/icons-material/Clear";

import API from "../services/api";

const EMPTY = {
  plant: "",
  priority: "",
  status: "",
  planner_group: "",
  date_from: "",
  date_to: "",
};

export default function FilterBar({ onFilter, onClear }) {
  const [options, setOptions] = useState({
    plants: [],
    priorities: [],
    statuses: [],
    planner_groups: [],
  });

  const [filters, setFilters] = useState(EMPTY);

  useEffect(() => {
    loadFilterOptions();
  }, []);

  const loadFilterOptions = async () => {
    try {
      const response = await fetch(`${API}/analytics/filter-options`);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();

      setOptions({
        plants: data.plants || [],
        priorities: data.priorities || [],
        statuses: data.statuses || [],
        planner_groups: data.planner_groups || [],
      });
    } catch (error) {
      console.error("Filter Options Error:", error);

      setOptions({
        plants: [],
        priorities: [],
        statuses: [],
        planner_groups: [],
      });
    }
  };

  const handleChange = (key) => (event) => {
    setFilters((prev) => ({
      ...prev,
      [key]: event.target.value,
    }));
  };

  const apply = () => {
    const activeFilters = Object.fromEntries(
      Object.entries(filters).filter(([, value]) => value !== "")
    );

    onFilter(activeFilters);
  };

  const clear = () => {
    setFilters(EMPTY);

    if (onClear) {
      onClear();
    }
  };

  return (
    <Box
      sx={{
        p: 2,
        mb: 3,
        borderRadius: 2,
        background: "rgba(25,118,210,0.06)",
        border: "1px solid rgba(25,118,210,0.20)",
      }}
    >
      <Grid container spacing={2} alignItems="center">
        {[
          {
            key: "plant",
            label: "Plant",
            options: options.plants,
          },
          {
            key: "priority",
            label: "Priority",
            options: options.priorities,
          },
          {
            key: "status",
            label: "Status",
            options: options.statuses,
          },
          {
            key: "planner_group",
            label: "Planner Group",
            options: options.planner_groups,
          },
        ].map(({ key, label, options }) => (
          <Grid item xs={6} sm={3} md={2} key={key}>
            <TextField
              select
              fullWidth
              size="small"
              label={label}
              value={filters[key]}
              onChange={handleChange(key)}
            >
              <MenuItem value="">All</MenuItem>

              {options.map((item) => (
                <MenuItem key={item} value={item}>
                  {item}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
        ))}

        <Grid item xs={6} sm={3} md={2}>
          <TextField
            fullWidth
            size="small"
            type="date"
            label="From"
            InputLabelProps={{ shrink: true }}
            value={filters.date_from}
            onChange={handleChange("date_from")}
          />
        </Grid>

        <Grid item xs={6} sm={3} md={2}>
          <TextField
            fullWidth
            size="small"
            type="date"
            label="To"
            InputLabelProps={{ shrink: true }}
            value={filters.date_to}
            onChange={handleChange("date_to")}
          />
        </Grid>

        <Grid item xs={12} sm="auto">
          <Box sx={{ display: "flex", gap: 1 }}>
            <Button
              variant="contained"
              size="small"
              startIcon={<FilterListIcon />}
              onClick={apply}
            >
              Apply
            </Button>

            <Tooltip title="Clear all filters">
              <Button
                variant="outlined"
                size="small"
                startIcon={<ClearIcon />}
                onClick={clear}
              >
                Clear
              </Button>
            </Tooltip>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}