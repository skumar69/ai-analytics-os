const API = "http://127.0.0.1:8000";

export async function getStats() {
  const res = await fetch(`${API}/stats`);
  return res.json();
}

export async function getTrend() {
  const res = await fetch(`${API}/workorder-trend`);
  return res.json();
}

export async function getPriorityChart() {
  const res = await fetch(`${API}/priority-chart`);
  return res.json();
}

export async function getStatusChart() {
  const res = await fetch(`${API}/status-chart`);
  return res.json();
}

export async function getPlantChart() {
  const res = await fetch(`${API}/plant-chart`);
  return res.json();
}

export async function getAIInsights() {
  const res = await fetch(`${API}/ai-insights`);
  return res.json();
}

export async function getAssets() {
  const res = await fetch(`${API}/high-risk-assets`);
  return res.json();
}

export async function getNotifications() {
  const res = await fetch(`${API}/notifications`);
  return res.json();
}

export async function uploadExcel(formData) {
  const res = await fetch(`${API}/upload`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}

export async function getAnalyticsSummary() {
  const res = await fetch(`${API}/analytics/summary`);
  return res.json();
}

export async function getMTTR() {
  const res = await fetch(`${API}/analytics/mttr`);
  return res.json();
}

export async function getMTBF() {
  const res = await fetch(`${API}/analytics/mtbf`);
  return res.json();
}

export async function getPMCompliance() {
  const res = await fetch(`${API}/analytics/pm-compliance`);
  return res.json();
}

export async function getBreakdownPercentage() {
  const res = await fetch(`${API}/analytics/breakdown-percentage`);
  return res.json();
}

export async function getBacklog() {
  const res = await fetch(`${API}/analytics/backlog`);
  return res.json();
}

export async function getWorkOrderAge() {
  const res = await fetch(`${API}/analytics/work-order-age`);
  return res.json();
}

export async function getHealthScore() {
  const res = await fetch(`${API}/analytics/health-score`);
  return res.json();
}

export async function getTopFailures() {
  const res = await fetch(`${API}/analytics/top-failures`);
  return res.json();
}

export async function getAssetCriticality() {
  const res = await fetch(`${API}/analytics/asset-criticality`);
  return res.json();
}