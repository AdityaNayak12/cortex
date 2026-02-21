const API_BASE = "http://localhost:8000/api";
const USER_ID = 1; // TODO: load from user auth

async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

document.getElementById("btn-load-insights").addEventListener("click", async () => {
    const el = document.getElementById("insights-output");
    el.textContent = "Loading…";
    try {
        const data = await fetchJSON(`${API_BASE}/analyze/${USER_ID}`);
        el.textContent = data.insights;
    } catch (err) {
        el.textContent = `Error: ${err.message}`;
    }
});

document.getElementById("btn-load-plan").addEventListener("click", async () => {
    const el = document.getElementById("plan-output");
    el.textContent = "Loading…";
    try {
        const data = await fetchJSON(`${API_BASE}/plan/${USER_ID}`);
        el.textContent = data.plan;
    } catch (err) {
        el.textContent = `Error: ${err.message}`;
    }
});
