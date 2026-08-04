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