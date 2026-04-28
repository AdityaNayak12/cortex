const API_BASE = "http://127.0.0.1:8000/api";

const userIdInput = document.getElementById("user-id-input");
const saveBtn = document.getElementById("btn-save-id");
const idStatus = document.getElementById("id-status");

// Load saved user ID on page load
const savedId = localStorage.getItem("cortex_user_id");
if (savedId) {
    userIdInput.value = savedId;
    idStatus.textContent = "✓ Saved";
    idStatus.className = "id-status success";
}

// Save user ID to localStorage
saveBtn.addEventListener("click", () => {
    const id = userIdInput.value.trim();
    if (!id) {
        idStatus.textContent = "Enter a valid ID";
        idStatus.className = "id-status error";
        return;
    }
    localStorage.setItem("cortex_user_id", id);
    idStatus.textContent = "✓ Saved";
    idStatus.className = "id-status success";
});

function getUserId() {
    const id = localStorage.getItem("cortex_user_id");
    return id ? parseInt(id, 10) : null;
}

async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

document.getElementById("btn-load-insights").addEventListener("click", async () => {
    const userId = getUserId();
    const el = document.getElementById("insights-output");
    if (!userId) {
        el.textContent = "⚠ Please set your User ID above first.";
        return;
    }
    el.textContent = "Loading…";
    try {
        const data = await fetchJSON(`${API_BASE}/analyze/${userId}`);
        el.textContent = data.insights;
    } catch (err) {
        el.textContent = `Error: ${err.message}`;
    }
});

document.getElementById("btn-load-plan").addEventListener("click", async () => {
    const userId = getUserId();
    const el = document.getElementById("plan-output");
    if (!userId) {
        el.textContent = "⚠ Please set your User ID above first.";
        return;
    }
    el.textContent = "Loading…";
    try {
        const data = await fetchJSON(`${API_BASE}/plan/${userId}`);
        el.textContent = data.plan;
    } catch (err) {
        el.textContent = `Error: ${err.message}`;
    }
});
