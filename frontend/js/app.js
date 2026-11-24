async function checkApiHealth() {
  const badge = document.getElementById("api-status-badge");
  if (!badge) return;

  try {
    const response = await fetch("/api/v1/health");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    badge.className =
      "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/80";
    badge.innerHTML = `
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
      API ${data.status.toUpperCase()} · DB: ${data.database}
    `;
  } catch (_err) {
    badge.className =
      "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-red-50 text-red-700 border border-red-200/80";
    badge.innerHTML = `
      <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
      API Offline
    `;
  }
}

document.addEventListener("DOMContentLoaded", checkApiHealth);
