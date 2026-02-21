const API_BASE = "http://localhost:8000/api";
const USER_ID = 1; // TODO: load from chrome.storage

const output = document.getElementById("output");
const currentSite = document.getElementById("current-site");

// Show current tab domain in status bar
chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
    if (tab?.url) {
        try {
            currentSite.textContent = new URL(tab.url).hostname;
        } catch {
            currentSite.textContent = "unknown";
        }
    }
});

document.getElementById("btn-analyze").addEventListener("click", async () => {
    output.textContent = "Loading insights…";
    try {
        const res = await fetch(`${API_BASE}/analyze/${USER_ID}`);
        const data = await res.json();
        output.textContent = data.insights;
    } catch (err) {
        output.textContent = `Error: ${err.message}`;
    }
});

document.getElementById("btn-plan").addEventListener("click", async () => {
    output.textContent = "Generating plan…";
    try {
        const res = await fetch(`${API_BASE}/plan/${USER_ID}`);
        const data = await res.json();
        output.textContent = data.plan;
    } catch (err) {
        output.textContent = `Error: ${err.message}`;
    }
});
