// ==========================================
// VisionIQ API Configuration
// ==========================================

const API = import.meta.env.VITE_API_URL;

if (!API) {
  throw new Error(
    "VITE_API_URL is not defined. Please check your .env file."
  );
}

// ==========================================
// Dashboard APIs
// ==========================================

export async function getStats() {
  const res = await fetch(`${API}/stats`);

  if (!res.ok) {
    throw new Error("Failed to load dashboard statistics");
  }

  return await res.json();
}

export async function getTrend() {
  const res = await fetch(`${API}/workorder-trend`);

  if (!res.ok) {
    throw new Error("Failed to load work order trend");
  }

  return await res.json();
}

export async function getPriority() {
  const res = await fetch(`${API}/priority-distribution`);

  if (!res.ok) {
    throw new Error("Failed to load priority distribution");
  }

  return await res.json();
}

export async function getStatus() {
  const res = await fetch(`${API}/status-distribution`);

  if (!res.ok) {
    throw new Error("Failed to load status distribution");
  }

  return await res.json();
}

export async function getPlant() {
  const res = await fetch(`${API}/plant-distribution`);

  if (!res.ok) {
    throw new Error("Failed to load plant distribution");
  }

  return await res.json();
}

// ==========================================
// Export Base URL
// ==========================================

export default API;