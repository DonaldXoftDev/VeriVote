async function checkApiHealth() {
  const badge = document.getElementById("api-status-badge");
  if (!badge) return;

  try {
    const response = await fetch("/api/v1/health");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    badge.innerHTML = `
      <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
      API ${data.status.toUpperCase()} · DB: ${data.database}
    `;
    badge.classList.remove("text-slate-300");
    badge.classList.add("text-emerald-300", "border", "border-emerald-500/30");
  } catch (err) {
    badge.innerHTML = `
      <span class="h-2 w-2 rounded-full bg-rose-400"></span>
      API Offline
    `;
    badge.classList.add("text-rose-300");
  }
}

document.addEventListener("DOMContentLoaded", checkApiHealth);
